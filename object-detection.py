#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import Twist
import numpy as np

bridge = CvBridge()
hizPub = None
nesneMerkez = None
mesafe = None
hedefe_ulaşıldı = False  # flag

def kamera_callback(mesaj):
    global nesneMerkez
    img = bridge.imgmsg_to_cv2(mesaj, "bgr8")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    kirmiziAlt = np.array([0, 120, 70])
    kirmiziUst = np.array([10, 255, 255])
    maske = cv2.inRange(hsv, kirmiziAlt, kirmiziUst)
    
    sinirlar, _ = cv2.findContours(maske, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    if sinirlar:
        cnt = max(sinirlar, key=cv2.contourArea)
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            nesneMerkez = (cx, cy)
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)
        else:
            nesneMerkez = None
    else:
        nesneMerkez = None

    cv2.imshow("Kamera", img)
    cv2.waitKey(1)

def lidar_callback(veri):
    global mesafe, hedefe_ulaşıldı
    if not hedefe_ulaşıldı:  
        geçerli_mesafeler = [m for m in veri.ranges if not np.isnan(m)]
        if geçerli_mesafeler:
            mesafe = float(min(geçerli_mesafeler))
        else:
            mesafe = None

def hareket():
    global nesneMerkez, mesafe, hedefe_ulaşıldı
    twist = Twist()
    
    if hedefe_ulaşıldı:
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        rospy.loginfo("Nesnenin merkezine geldi ve durdu")
    elif nesneMerkez is None:
        twist.linear.x = 0.0
        twist.angular.z = 0.3
        rospy.loginfo("Kırmızı nesne aranıyor")
    else:
        merkez_x = 320  
        cx = nesneMerkez[0]
        fark = cx - merkez_x

        if mesafe is not None and mesafe < 2:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            hedefe_ulaşıldı = True
            rospy.loginfo("Nesnenin merkezine geldi ve durdu")
        else:
            twist.linear.x = 0.5
            twist.angular.z = -0.005 * fark #ortalıyor
            rospy.loginfo(f"nesneye uzaklık: {mesafe}")
    
    hizPub.publish(twist)

if __name__ == '__main__':
    rospy.init_node("kamera_node")
    
    hizPub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
    rospy.Subscriber("camera/rgb/image_raw", Image, kamera_callback)
    rospy.Subscriber("scan", LaserScan, lidar_callback)
    
    rate = rospy.Rate(10)  
    while not rospy.is_shutdown():
        hareket()
        rate.sleep()

    cv2.destroyAllWindows()
