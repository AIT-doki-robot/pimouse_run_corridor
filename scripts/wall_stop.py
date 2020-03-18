#!/usr/bin/env python
#encoding: utf-8

import rospy, copy
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.msg import LightSensorValues

class WallStop():
    def __init__(self): #constractor
        self.cmd_vel = rospy.Publisher('/cmd_vel',Twist, queue_size=1)
        #create instance for publisher

        self.sensor_values = LightSensorValues()
        #create instance for sensor value

        rospy.Subscriber('/lightsensors',LightSensorValues, self.callback)
        #if data is updated, execute callback function

    def callback(self,messages):
        self.sensor_values = messages
        #input the sensor values by subscriber to sensor_values

    def run(self):
        rate = rospy.Rate(10)
        data = Twist()

        while not rospy.is_shutdown():
            
            data.linear.x = 0.2 if self.sensor_values.sum_all < 500 else 0.0
            # set velocity
            self.cmd_vel.publish(data)
            # send the data
            rate.sleep()
            #sleep until the next step

if __name__ == '__main__':

    rospy.init_node('wall_stop') #node initialization
    rospy.wait_for_service('motor_on') # wait until service is available
    rospy.wait_for_service('motor_off')

    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    #Register function to be called on shutdown
    #Only registration at shutdown

    rospy.ServiceProxy('/motor_on', Trigger).call() # Motor switch ON
    WallStop().run() # execute WallStop()
     
    
