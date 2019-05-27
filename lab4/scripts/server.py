#!/usr/bin/env python

import sys
import rospy
import time
import math as m
from lab4.srv import *
from sensor_msgs.msg import JointState

#req.t typu Time

RATE = 10
TOP_SPEED = 1

def handle_service(data):
    print "Returning [%s %s %s %s]"%(data.x, data.y, data.z, data.t.secs)
    dpos = [data.x-pos[0], data.y-pos[1], data.z-pos[2]]
    lenght = m.sqrt(m.pow(dpos[0],2)+m.sqrt(m.pow(dpos[1],2)+m.pow(dpos[2],2)))
    if (data.t.secs==0):
	return False
    if (lenght/data.t.secs>TOP_SPEED):
	rospy.loginfo("Too fast")
	return False
    i = data.t.secs/RATE

    # interpolacja
    if (i!=0):
    	dpos[0] = dpos[0]/i
    	dpos[1] = dpos[1]/i
    	dpos[2] = dpos[2]/i


    rate = rospy.Rate(RATE)
    pub_msg = JointState()
    pub_msg.header.frame_id = 'base_link'
    pub_msg.name = ['base_to_link1','link1_to_link2','link2_to_link3']
    while(i):
        pub_msg.position = [pos[0]+ dpos[0],pos[1]+ dpos[1],pos[2]+ dpos[2]]
        pub.publish(pub_msg)
	i-=1
        rate.sleep

    pos[0] = data.x
    pos[1] = data.y
    pos[2] = data.z
    pub_msg.position = [pos[0],pos[1],pos[2]]
    pub.publish(pub_msg)
    return serviceResponse(data.x, data.y, data.z, data.t)

def server():
    rospy.init_node('jint_v2')
    global pub
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    s = rospy.Service('service', service, handle_service)
    print "Server ready."
    rospy.spin()

if __name__ == "__main__":
    pos = [0, 0, 0]
    server()
