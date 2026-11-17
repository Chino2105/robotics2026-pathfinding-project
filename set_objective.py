#!/usr/bin/env python3

import rospy
import sys

def set_objective(x, y):
	
	rospy.wait_for_service('set_objective')
	try:
		set_objective_call = rospy.ServiceProxy('set_objective', Objective)
		response = set_objective_call(x, y)
		
	except rospy.ServiceException as e:
		print("Service call failed: %s"%e)
	
	
if __name__ == "__main__":
	
	if len(sys.argv) == 3:
		x = float(sys.argv[1])
		y = float(sys.argv[2])	
	else:
		sys.exit(1)



