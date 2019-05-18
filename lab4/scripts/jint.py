#!/usr/bin/env python

import rospy
import time
import math as m
# TODO import lab4 srv
from sensor_msgs.msg import JointState #Subscribe Header header string[] name float64[] position float64[] velocity float64[] effort
#Pose Point position Quaternion orientation
#Point float64 x float64 y float64 z
#Quaternion float64 x float64 y float64 z float64 w

def my_node():
    rospy.init_node('JINT', anonymous=True)
    global pub
    pub = rospy.Publisher('pub_joint', JointState, queue_size=10)
    rospy.Subscriber('service', service, callback)
    rospy.spin()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard position %f from %s', data.position[0], data.name[0])

    #dpos = {data.position[0]-m.pos[0], data.position[1]-m.pos[1], data.position[2]-m.pos[2]} 
    #lenght = m.sqrt(m.pow(dpos[0],2)+m.sqrt(m.pow(dpos[1],2)+m.pow(dpos[2],2)))
    #if (lenght/data.position[3]>TOP_SPEED)
	#rospy.loginfo("Too fast")
	#return???????
    #i = data.position[3]/RATE

    # interpolacja
    #dpos = dpos/i

    #rate = rospy.Rate(RATE)
    pub_msg = JointState
    pub_msg.header.frame_id = "base_link"
    #while(i) 
        #pub_msg.position[0] = pos[0] + dpos[0]
        #pub_msg.position[1] = pos[1] + dpos[1]
        #pub_msg.position[2] = pos[2] + dpos[2]
        #pub.publish(pub_msg)
	#i--
    #rate.sleep

    # wyeliminowanie niedokładności
    #pos[0] = data.position[0]
    #pos[1] = data.position[1]
    #pos[2] = data.position[2] 
    pub_msg.position[0] = data.position[0]
    pub_msg.position[1] = data.position[1]
    pub_msg.position[2] = data.position[2]
    pub.publish(pub_msg)


if __name__ == '__main__':
#define    RATE = 10
#define    TOP_SPEED = 1
    #pos = {0, 0, 0}
    try:
        my_node()
    except rospy.ROSInterruptException:
        pass

