import rospy
import tf
import time
from std_msgs.msg import String

if __name__ == '__main__':
    rospy.init_node('robot_tf_listener')
    listener = tf.TransformListener() #start listener
    pub = rospy.Publisher("/current_pose", String, queue_size=10)
    msg = String()
    while not rospy.is_shutdown():
        try:
            #获取 base_footprint 相对 map 的坐标变换，返回两个列表
            (position, orientation) = listener.lookupTransform('map', 'base_footprint', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        print('position', position)
        print('orientation', orientation)
        msg.data = '{"position":' + str(position) + ',' +  '"orientation"' + ':' + str(orientation) + '}'
        # msg.data = '{"position":[1,3,6], "orientation":[3,4,5,6]}'
        pub.publish(msg)
        time.sleep(0.5)