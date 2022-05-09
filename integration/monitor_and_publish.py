#!/usr/bin/env python

import paho.mqtt.client as mqtt
import rospy
from std_msgs.msg import String
from actionlib_msgs.msg import GoalStatusArray
import time

status_dict = {
    -1: "NOT_STARTED",
    0: "PENDING",
    1: "ACTIVE",
    2: "PREEMPTED",
    3: "SUCCEEDED",
    4: "ABORTED",
    5: "REJECTED",
    6: "PREEMPTING",
    7: "RECALLING",
    8: "RECALLED",
    9: "LOST",
}

def publish_mqtt(msg):
    mqtt_client.publish(mqtt_topic, msg)

class PubSub:

    def __init__(self):
        
        self.nav_status = -1
        self.goal_id = -1
        self.msg = "Building the map. Sending 0."
        self.counter = 0

    def reader_callback(self, data):

        status_list = data.status_list
        try:
            self.goal_id = status_list[0].status
            self.msg = str(self.goal_id)
            self.msg = "Goal Status: {}".format(self.goal_id)
        except AttributeError:
            self.goal_id = -1
            self.msg = "Attr {}".format(self.counter)
            self.counter += 1
        # self.msg = "Goal Status: {}".format(status_dict[self.goal_id])
        if self.nav_status != 3 and self.goal_id == 3:
            # Send status via mqtt
            self.msg = "Changed status from {} to SUCCEEDED. Sending 1.".format(status_dict[self.nav_status])
            self.nav_status = 3
            publish_mqtt("1")
        elif self.nav_status == 3 and self.goal_id != 3:
            self.msg = "Changed status from {} to {}. Sending 0.".format(status_dict[self.nav_status], status_dict[self.goal_id])
            self.nav_status = self.goal_id
            # Send zero via mqtt
            publish_mqtt("0")
        elif self.nav_status == 3 and self.goal_id == 3:
            # Send 1 via mqtt
            self.msg = "Status still SUCCEEDED. Sending 1."
            publish_mqtt("1")
        else:
            # Send 0 via mqtt
            publish_mqtt("0")
            if self.nav_status != self.goal_id:
                self.msg = "Changed status from {} to {}. Sending 0.".format(status_dict[self.nav_status], status_dict[self.goal_id])
            else:
                self.msg = "Status did not change from {}. Sending 0.".format(status_dict[self.goal_id])

mqttBroker ="10.155.61.43" 
mqtt_topic = "arm_safe_to_move_ugv"
mqtt_client = mqtt.Client("UGV_SLAM")
mqtt_client.connect(mqttBroker)

# ROS subscribers
nav_reader_node = "arm_safe_to_move_sub"
nav_status_topic = "/move_base/status"
nav_pub_status_topic = "/ugv_save_to_move"

pub_handler = PubSub()

rospy.init_node(nav_reader_node, anonymous=True)
rate = rospy.Rate(10) # 10hz
sub = rospy.Subscriber(nav_status_topic, GoalStatusArray, pub_handler.reader_callback)


while not rospy.is_shutdown():
    print(str(pub_handler.msg))
    safe_status = "1" if pub_handler.nav_status == 3 else "0"

