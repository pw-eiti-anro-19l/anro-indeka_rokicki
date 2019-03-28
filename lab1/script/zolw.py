#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import sys, termios, tty, os, time

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
button_delay = 0.2

def zolw():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('zolw', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    while not rospy.is_shutdown():
        key = getch()
        up = rospy.get_param("up")
        down = rospy.get_param("down")
        left = rospy.get_param("left")
        right = rospy.get_param("right")
        msg_t = Twist()
        if key == up :
            msg_t.linear.x=2.0
        if key == down :
            msg_t.linear.x=-2.0
        if key == left :
            msg_t.angular.z=1.8
        if key == right :
            msg_t.angular.z=-1.8
        rospy.loginfo(msg_t)
        rospy.loginfo(key)
        pub.publish(msg_t)
        if key == 'c' :
            sys.exit(0)
        rate.sleep()

if __name__ == '__main__':
    try:
        zolw()
    except rospy.ROSInterruptException:
	pass
