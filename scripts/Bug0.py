#! /usr/bin/env python


from turtlesim.srv import *
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from tf import transformations
from nav_msgs.msg import Odometry
from wk2Assignment_3.srv import HomingSignal3
from wk2Assignment_3.srv import SetBugBehaviour3
import rospy
import math

class Bug:
    def __init__(self,mode=1):
       

        self.state=0
        self.state_desc=[
            "Go to the point",
            "Follow the wall"
        ]
        self.yaw = 0
        self.raw_error_allowed = 5 * (math.pi / 180) # 5 degrees

        self.regions=None
        self.position=Point()

        self.desired_position = Point()
        self.desired_position.x = rospy.get_param('des_pos_x')
        self.desired_position.y = rospy.get_param('des_pos_y')
       
        
        if mode==2:
              teleport=rospy.ServiceProxy('wk2Bot3/teleport_absolute',TeleportAbsolute)
              teleport(self.desired_position.x,self.desired_position.y,0)

        self.dist_threshold = rospy.get_param('th_dist') # unit: meter

        self.sub_laser = rospy.Subscriber('/wk2Bot3/laser/scan', LaserScan, self.clbk_laser)
        self.sub_odom = rospy.Subscriber('/odom', Odometry, self.clbk_odom)
        
        rospy.wait_for_service('GoToPoint_switch')
        rospy.wait_for_service('followWall_switch')
        self.go_to_point=rospy.ServiceProxy('GoToPoint_switch',SetBugBehaviour3)
        self.follow_wall=rospy.ServiceProxy('followWall_switch',SetBugBehaviour3)


        self.change_state(0)
        
        while  not self.regions:
                continue
        rate=rospy.Rate(20)
        while not rospy.is_shutdown():
            # rospy.loginfo("state: %s"%self.state)
            if self.state == 0:
                
                err_pos =math.sqrt(pow(self.desired_position.y-self.position.y,2)+pow(self.desired_position.x-self.position.x,2))
                if err_pos<self.dist_threshold:
                    rospy.loginfo("wk2Bot3 has reached the charging station located at (%s,%s)"%(self.desired_position.x,self.desired_position.y))
                    break

                if 0.15<self.regions['front'] < 1 :
                    self.change_state(1)

            elif self.state == 1:
                desired_yaw = math.atan2(self.desired_position.y - self.position.y, self.desired_position.x - self.position.x)
                err_yaw = self.normalize_angle(desired_yaw - self.yaw)

                # less than 30 degrees
                if math.fabs(err_yaw) < (math.pi / 6) and \
                        self.regions['front'] > 1.5 and self.regions['fright'] > 1 and self.regions['fleft'] > 1:
                    self.change_state(0)

                # between 30 and 90
                if err_yaw > 0 and \
                        math.fabs(err_yaw) > (math.pi / 6) and \
                        math.fabs(err_yaw) < (math.pi / 2) and \
                        self.regions['left'] > 1.5 and  self.regions['fleft'] > 1:
                    self.change_state(0)

                if err_yaw < 0 and \
                        math.fabs(err_yaw) > (math.pi / 6) and \
                        math.fabs(err_yaw) < (math.pi / 2) and \
                        self.regions['right'] > 1.5 and self.regions['fright'] > 1:
                    self.change_state(0)
            rate.sleep()

          

    def change_state(self,state):
        self.state=state
        # print("***************changed follow wall or go to point************************")
        log= "state changed: %s"%self.state_desc[state]
        rospy.loginfo(log)
       
        if state==0:
            self.go_to_point(True,1.5,"left")
            self.follow_wall(False,1.5,"left") 

        if state==1:
            self.follow_wall(True,1.5,"left")
            self.go_to_point(False,1.5,"left")


           
       # rospy.loginfo(resp)

    def clbk_odom(self,msg):
        # position
        self.position = msg.pose.pose.position

        # yaw
        quaternion = (
            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w)
        euler = transformations.euler_from_quaternion(quaternion)
        self.yaw = euler[2]
     

    def clbk_laser(self,msg):
        """ ok """
        self.regions = {
            'right':  min(min(msg.ranges[0:143]), 10),
            'fright': min(min(msg.ranges[144:287]), 10),
            'front':  min(min(msg.ranges[288:431]), 10),
            'fleft':  min(min(msg.ranges[432:575]), 10),
            'left':   min(min(msg.ranges[576:719]), 10),
        }
       
     
       

    def normalize_angle(self,angle):
        if(math.fabs(angle) > math.pi):
            angle = angle - (2 * math.pi * angle) / (math.fabs(angle))
        return angle

def clbk_bug0(req):
    if req.flag:
        Bug()
    return "Done!"
    
if __name__=="__main__":
    rospy.init_node("bug0service")
  #  mode =int(input("Please choose the mode \n1 go to the point using bug0 algorithm \n 2 teleport"))
    rospy.Service("bug0",HomingSignal3,clbk_bug0)
    rospy.spin()