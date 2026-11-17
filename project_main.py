#! usr/bin/env python3

import rospy
from robotics_project.srv import Objective, ObjectiveResponse




def handle_set_objective(req):
	path_to_objective(req.x, req.y)
	return ObjectiveResponse("Pathing to ["+req.x+", "+req.y+"]")	
	
def project_main():
	
	rospy.init_node('project_main')
	objective_in = rospy.Service('set_objective', Objective, handle_set_objective)

	rospy.spin()
	
def path_to_objective(x, y):







if __name__ == "__main__":
	project_main()
