#!/usr/bin/env python

from dis import dis
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
from math import sqrt
import time
import numpy
import paho.mqtt.client as mqtt 
import time
from random import randrange, uniform


## inputs
target_x = 0.0  # m
target_y = 0.0  # m
target_theta = 0.0  # degree

count = 0
x = 0.0
y = 0.0 
theta = 0.0

received_status = 0



def on_message(client, userdata, message):
    '''This function's primary purpose is to get the message sent
       by the client and parse it so it can be used in the movement 
       of the robot'''

    global target_x
    global target_y
    global target_theta
    global received_status

    print("Received data")
    received_data = str(message.payload.decode("utf-8"))
    print("Data Recieved: ", received_data)
    parsed_string = received_data.split(",")
    print(len(parsed_string))
    target_x = float(parsed_string[0])
    target_y = float(parsed_string[1])
    target_theta = float(parsed_string[2])
    
    received_status = 1


def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("speed_controller")

sub = rospy.Subscriber("/odometry/filtered", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

speed = Twist()

r = rospy.Rate(4)

goal = Point()



mqttBroker ="broker.hivemq.com" 
topic = "movement_without_nav" 

client = mqtt.Client("UGV_Lidar")
client.on_message=on_message

client.connect(mqttBroker) 


message = "0"
client.publish(topic, message)
print("Just published: " + message)


client.loop_start()
client.subscribe(topic)
# time.sleep(10) # wait
while received_status == 0:
    time.sleep(0.1)

client.loop_stop() #stop the loop
print(target_y)
print("newline", target_x)
angle_to_goal = atan2(abs(target_y), abs(target_x))
#angle_to_goal = abs(angle_to_goal)
#print("first", angle_to_goal*180/3.14)
while count == 0:
	if target_x > 0 and target_y > 0:
		angle_to_goal = angle_to_goal*180/3.14
	elif target_x < 0 and target_y > 0:
		angle_to_goal = 180 - angle_to_goal*180/3.14
                print("WTF ", angle_to_goal)
	elif target_x < 0 and target_y < 0:
		angle_to_goal = 180 + angle_to_goal*180/3.14
	elif target_x > 0 and target_y < 0:
		angle_to_goal = 360 - angle_to_goal*180/3.14
	elif target_x == 0 and target_y > 0:
		angle_to_goal = 90
	elif target_x == 0 and target_y < 0:
		angle_to_goal = 270
	count += 1


#print("This is the angle to goal.: ", angle_to_goal)
angle_to_goal = angle_to_goal * 3.14/180

adjusted_theta = 0

if theta >= 0:
    adjusted_theta = theta
elif theta < 0:
    adjusted_theta = 6.283 - abs(theta)

if angle_to_goal >= 3.1415: 
    angle_to_goal_effective = 6.283 - angle_to_goal
    vel = -0.1
elif angle_to_goal < 3.1415:
    angle_to_goal_effective = angle_to_goal
    vel = 0.1
    
print("Angle Theta: ", angle_to_goal_effective)

curr_time_ang = time.time()
c = 0
while abs(angle_to_goal - adjusted_theta) > 0.0807:  # tolerance = 0.0807 rad = 5 degree
    #print("This is the theta",angle_to_goal - theta)
    if c == 0:
	init_time_ang = time.time()
	c = 1
	continue
    time_diff_ang = curr_time_ang-init_time_ang
    print(angle_to_goal)
    if(time_diff_ang >= angle_to_goal_effective/0.1):
	print(time_diff_ang)
	break
    print("Time diff: ", time_diff_ang)
    print(vel)
    speed.angular.z = vel
    speed.linear.x = 0
    curr_time_ang = time.time()
    r.sleep()
    pub.publish(speed)

# NOW THE ROTATION IS DONE 
# IT IS THE TIME FOR TRANSLATION

curr_time_line = time.time()
dist_to_goal = sqrt((target_x)**2 + (target_y)**2)
print(dist_to_goal)
c = 0
while True:
    if c == 0:
	init_time_line = time.time()
	c=1
	continue
    time_diff_line = curr_time_line - init_time_line
    if (time_diff_line >= dist_to_goal/0.1):
	print(time_diff_line)
	break
    print("Linear movement: ", time_diff_line)
    speed.angular.z = 0.0
    speed.linear.x = 0.1
    curr_time_line = time.time()
    pub.publish(speed)
    r.sleep()

print("almost done")
# WE HAVE REACHED THE DESTINATION
# JUST NEED TO ADJUST THE ORIENTATION

while abs(theta - target_theta) < 0.0807:  # tolerance = 0.087 rad = 5 degree
    speed.linear.x = 0.0
    speed.angular.z = 0.1
    r.sleep()



message = "1"
client.publish(topic, message)
print("Just published: " + message)
