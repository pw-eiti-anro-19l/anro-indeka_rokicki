#!/usr/bin/env python

import sys
import rospy
from lab4.srv import service

def client(x, y, z, t):
    rospy.wait_for_service('service')
    try:
        service1 = rospy.ServiceProxy('service', service)
        tim = rospy.Time()
        tim.secs = t
        resp1 = service1(x, y, z, tim)
        print "Response: [%s %s %s %s]"%(resp1.x, resp1.y, resp1.z, resp1.t.secs)
        return
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y z t]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 5:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
        z = float(sys.argv[3])
        t = int(sys.argv[4])
    else:
        print usage()
        sys.exit(1)
    print "Requesting %s %s %s %s"%(x, y, z, t)
    client(x, y, z, t)
