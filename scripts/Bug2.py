#! /usr/bin/env python

from gazebo_msgs.srv import SetModelState
from turtlesim.srv import *
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from tf import transformations
from nav_msgs.msg import Odometry
from wk2Assignment_3.srv import * 

import rospy
import math

class Bug:
    def __init__(self,mode=1):
       
        rospy.loginfo("bug2 is run")
        self.state=0
        self.state_desc=[
            "Go to point",
            "Circumnavigate obstacle"
        ]

        self.speed=0.5
        self.turning="left"
        self.yaw = 0
        self.raw_error_allowed = 5 * (math.pi / 180) # 5 degrees

        self.regions=None
        self.position=Point()
        self.initial_position=Point()
        self.initial_position.x=rospy.get_param('init_x')
        self.initial_position.y=rospy.get_param('init_y')

        self.desired_position = Point()
        self.desired_position.x = rospy.get_param('des_pos_x')
        self.desired_position.y = rospy.get_param('des_pos_y')

        self.circumnavigate_starting_point=Point()
        self.circumnavigate_closet_point=Point()

        #self.count_state_time=0
        self.count_loop=0
        
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
        #self.set_model_state=rospy.ServiceProxy()

        self.change_state(0)
        
        while not self.regions:
            continue

        rate=rospy.Rate(20)

        while not rospy.is_shutdown():
            # rospy.loginfo("state: %s"%self.state)
            distance_position_to_line = self.distance_to_line(self.position)

            if self.state == 0:

                err_pos = math.sqrt(pow(self.desired_position.y-self.position.y,2)+pow(self.desired_position.x-self.position.x,2))
                if err_pos < self.dist_threshold:
                    rospy.loginfo("wk2Bot3 has reached the charging station located at (%s,%s)"%(self.desired_position.x,self.desired_position.y))
                    break

                if 0.15 < self.regions['front'] < 1 :
                    self.change_state(1)

            elif self.state == 1:
                    if self.count_state_time > 5 and distance_position_to_line < 0.1:
                        self.change_state(0)

            self.count_loop += 1
            if self.count_loop == 20:
                self.count_state_time += 1
                self.count_loop = 0

            #rospy.loginfo("distance to line: [%.2f], position: [%.2f, %.2f]", self.distance_to_line(self.position), self.position.x, self.position.y)
            rate.sleep()
          

    def change_state(self,state):
        self.state=state
        # print("***************changed  go to point or go to closet follow wall or************************")
        log= "state changed: %s"%self.state_desc[state]
        rospy.loginfo(log)

        self.count_state_time=0
       
        if state==0:
            self.go_to_point(True,self.speed,self.turning)
            self.follow_wall(False,self.speed,self.turning) 

        if state==1:
            self.go_to_point(False,self.speed,self.turning)
            self.follow_wall(True,self.speed,self.turning)

    def distance_to_line(self, p0):
        # calculate the distance of the robot to the initial line
	# p0 - current position  p1 - initial position  p2 - desired positon
        p1 = self.initial_position
        p2 = self.desired_position
        up_eq = math.fabs((p2.y - p1.y) * p0.x - (p2.x - p1.x) * p0.y + (p2.x * p1.y) - (p2.y * p1.x))
        lo_eq = math.sqrt(pow(p2.y - p1.y, 2) + pow(p2.x - p1.x, 2))
        distance = up_eq / lo_eq
        return distance

    def calc_dist_points(self,point1,point2):
        return math.sqrt((point1.y-point2.y)**2+(point1.x-point2.x)**2)

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


def clbk_bug2(req):
    if req.flag:
        Bug()
    return "Done!"

if __name__=="__main__":
    rospy.init_node("bug1service")
  #  mode =int(input("Please choose the mode \n1 go to the point using bug0 algorithm \n 2 teleport"))
    rospy.Service("bug2",HomingSignal3,clbk_bug2)
    rospy.spin()
   
