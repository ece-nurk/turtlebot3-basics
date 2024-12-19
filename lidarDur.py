#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from basit_uygulamalar.msg import lidar
from geometry_msgs.msg import Twist

def lidarDur(data):

    minMesafe = min(data.ranges)  
    rospy.loginfo("Engel uzaklığı: %f", minMesafe)    
    durulacakMesafe = 1.0

    lidar_msg = lidar()

    lidar_msg.minMesafe = minMesafe

    if minMesafe < durulacakMesafe: # Engel var 
        lidar_msg.hiz = 0.0
        lidar_msg.fren = 3.0

    else: # Engel yok 
        lidar_msg.hiz = 0.2 
        lidar_msg.fren = 0.0
    
    lidar_pub.publish(lidar_msg)
    
    # hareket komutları 
    twist = Twist()
    twist.linear.x = lidar_msg.hiz
    twist.angular.z = 0.0
    cmd_vel_pub.publish(twist)

def listener():

    rospy.init_node('lidarNode', anonymous=True)

    #publishers
    global lidar_pub
    lidar_pub = rospy.Publisher('lidar', lidar, queue_size=10)

    global cmd_vel_pub
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    #subscribers
    rospy.Subscriber('/scan', LaserScan, lidarDur)
    
    rospy.spin() # spin() fonksiyonu programın kapanmasını engelliyor 

if __name__ == '__main__':
    listener()
