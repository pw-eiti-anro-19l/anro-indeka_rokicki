#!/usr/bin/env python

import rospy
import PyKDL as kdl
import yaml
from geometry_msgs.msg import PoseStamped #Publish Header header Pose pose
from sensor_msgs.msg import JointState #Subscribe Header header string[] name float64[] position float64[] velocity float64[] effort
#Pose Point position Quaternion orientation
#Point float64 x float64 y float64 z
#Quaternion float64 x float64 y float64 z float64 w

def my_node():
    #with open('../urdf.yaml', 'r') as file:
    #    parsed = yaml.load(file)
    #    print(yaml.dump(parsed))

    rospy.init_node('NONKDL_DKIN', anonymous=True)
    global pub
    pub = rospy.Publisher('pub_pose', PoseStamped, queue_size=10) #to who
    rospy.Subscriber('joint_states', JointState, callback)
    rospy.spin()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard position %f from %s', data.position[0], data.name[0])

    chain = kdl.Chain()
# ten fragment dopracować
    rot = kdl.Rotation(0,0,1.57075, 1.57075,0,0, 0,0,0)
    
    chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.None), kdl.Frame(kdl.Vector(0.0,0.0,1.0))))
    chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), kdl.Frame(rot,kdl.Vector(0.0,0.0,1.0))))
    chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), kdl.Frame(rot,kdl.Vector(0.0,0.0,1.0))))
    chain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), kdl.Frame(rot,kdl.Vector(0.0,0.0,1.0))))

    fksolver = kdl.ChainFkSolverPos_recursive(chain)

    jpos = kdl.JntArray(chain.getNrOfJoints())    
    jpos[2] = data.position[2]
    jpos[1] = data.position[1]
    jpos[0] = data.position[0]
#
    cartpos = kdl.Frame()
    
    fksolver.JntToCart(jpos,cartpos)

    pub_msg = PoseStamped()
    pub_msg.header.frame_id = "base_link"
    pub_msg.pose.position.x = cartpos.p[0]
    pub_msg.pose.position.y = cartpos.p[1]
    pub_msg.pose.position.z = cartpos.p[2]
    pub.publish(pub_msg)

if __name__ == '__main__':
    try:
        my_node()
    except rospy.ROSInterruptException:
        pass

