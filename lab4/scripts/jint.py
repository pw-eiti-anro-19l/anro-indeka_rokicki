#!/usr/bin/env python

import sys
import rospy
import time
import math as m
from lab4.srv import *
from sensor_msgs.msg import JointState #Subscribe Header header string[] name float64[] position float64[] velocity float64[] effort
#Pose Point position Quaternion orientation
#Point float64 x float64 y float64 z
#Quaternion float64 x float64 y float64 z float64 w

RATE = 10
TOP_SPEED = 1


def my_node():
    global pub
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('JINT', anonymous=True)

    pub_msg = JointState
    pub_msg.header = "base_link"
    pub_msg.position = [pos[0],pos[1],pos[2]]
    pub.publish(pub_msg)
    while (1):
        rospy.wait_for_service('service') 
        try:
            service1 = rospy.ServiceProxy('service', service)
      	    tim = rospy.Time()
            tim.secs = t
            resp1 = service1(x, y, z, tim)
            tab = [resp1.x, resp1.y, resp1.z, resp1.t]
            print str(resp1.x)
            foo(tab)
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e


        rospy.spin()

def foo(data):
#    rospy.loginfo(rospy.get_caller_id() + 'I heard position %f from %s', data.position[0], data.name[0])

    dpos = [data[0]-pos[0], data[1]-pos[1], data[2]-pos[2]]
    lenght = m.sqrt(m.pow(dpos[0],2)+m.sqrt(m.pow(dpos[1],2)+m.pow(dpos[2],2)))
    if (data[3].secs==0):
	return False
    if (lenght/data[3].secs>TOP_SPEED):
	rospy.loginfo("Too fast")
	return False
    i = data.position[3]/RATE

    # interpolacja
    dpos = dpos/i

    rate = rospy.Rate(RATE)
    pub_msg = JointState
    pub_msg.header.frame_id = "base_link"
    while(i):
        pub_msg.position[0] = pos[0] + dpos[0]
        pub_msg.position[1] = pos[1] + dpos[1]
        pub_msg.position[2] = pos[2] + dpos[2]
        pub.publish(pub_msg)
	i-=1
    rate.sleep

    pos[0] = data[0]
    pos[1] = data[1]
    pos[2] = data[2]
    pub_msg.position[0] = data[0]
    pub_msg.position[1] = data[1]
    pub_msg.position[2] = data[2]
    pub.publish(pub_msg)


if __name__ == '__main__':
    pos = [0, 0, 0]
    x=float(0)
    y=float(0)
    z=float(0)
    t=int(0)
    try:
        my_node()
    except rospy.ROSInterruptException:
        pass

