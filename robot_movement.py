#!/usr/bin/env python3
import math
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class RobotMover:
    def __init__(self):
        # Sends speed commands to the wheels
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Listens to the robot's current position from wheel odometry
        rospy.Subscriber('/odom', Odometry, self.odom_callback)

        self.current_x = 0.0
        self.current_y = 0.0
        self.got_odom = False

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        self.got_odom = True

    def stop(self):
        self.cmd_pub.publish(Twist())

    def move_relative(self, move_up, move_left):
        """
        move_up: meters forward (negative = backward)
        move_left: meters left (negative = right)
        """
        while not self.got_odom and not rospy.is_shutdown():
            rospy.sleep(0.1)

        target_x = self.current_x + move_up
        target_y = self.current_y + move_left

        rate = rospy.Rate(10)
        cmd = Twist()

        while not rospy.is_shutdown():
            diff_x = target_x - self.current_x
            diff_y = target_y - self.current_y
            distance = math.hypot(diff_x, diff_y)

            # Stop once within 5 cm of target
            if distance < 0.05:
                self.stop()
                rospy.loginfo("Reached target!")
                break

            speed = 0.2
            cmd.linear.x = speed * (diff_x / distance)
            cmd.linear.y = speed * (diff_y / distance)

            self.cmd_pub.publish(cmd)
            rate.sleep()


if __name__ == '__main__':
    rospy.init_node('robot_movement_test')
    mover = RobotMover()
    rospy.loginfo("Testing movement: 0.5m forward, 0.3m left...")
    mover.move_relative(0.5, 0.3)
