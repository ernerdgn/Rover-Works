#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2

def callback(data):

    shift_begin = 912	# this value is between 0 to 1024

    data_arr = []
    temp = []

    for i in range(16):  # height = 16
        temp = data.data[i*48*1024: i*48*1024+1024*48]  #width = 1024, point_step = 48
        temp += temp[:512*48]
        data_arr += temp[shift_begin*48 : shift_begin*48 + 512*48]  # bounding the PointCloud2 data

    data.header.frame_id = "map"  # instead of "os_sensor", with this change you can observe data with RViz in desired frame id.

    publisher = rospy.Publisher('modified_PointCloud2', PointCloud2, queue_size=10)

    publisher.publish(data.header, data.height, data.width//2,
                        data.fields, data.is_bigendian, data.point_step,
                        data.row_step//4, data_arr, data.is_dense)

def point_listener():
    rospy.init_node("listener", anonymous=True)
    
    rospy.Subscriber("os_cloud_node/points", PointCloud2, callback)

    rospy.spin()

if __name__ == "__main__":
    point_listener()
