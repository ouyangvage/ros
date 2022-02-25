import re
from numpy import source
import rospy
import roslaunch
from service.srv import RobotServer, RobotServerResponse
import time

command = ''
uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)
# launch_map_create = roslaunch.parent.ROSLaunchParent(uuid, ["/home/dhzhang/ros_ouyang/ros/src/map/launch/map_create.launch"])
# launch_map_save = roslaunch.parent.ROSLaunchParent(uuid, ["/home/dhzhang/ros_ouyang/ros/src/map/launch/map_save.launch"])
# launch_map_load = roslaunch.parent.ROSLaunchParent(uuid, ["/home/dhzhang/ros_ouyang/ros/src/map/launch/map_load.launch"])

launch_map_create = roslaunch.parent.ROSLaunchParent(uuid, ["/home/ubuntu/ros/src/map/launch/map_create.launch"])
launch_map_save = roslaunch.parent.ROSLaunchParent(uuid, ["/home/ubuntu/ros/src/map/launch/map_save.launch"])
launch_map_load = roslaunch.parent.ROSLaunchParent(uuid, ["/home/ubuntu/ros/src/map/launch/map_load.launch"])
launch_amcl = roslaunch.parent.ROSLaunchParent(uuid, ["/home/ubuntu/ros/src/navigation/launch/amcl.launch"])
launch_navigation = roslaunch.parent.ROSLaunchParent(uuid, ["/home/ubuntu/ros/src/navigation/launch/navigation.launch"])


def robot_function(req):
    global command 
    print("Returning request:%s"%(req.robot_controller))
    if req.robot_controller == 'map_create':
        command = 'map_create'
        print("command:%s"%(command))
        return RobotServerResponse('map create')
    elif req.robot_controller == 'map_save':
        command = 'map_save'
        print("command:%s"%(command))
        return RobotServerResponse('map_save')
    elif req.robot_controller  == 'map_load':
        command = 'map_load'
        return RobotServerResponse('map_load')
    elif req.robot_controller == "map_end":
        command = "map_end"
        return RobotServerResponse('server_end')
    elif req.robot_controller == 'navigation_start':
        command = "navigation_start" 
        return RobotServerResponse('navigation_start')
    elif req.robot_controller == 'navigation_end':
        command = 'navigation_end'
        return RobotServerResponse('navigation_end')
    elif req.robot_controller == 'amcl_start':
        command = 'amcl_start'
        return RobotServerResponse('amcl_start')
    elif req.robot_controller == 'amcl_end':
        command = 'amcl_end'
        return RobotServerResponse('amcl_end')
    elif req.robot_controller == "server_off":
        command = "server_off"
        return RobotServerResponse('server_off') 
    

def robot_server():
    global command
    global launch_map_create
    global launch_map_save
    global launch_map_load
    server = rospy.Service('robot_server', RobotServer, robot_function)
    print("callback server:%s"%(server))
    print("Ready to start map server.")
    while(1):
        if command == 'map_create':
            print("callback server:map_create")
            launch_map_create.start()
            command = ''
        elif command == 'map_save':
            print("callback servermap_save")
            launch_map_save.start()
            command = ''
        elif command == 'map_load':
            print("callback server:map_load")
            launch_map_load.start()
            command = ''
        elif command == 'map_end':
            print("callback server:map_end")
            launch_map_create.shutdown()
            command = ''
        elif command == 'navigation_start':
            print("callback server:navigation_start")
            launch_navigation.start()
            command = ''
        elif command == 'navigation_end':
            print("callback server:navigation_end")
            launch_navigation.shutdown()
            command = ''
        elif command == 'amcl_start':
            print("callback server:amcl_start")
            launch_amcl.start()
            command = ''
        elif command == 'navigation_end':
            print("callback server:amcl_end")
            launch_amcl.shutdown()
            command = ''
        elif command == "server_off":
            return  
        time.sleep(1)
    rospy.spin()
    

if __name__ == "__main__":
    try:
        rospy.init_node('robot_server')
        robot_server()
    except rospy.ROSException:
        pass
