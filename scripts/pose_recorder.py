#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that listens to std_msgs/Strings published
## to the 'chatter' topic

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from cmvision.msg import Blobs
from cmvision_3d.msg import Blobs3d, Blob3d


from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import cv2
import pyrealsense2 as rs





class ImageListener:
    def __init__(self, topic):
        self.topic = topic
        self.bridge = CvBridge()
        self.sub = rospy.Subscriber(topic, Blobs3d, self.imageDepthCallback)

        self.map_size=1000
        self.range=5
        self.height=2
        self.calibration_color="red"

    def imageDepthCallback(self, data):

        try:

            world_pose=input("please input pose:(x,y,z)")


            if len(world_pose)<3:
                return
            x_w = float(world_pose[0])
            y_w = float(world_pose[1])
            z_w = float(world_pose[2])
            print(x_w,y_w,z_w)
            for blob in data.blobs:
                if not blob.name==self.calibration_color:
                    continue
                x_c,y_c,z_c = blob.center.x,blob.center.y,blob.center.z
                with open("pose_record.csv","a") as pose_file:
                    saved_str=str([x_w,y_w,z_w,x_c,y_c,z_c]).strip("[").strip("]")
                    print(saved_str)
                    pose_file.write(saved_str+"\n")

                return

        except:

            return


if __name__ == '__main__':


    rospy.init_node("pose_recorder")
    topic = '/blobs_3d'
    listener = ImageListener(topic)
    rospy.spin()
