#!/usr/bin/env python

import rospy
import PyKDL as kdl
import json
import os
from geometry_msgs.msg import PoseStamped #Publish Header header Pose pose
from sensor_msgs.msg import JointState #Subscribe Header header string[] name float64[] position float64[] velocity float64[] effort
#Pose Point position Quaternion orientation
#Point float64 x float64 y float64 z
#Quaternion float64 x float64 y float64 z float64 w

def my_node():
    rospy.init_node('NONKDL_DKIN', anonymous=True)
    global pub
    pub = rospy.Publisher('pub_pose', PoseStamped, queue_size=10) #to who
    rospy.Subscriber('joint_states', JointState, callback)
    rospy.spin()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard position %f from %s', data.position[0], data.name[0])

    chain = kdl.Chain()
#   helpFrame = kdl.Frame()
#
#   outFrame = helpFrame.DH(0, 0, 0, 0)
#   chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.None), outFrame))
#   outFrame = helpFrame.DH(a1, d1, al1, th1)
#   chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), outFrame))
#   outFrame = helpFrame.DH(a2, d2, al2, th2)
#   chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), outFrame))
#   outFrame = helpFrame.DH(a3, d3, al3, th3)
#   chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), outFrame))

    rot = kdl.Rotation(0,1,0, 0,0,1, 1,0,0)
    
    #chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.None), kdl.Frame(kdl.Vector(0.0,0.0,0.0))))
    chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), kdl.Frame(rot, kdl.Vector(1.0,0.0,0.0))))
    chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), kdl.Frame(rot, kdl.Vector(1.0,0.0,0.0))))
    chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), kdl.Frame(rot, kdl.Vector(1.0,0.0,0.0))))


    fksolver = kdl.ChainFkSolverPos_recursive(chain)

    jpos = kdl.JntArray(chain.getNrOfJoints())    
    jpos[2] = data.position[0]
    jpos[1] = data.position[1]
    jpos[0] = data.position[2]

    cartpos = kdl.Frame()
    
    fksolver.JntToCart(jpos,cartpos)

    pub_msg = PoseStamped()
    pub_msg.header.frame_id = "base_link"
    pub_msg.pose.position.x = cartpos.p[2]
    pub_msg.pose.position.y = cartpos.p[1]
    pub_msg.pose.position.z = cartpos.p[0]
    pub.publish(pub_msg)

if __name__ == '__main__':
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../dh.json', 'r') as file:
	params = json.loads(file.read())
	a1, d1, al1, th1 = params['i1']
	a2, d2, al2, th2 = params['i2']
	a3, d3, al3, th3 = params['i3']
	a1, d1, al1, th1 = float(a1), float(d1), float(al1), float(th1)
	a2, d2, al2, th2 = float(a2), float(d2), float(al2), float(th2)
	a3, d3, al3, th3 = float(a3), float(d3), float(al3), float(th3)
    try:
        my_node()
    except rospy.ROSInterruptException:
        pass

