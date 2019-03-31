#!/usr/bin/env python

import click
import rospy
from geometry_msgs.msg import Twist


def zolw():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('zolw')
    
    while not rospy.is_shutdown():
        twist = Twist()
	key = click.getchar()

        up = rospy.get_param("up")
        down = rospy.get_param("down")
        left = rospy.get_param("left")
        right = rospy.get_param("right")

        if key == up :
            twist.linear.x=2.0
        if key == down :
            twist.linear.x=-1.0
        if key == left :
            twist.angular.z=1.5
        if key == right :
            twist.angular.z=-1.5

        pub.publish(twist)

if __name__ == '__main__':
    try:
        zolw()
    except rospy.ROSInterruptException:
	pass
