from numpy import source
import rospy
import roslaunch
from service.srv import MapServer, MapServerResponse

command = ''
uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)
launch_map_create = roslaunch.parent.ROSLaunchParent(uuid, ["/home/fdata/ros/src/map/launch/map_create.launch"])
launch_map_save = roslaunch.parent.ROSLaunchParent(uuid, ["/home/fdata/ros/src/map/launch/map_save.launch"])
launch_map_load = roslaunch.parent.ROSLaunchParent(uuid, ["/home/fdata/ros/src/map/launch/map_load.launch"])

def map_function(req):
    global command 
    print("Returning request:%s"%(req.map_controller))
    if req.map_controller == 'map_create':
        command = 'map_create'
        print("command:%s"%(command))
        return MapServerResponse('map create')
    elif req.map_controller == 'map_save':
        command = 'map_save'
        print("command:%s"%(command))
        return MapServerResponse('map_save')
    elif req.map_controller  == 'map_load':
        command = 'map_load'
        return MapServerResponse('map_load')
    elif req.map_controller == "map_end":
        command = "map_end"
        return MapServerResponse('map_end') 
    elif req.map_controller == "map_off":
        command = "map_off"
        return MapServerResponse('map_off') 
    

def map_server():
    global command
    global launch_map_create
    global launch_map_save
    global launch_map_load
    rospy.init_node('map_server')
    server = rospy.Service('map_server', MapServer, map_function)
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
        elif command == "map_end":
            print("callback server:map_end")
            launch_map_create.shutdown()
            command = ""
        elif command == "map_off":
            return  
    rospy.spin()
    

if __name__ == "__main__":
    try:
        map_server()
    except rospy.ROSException:
        pass