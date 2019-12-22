#!/usr/bin/env python3

# node for turning gamepad inputs into drive commands
import math
import rospy
import numpy as np
import indydcp_client as client
from geometry_msgs.msg import Twist


bind_ip   = "192.168.0.14"
server_ip = "10.82.10.62"

name = "NRMK-Indy7"
indy = client.IndyDCPClient(bind_ip, server_ip, name)
indy.connect()
print(indy.is_connected())
indy.reset_robot()
indy.go_home()
pos1 = [0,0,0,0,0,0]

def publish_status():
	status = Twist()
	status_list = indy.get_joint_pos()
	print(status_list)
	status.linear.x = status_list[0]
	status.linear.y = status_list[0]
	status.linear.z = status_list[0]
	status.angular.x = status_list[0]
	status.angular.y = status_list[0]
	status.angular.z = status_list[0]
	status_pub.publish(status)

def joint_callback(msg):
	joint=[msg.linear.x, msg.linear.y, msg.linear.z, msg.angular.x, msg.angular.y,  msg.angular.z]
	if indy.is_move_finished():
		indy.joint_move_to(joint)

def key_callback(msg):
	global pos1
	indy.stop_motion()
	pos=[msg.linear.x, msg.linear.y, msg.linear.z, msg.angular.x, msg.angular.y,  msg.angular.z]
	if pos != pos1:	
		indy.task_move_by(pos)
	pos1 = pos

rospy.init_node('indy_move')
status_pub = rospy.Publisher('/indy/status', Twist, queue_size=1)
rospy.Subscriber('/indy/move/joint', Twist, joint_callback)
rospy.Subscriber('/indy/move/key', Twist, key_callback)
publish_status()

# wait before shutdown
rospy.spin()
