#!/usr/bin/env python
#encoding: utf-8

import unittest, rostest
import rosnode, rospy
import time
from geometry_msgs.msg import Twist
from pimouse_ros.msg import LightSensorValues

class WallStopAccelTest(unittest.TestCase):
    def set_and_get(self, lf, ls, rs, rf):
        with open("/dev/rtlightsensor0", "w") as f:
            f.write("%d %d %d %d\n" % (rf, rs, ls, lf))

            time.sleep(0.3)

        with open("/dev/rtmotor_raw_l0","r") as lf,\
             open("/dev/rtmotor_raw_r0","r") as rf:

            left = int(lf.readline().rstrip())
            right= int(rf.readline().rstrip())

        return left, right

    def test_io(self):
        left, right = self.set_and_get(400,100,100,0) #total : 600
        self.assertTrue( left == right==0, "can't stop")

        left, right = self.set_and_get(10,10,10,10) #total:40
        self.assertTrue( 0 < left == right <1000, "can't move again")

        time.sleep(5.0)

        left, right = self.set_and_get(15,10,10,15) #total:50
        self.assertTrue( left == right==0, "can't stop")

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('travis_test_wall_stop_accel')
    rostest.rosrun('pimouse_run_corridor','travis_test_wall_accel', WallStopAccelTest)
 
