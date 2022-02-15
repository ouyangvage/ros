import rospy
import roslaunch

# def startlaunch():
#     uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
#     roslaunch.configure_logging(uuid)
#     tracking_launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/fdata/ros/src/model/launch/robot.launch"])
#     tracking_launch.start()
#     while not rospy.is_shutdown():
#         tracking_launch.shutdown()
    

if __name__ == "__main__":
    try:
        rospy.init_node('en_Mapping', anonymous=True)
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/fdata/ros/src/model/launch/robot.launch"])
        launch.start()
        rospy.loginfo("started")
        while not rospy.is_shutdown():
            pass
    except rospy.ROSException:
        pass