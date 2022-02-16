import rospy
import roslaunch
from service.srv import MapServer, MapServerResponse

command = ''
uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)
launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/fdata/ros/src/model/launch/robot.launch"])

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
        return MapServerResponse('map_load')
    

def map_server():
    global launch
    global command
    rospy.init_node('map_server')
    server = rospy.Service('map_server', MapServer, map_function)
    print("callback server:%s"%(server))
    print("Ready to start map server.")
    while(1):
        print("command:%s"%(command))
        if command == 'map_create':
            print("callback server:map_create")
            launch.start()
            command = ''
        elif command == 'map_save':
            print("callback servermap_save")
            launch.shutdown()
            command = ''
            break
    rospy.spin()
    

if __name__ == "__main__":
    try:
        map_server()
    except rospy.ROSException:
        pass