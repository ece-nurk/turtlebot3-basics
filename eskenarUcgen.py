#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def eskenarUcgen():
    rospy.init_node('eskenarUcgenCiz', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    hiz_msg = Twist()

    kenarMesafe = 1.0
    hiz = 0.1  
    donusAci = 2 * 3.14159 / 3  
    donusHizi = 0.2  
    rospy.sleep(1) 

    # 1. Kenar
    rospy.loginfo("1. kenar")
    hiz_msg.linear.x = hiz
    hiz_msg.angular.z = 0.0
    pub.publish(hiz_msg)
    rospy.sleep(kenarMesafe / hiz)

    hiz_msg.angular.z = 0.0
    hiz_msg.linear.x = 0.0
    pub.publish(hiz_msg)
    rospy.sleep(1)

    # 1. Dönüş
    rospy.loginfo("1. dönüş")
    hiz_msg.angular.z = donusHizi
    pub.publish(hiz_msg)
    rospy.sleep(donusAci / donusHizi)

    hiz_msg.angular.x = 0.0
    hiz_msg.angular.z = 0.0
    pub.publish(hiz_msg)
    rospy.sleep(1)

    # 2. Kenar
    rospy.loginfo("2. kenar")
    hiz_msg.linear.x = hiz
    hiz_msg.angular.z = 0.0
    pub.publish(hiz_msg)
    rospy.sleep(kenarMesafe / hiz)

    hiz_msg.angular.z = 0.0
    hiz_msg.linear.x = 0.0
    pub.publish(hiz_msg)
    rospy.sleep(1)

    # 2. Dönüş
    rospy.loginfo("2. dönüş")
    hiz_msg.angular.z = donusHizi
    pub.publish(hiz_msg)
    rospy.sleep(donusAci / donusHizi)
    hiz_msg.angular.z = 0.0

    hiz_msg.angular.z = 0.0
    pub.publish(hiz_msg)
    rospy.sleep(1)

    # 3. Kenar
    rospy.loginfo("3. kenar")
    hiz_msg.linear.x = hiz
    pub.publish(hiz_msg)
    rospy.sleep(kenarMesafe / hiz)

    hiz_msg.linear.x = 0.0
    pub.publish(hiz_msg)
    rospy.sleep(1)

    rospy.loginfo("Eşkenar üçgen tamamlandı!")

    hiz_msg.linear.x = 0.0
    hiz_msg.angular.z = 0.0
    pub.publish(hiz_msg)

if __name__ == '__main__':
    try:
        eskenarUcgen()
    except rospy.ROSInterruptException:
        pass
