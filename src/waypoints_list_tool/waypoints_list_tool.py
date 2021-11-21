#!/usr/bin/env python

import threading
import rospy
import actionlib
from smach import State, StateMachine
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

from geometry_msgs.msg import PoseWithCovarianceStamped, PoseArray, PointStamped, PolygonStamped, Polygon, Point32

from std_msgs.msg import Empty
from tf import TransformListener
import tf
import math
import rospkg
import csv
import time
from geometry_msgs.msg import PoseStamped

class Mngt_path():
	def __init__(self):

		# Initialisations related to path following 

#		State.__init__(self, outcomes=['success'], input_keys=['waypoints'])
		self.frame_id = rospy.get_param('~goal_frame_id', 'map')
		self.odom_frame_id = rospy.get_param('~odom_frame_id', 'odom')
		self.base_frame_id = rospy.get_param(
			'~base_frame_id', 'base_footprint')
		self.duration = rospy.get_param('~wait_duration', 0.0)
		# Todo repace next section by parameters
		self.starting_waypoint=0
		self.ending_waypoint=-1 # Enter the value	-1 for all the list 
		# initialize shared waypoints list
		self.waypoints = []		
		# Path for saving and retreiving the pose.csv file
		self.output_file_path = rospkg.RosPack().get_path(
			'waypoints_list_tool')+"/saved_path/pose.csv"
		# ens of todo

		# Get a move_base action client
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		rospy.loginfo('Connecting to move_base...')
		self.client.wait_for_server()
		rospy.loginfo('Connected to move_base.')
		rospy.loginfo('Starting a tf listner.')
		self.tf = TransformListener()
		self.listener = tf.TransformListener()
		self.distance_tolerance = rospy.get_param(
			'waypoint_distance_tolerance', 0.0)

		# Initialisations related to path following 


		# Subscribe to pose message to get new waypoints
		self.addpose_topic = rospy.get_param('~addpose_topic', '/initialpose')
		# Create publsher to publish waypoints as pose array so that you can see them in rviz, etc.
		self.posearray_topic = rospy.get_param(
			'~posearray_topic', '/waypoints')
		self.poseArray_publisher = rospy.Publisher(
			self.posearray_topic, PoseArray, queue_size=1)
		self.posearray_topic = rospy.get_param(
			'~posearray_topic', '/waypoints')
		self.polygone_publisher = rospy.Publisher(
			'/waypoint_editor/path', PolygonStamped, queue_size=1)
#		self.print_menu()	

# General functions

	def changePose(self, waypoint, target_frame):
		if waypoint.header.frame_id == target_frame:
			# already in correct frame
			return waypoint
		if not hasattr(self.changePose, 'listener'):
			self.changePose.listener = tf.TransformListener()
		tmp = PoseStamped()
		tmp.header.frame_id = waypoint.header.frame_id
		tmp.pose = waypoint.pose.pose
		try:
			self.changePose.listener.waitForTransform(
				target_frame, tmp.header.frame_id, rospy.Time(0), rospy.Duration(3.0))
			pose = self.changePose.listener.transformPose(target_frame, tmp)
			ret = PoseWithCovarianceStamped()
			ret.header.frame_id = target_frame
			ret.pose.pose = pose.pose
			return ret
		except:
			rospy.loginfo("CAN'T TRANSFORM POSE TO {} FRAME".format(target_frame))
			exit()

	def convert_PoseWithCovArray_to_PoseArray(self):
		"""Used to publish waypoints as pose array so that you can see them in rviz, etc."""
		poses = PoseArray()
		poses.header.frame_id = rospy.get_param('~goal_frame_id', 'map')
		poses.poses = [pose.pose.pose for pose in self.waypoints]
	#	print(poses)
		return poses

	def convert_PoseWithCovArray_to_Polygone(self):
		# Used to publish waypoints as pose array so that you can see them in rviz, etc.
		poly = PolygonStamped()
		poly.header.frame_id = rospy.get_param('~goal_frame_id', 'map')
		poly.header.stamp = rospy.Time.now()
	#	print(poly)
		poly.polygon = Polygon()
		for pose in self.waypoints:

			#		print(pose.pose.pose.position)
			poly_point = Point32()
			poly_point.x = pose.pose.pose.position.x
			poly_point.y = pose.pose.pose.position.y
			poly_point.z = pose.pose.pose.position.z
			poly.polygon.points.append(poly_point)

	#	print(poly)
		return poly	

	def initialize_path_queue(self):
		global waypoints
		self.waypoints = []  # the waypoint queue
		# publish empty waypoint queue as pose array so that you can see them the change in rviz, etc.
		self.display_waypoints_in_rviz()
	

	def display_waypoints_in_rviz(self):
		self.poseArray_publisher.publish(
			self.convert_PoseWithCovArray_to_PoseArray())
		self.polygone_publisher.publish(
			self.convert_PoseWithCovArray_to_Polygone())

	def Read_Waypoints_csv(self):
		global waypoints
		with open(self.output_file_path, 'r') as file:
			reader = csv.reader(file, delimiter=',')
			for row in reader:
				print(row)
				current_pose = PoseWithCovarianceStamped()
				current_pose.pose.pose.position.x = float(row[0])
				current_pose.pose.pose.position.y = float(row[1])
				current_pose.pose.pose.position.z = float(row[2])
				current_pose.pose.pose.orientation.x = float(row[3])
				current_pose.pose.pose.orientation.y = float(row[4])
				current_pose.pose.pose.orientation.z = float(row[5])
				current_pose.pose.pose.orientation.w = float(row[6])
				self.waypoints.append(current_pose)

			#print(waypoints)
			self.display_waypoints_in_rviz()
		return 0

	def write_waypoints_csv(self):
		
		with open(self.output_file_path, 'w') as file:
#			print(self.waypoints)
			for current_pose in self.waypoints:
				file.write(str(current_pose.pose.pose.position.x) + ',' + str(current_pose.pose.pose.position.y) + ',' + str(current_pose.pose.pose.position.z) + ',' + str(
					current_pose.pose.pose.orientation.x) + ',' + str(current_pose.pose.pose.orientation.y) + ',' + str(current_pose.pose.pose.orientation.z) + ',' + str(current_pose.pose.pose.orientation.w) + '\n')
			rospy.loginfo('poses written to ' + self.output_file_path)
		return

	def print_menu(self):
#		global selected_waypoint, x, y, stepX, stepY, current_selection_label, current_selection ,current_manage_mode,current_manage_sub_mode
		print("")
		print("")
		print("1.New path")
		print("2.Import path from csv")
		print("3.Manage list ")
		print("4.Rearange orientations")
		print("5.Simulate all")
		print("6.Simulate range")
		print("7.Save")
		print("8.Quit")	
		print("")

	def drive_path(self):
		print(self.ending_waypoint,self.starting_waypoint)
		# Execute waypoints each in sequence
		if (self.ending_waypoint)<0: #enter -1 to go to last waypoint
				self.ending_waypoint=len(self.waypoints)
		if (self.ending_waypoint)>len(self.waypoints):
				self.ending_waypoint=len(self.waypoints)
		if (self.starting_waypoint)<0:
				self.starting_waypoint=0
		print(self.ending_waypoint,self.starting_waypoint)		
#		if (starting_waypoint)>len(waypoints):
#		starting_waypoint=raw_input("Starting after last waypoint, enter a new value ? ")
		position_in_list=0
		for waypoint in self.waypoints:
			# Break if preempted
			position_in_list=position_in_list+1
			if self.waypoints == []:
				rospy.loginfo('The waypoint queue has been reset.')
				break
			# Otherwise publish next waypoint as goal
			test=(position_in_list >= self.starting_waypoint and position_in_list < self.ending_waypoint)
			test1=(position_in_list >= self.starting_waypoint)
			test2=(position_in_list < self.ending_waypoint)
			print(self.starting_waypoint,position_in_list, self.ending_waypoint,test1,test2,test)
			test4=True				
			# Move to the points in the list
			if test:
				goal = MoveBaseGoal()
				goal.target_pose.header.frame_id = self.frame_id
				goal.target_pose.pose.position = waypoint.pose.pose.position
				goal.target_pose.pose.orientation = waypoint.pose.pose.orientation
				rospy.loginfo('Executing move_base goal to position (x,y): %s, %s' %
							(waypoint.pose.pose.position.x, waypoint.pose.pose.position.y))
				rospy.loginfo(
					"To cancel the goal: 'rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}'")
				self.client.send_goal(goal)
				if not self.distance_tolerance > 0.0:
					self.client.wait_for_result()
					rospy.loginfo("Waiting for %f sec..." % self.duration)
					time.sleep(self.duration)
				else:
					# This is the loop which exist when the robot is near a certain GOAL point.
					distance = 10
					while(distance > self.distance_tolerance):
						now = rospy.Time(now)
						self.listener.waitForTransform(
							self.odom_frame_id, self.base_frame_id, now, rospy.Duration(4.0))
						trans, rot = self.listener.lookupTransform(
							self.odom_frame_id, self.base_frame_id, now)
						distance = math.sqrt(pow(
							waypoint.pose.pose.position.x-trans[0], 2)+pow(waypoint.pose.pose.position.y-trans[1], 2))
		return 

	def receive_poses_from_rviz(self):
		
		self.initialize_path_queue()
		self.path_ready = False

		# Start thread to listen for when the path is ready (this function will end then)
		# Also will save the clicked path to pose.csv file
		def wait_for_path_ready():
			
			"""thread worker function"""
			data = rospy.wait_for_message('/clicked_point', PointStamped)
			rospy.loginfo('Recieved path READY message')
			print("waypoints b4")
			print(self.waypoints)
			self.path_ready = True
#			rospy.loginfo('Begin save')
			self.write_waypoints_csv()
			rospy.loginfo('*********************** Back from save ***********************')
		ready_thread = threading.Thread(target=wait_for_path_ready)
		ready_thread.start()

		# Receive data from RVIZ
		self.topic = self.addpose_topic
		rospy.loginfo(
			"Waiting to receive waypoints via Pose msg on topic %s" % self.topic)
		rospy.loginfo(
			"To stop recording , Publish a poin in RVIZ ( topic /clicked_point ) ")
		

		# Wait for published waypoints or saved path  loaded
		while (not self.path_ready):
			try:
				pose = rospy.wait_for_message(
					self.topic, PoseWithCovarianceStamped, timeout=1)
			except rospy.ROSException as e:
				if 'timeout exceeded' in e.message:
					continue  # no new waypoint within timeout, looping...
				else:
					raise e
			rospy.loginfo("Recieved new waypoint")
			self.waypoints.append(self.changePose(pose, "map"))
			# publish waypoint queue as pose array so that you can see them in rviz, etc.
			self.display_waypoints_in_rviz()

		# Path is ready! return success and move on to the next state (FOLLOW_PATH)
		return 

def main():
	rospy.init_node('waypoints_list_tool')
	path_manager=Mngt_path()
#	path_manager.print_menu()
#	path_manager.receive_poses_from_rviz()
#	path_manager.drive_path()
	menu_choice="0"

	
	while True:
		path_manager.print_menu()
		menu_choice=raw_input("Enter menu choice : ")
		if menu_choice=="1":
			path_manager.receive_poses_from_rviz()
		if menu_choice=="2":		
			path_manager.Read_Waypoints_csv()
		if menu_choice=="3":
			print("Manage list in construction")
		if menu_choice=="4":
			print("Aling in construction")
		if menu_choice=="5":
			path_manager.drive_path()
		if menu_choice=="6":
			path_manager.drive_path()
		if menu_choice=="7":
			path_manager.write_waypoints_csv()
		if menu_choice=="8":
			break # stop node		

