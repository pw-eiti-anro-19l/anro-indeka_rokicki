#!/usr/bin/env python

from lab4.srv import service
import rospy

#req.t typu Time

def handle_service(req):
    print "Returning [%s %s %s %s]"%(req.x, req.y, req.z, req.t.secs)
    return serviceResponse(req.x, req.y, req.z, req.t)

def server():
    rospy.init_node('server')
    s = rospy.Service('service', service, handle_service)
    print "Server ready."
    rospy.spin()

if __name__ == "__main__":
    server()
