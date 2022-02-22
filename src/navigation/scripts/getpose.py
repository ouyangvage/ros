import rospy
import tf
import time

if __name__ == '__main__':
    rospy.init_node('robot_tf_listener')
    listener = tf.TransformListener() #start listener
    while not rospy.is_shutdown():
        try:
            #获取 base_footprint 相对 map 的坐标变换，返回两个列表
            (position, orient) = listener.lookupTransform('map', 'base_footprint', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        print('position', position)
        print('orient', orient)
        time.sleep(0.5)