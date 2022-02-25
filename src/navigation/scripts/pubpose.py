import rospy
import time
from geometry_msgs.msg import PoseStamped

if __name__ == '__main__':
    rospy.init_node('publisher_pose')
    robot_pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=1)
    target_pose = PoseStamped() #first null point for try
    robot_pub.publish(target_pose)
    time.sleep(1)

    target_pose = PoseStamped()
    target_pose.header.frame_id = 'base_footprint'
    target_pose.pose.position.x = 1
    target_pose.pose.position.y = 0
    target_pose.pose.position.z = 0

    target_pose.pose.orientation.x = 0
    target_pose.pose.orientation.y = 0
    target_pose.pose.orientation.z = 1
    target_pose.pose.orientation.w = 0

    robot_pub.publish(target_pose)

    time.sleep(5)


