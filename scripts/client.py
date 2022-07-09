#! /usr/bin/env python

from std_srvs.srv import SetBool
import rospy

if __name__ =="__main__":
  
    rospy.wait_for_service("bug0")
    rospy.wait_for_service("bug1")
    # rospy.wait_for_service("bug2")
    print("******************")
    bug0 =rospy.ServiceProxy("bug0",SetBool)
    bug1 =rospy.ServiceProxy("bug1",SetBool)
    # bug2 =rospy.ServiceProxy("bug2",SetBool)

    print("********************client is running***************************")
    mode = int(input("Please input the type of Bug algorithm you want to use \n 0 Bug0 \n 1 Bug1 \n 2 Bug2\n"))
    if mode==0:
        bug0(True)
        bug1(False)
        # bug2(False)
    elif mode==1:
        bug0(False)
        bug1(True)
        rospy.loginfo("bug1 in client")
        # bug2(False)
        