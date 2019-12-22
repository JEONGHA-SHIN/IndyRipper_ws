#!/usr/bin/python


import math
import rospy
import keyboard as Key
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from std_msgs.msg import String

toss_key=0
indy_status=[0,0,0,0,0,0]
gripper_status=0
station_status=0


class indy_gripper:
	def __init__(self):
		rospy.init_node("indy_gripper")
		self.data = None
		self.i_msg = Twist()
		self.g_msg = Float32()
		self.s_msg = String()

		self.indy_status = [0, 0, 0, 0, 0, 0]
		self.gripper_status = 0
		self.station_status = ""

		self.indy_task = ""
		self.gripper_task = ""
		self.station_task = ""
	 
		self.indy_sub = rospy.Subscriber("/indy/status",Twist, self.indy_status_cb)
		self.gripper_sub = rospy.Subscriber("/gripper/status",Float32, self.gripper_status_cb)
		self.FCstation_sub = rospy.Subscriber("/station/status",String, self.station_status_cb)
	
		self.indy_joint_pub = rospy.Publisher('/indy/move/joint', Twist, queue_size=1)
		self.indy_key_pub = rospy.Publisher('/indy/move/key', Twist, queue_size=1)
		self.gripper_angle_pub = rospy.Publisher('/gripper/move/angle', Float32, queue_size=1)
		self.gripper_key_pub = rospy.Publisher('/gripper/move/key', Float32, queue_size=1)
		self.station_pub = rospy.Publisher('/station/move', String, queue_size=1)
		self.station_key_pub = rospy.Publisher('/station/move/key', String, queue_size=1)
	
		indy_move = "indy_move"
		gripper_move = "gripper_move"
		finger_change = "finger_change"
		exit = "exit"

		joint = "joint"
		keyboard = "keyboard"
		status = "status"
		angle = "angle"
		load = "load"
		unload = "unload"

		while True:
			main_task = input("What do you want to do? (indy_move/gripper_move/finger_change)")
			if main_task =="indy_move":
				while True:
					self.indy_task = input("What do you want to do? (joint/keyboard/status)")
					if self.indy_task == "exit":
							break
					else:					
						self.indy()

			elif main_task =="gripper_move":
				while True:
					self.gripper_task = input("What do you want to do? (angle/keyboard/status)")
					if self.gripper_task == "exit":
						break
					else:
						self.gripper()
			
			elif main_task =="finger_change":
				while True:
					self.station_task = input("What do you want to do? (load/unload/keyboard/status)")
					if self.station_task == "exit":
						break
					else:
						self.fc_station()
			else:
				break



	def indy(self):
		joint = "joint"
		keyboard = "keyboard"
		status = "status"
		exit = "exit"

		if self.indy_task==joint:
			while True:
				indy_target_joints_list = input("write target joint [0,0,0,0,0,0]")
				if indy_target_joints_list =="exit":
					break
				else:
						self.i_msg.linear.x = indy_target_joints_list[0]
						self.i_msg.linear.y = indy_target_joints_list[1]
						self.i_msg.linear.z = indy_target_joints_list[2]
						self.i_msg.angular.x = indy_target_joints_list[3]
						self.i_msg.angular.y = indy_target_joints_list[4]
						self.i_msg.angular.z = indy_target_joints_list[5]
						self.indy_joint_pub.publish(self.i_msg)
				
		elif self.indy_task=="keyboard":			
			while True:
				self.i_msg.linear.x = 0
				self.i_msg.linear.y = 0
				self.i_msg.linear.z = 0
				self.i_msg.angular.x = 0
				self.i_msg.angular.y = 0
				self.i_msg.angular.z = 0

				if Key.is_pressed('q'): 
					break

				elif Key.is_pressed('j'): 
					self.i_msg.linear.x = 1
				elif Key.is_pressed('l'): 
					self.i_msg.linear.x = -1
				elif Key.is_pressed('i'): 
					self.i_msg.linear.y = 1
				elif Key.is_pressed(','): 
					self.i_msg.linear.y = -1
				elif Key.is_pressed('w'): 
					self.i_msg.linear.z = 1
				elif Key.is_pressed('x'): 
					self.i_msg.linear.z = -1

				elif Key.is_pressed('u'): 
					self.i_msg.angular.x = 1
				elif Key.is_pressed('o'): 
					self.i_msg.angular.x = -1
				elif Key.is_pressed('m'): 
					self.i_msg.angular.y = 1
				elif Key.is_pressed('.'): 
					self.i_msg.angular.y = -1
				elif Key.is_pressed('e'): 
					self.i_msg.angular.z = 1
				elif Key.is_pressed('c'): 
					self.i_msg.angular.z = -1
				self.indy_key_pub.publish(self.i_msg)
					 

		elif self.indy_task=="status":
			print(self.indy_status)
		


	def gripper(self):
		angle = "angle"
		keyboard = "keyboard"
		status = "status"
		exit = "exit"

		if self.gripper_task=="angle":
			while True:
				gripper_target_angle = input()
				if gripper_target_angle =="exit":
					break
				else:
						self.g_msg = gripper_target_angle		
						self.gripper_angle_pub.publish(self.g_msg)
				
		elif self.gripper_task=="keyboard":
			while True:
				self.g_msg = 0
				
				if Key.is_pressed('q'): 
					break

				elif Key.is_pressed(','): 
					self.g_msg = -1
				elif Key.is_pressed('.'): 
					self.g_msg = 1
				
				self.gripper_key_pub.publish(self.g_msg)


		elif self.gripper_task=="status":
			print(self.gripper_status)
	
		



	def fc_station(self):
		load = "load"
		unload = "unload"
		keyboard = "keyboard"
		status = "status"
		exit = "exit"

		if self.station_task=="load":
			self.s_msg = "load"
			self.station_pub.publish(self.s_msg)
		elif self.station_task=="unload":
			self.s_msg = "unload"
			self.station_pub.publish(self.s_msg)
				
		elif self.station_task=="keyboard":
			while True:
				self.s_msg = ""
				
				if Key.is_pressed('q'): 
					break

				elif Key.is_pressed(','): 
					self.s_msg = "backward"
				elif Key.is_pressed('.'): 
					self.s_msg = "forward"
				
				self.station_key_pub.publish(self.s_msg)

		elif self.station_task=="status":
			print(self.station_status)
	
	
	def indy_status_cb(self, data):
		self.indy_status = self.data

	def gripper_status_cb(self, data):
		self.gripper_status = self.data

	def station_status_cb(self, data):
		self.station_status = self.data
			
			
if __name__ == "__main__":
	try:
		node = indy_gripper()
		rospy.spin()		


	except rospy.ROSInterruptException:
		exit()



