#! /usr/bin/env python
from wk2Assignment_3.srv import HomingSignal3
import rospy
from geometry_msgs.msg import Twist
import random

if __name__ =="__main__":
    rospy.init_node("client")
    count_time=2
    pub = rospy.Publisher('wk2Bot3/cmd_vel',Twist,queue_size=1)
    twist =Twist()
   
    rate=rospy.Rate(1)
    while count_time<10:
        twist.linear.x=0.5
        twist.angular.z=(random.random()-0.5)*10
        pub.publish(twist)
        count_time+=1
        rate.sleep()


    twist.linear.x=0
    twist.angular.z=0
    pub.publish(twist)
       
        

    rospy.wait_for_service("bug0")
    rospy.wait_for_service("bug1")
    # rospy.wait_for_service("bug2")
    print("******************")

    desired_position_x = rospy.get_param('des_pos_x')
    desired_position_y = rospy.get_param('des_pos_y')
    bug0 =rospy.ServiceProxy("bug0",HomingSignal3)
    bug1 =rospy.ServiceProxy("bug1",HomingSignal3)
    # bug2 =rospy.ServiceProxy("bug2",SetBool)

    print("********************client is running***************************")
    mode = int(input("Please input the type of Bug algorithm you want to use \n 0 Bug0 \n 1 Bug1 \n 2 Bug2\n"))
   
  
    if mode==0:
        bug0(True, desired_position_x, desired_position_y,0),
        bug1(False, desired_position_x, desired_position_y,0)
        # bug2(False)
    elif mode==1:
        bug0(False, desired_position_x, desired_position_y,0)
        bug1(True, desired_position_x, desired_position_y,0)
        rospy.loginfo("bug1 in client")
        # bug2(False)
        