#include <iostream>
#include "cmd_interface_linux.h"
#include <stdio.h>
#include "lipkg.h"
#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include "tofbf.h"
#include <string>

#define RADIAN_TO_ANGLED(angle) ((angle)*180000/3141.59)

int main(int argc , char **argv)
{
	ros::init(argc, argv, "product");
	ros::NodeHandle nh;                    /* create a ROS Node */

	LiPkg * lidar = new LiPkg;
  
    CmdInterfaceLinux cmd_port;
	std::string port_name;

	/*
    std::vector<std::pair<std::string, std::string> > device_list;
    
    cmd_port.GetCmdDevices(device_list);
    for (auto n : device_list)
    {
        std::cout << n.first << "    " << n.second << std::endl;
        if(strstr(n.second.c_str(),"CP2102"))
        {
            port_name = n.first;
        }
    }

	if(port_name.empty())
	{
		std::cout<<"Can't find LiDAR LD06"<< std::endl;
	}
	*/

	//编译报错安装 sudo apt-get install libudev-dev
	//etc/udev/rules.d/下的规则文件中命名
	port_name = "/dev/ttyUSB1"; //RK板固定串口名
	
	std::cout<<"LiDAR port:/dev/ttyUSB1"  <<std::endl;
	std::cout<<"FOUND LiDAR_LD06"  <<std::endl;
	cmd_port.SetReadCallback([&lidar](const char *byte, size_t len) {
		if(lidar->Parse((uint8_t*)byte, len))
		{
			lidar->AssemblePacket();  
		}
	});
	

	if(cmd_port.Open(port_name)){
		std::cout<<"LiDAR_LD06 started successfully "  <<std::endl;
	}
		
	ros::Publisher lidar_pub = nh.advertise<sensor_msgs::LaserScan>("LiDAR/LD06", 1); /*create a ROS topic */

	while (ros::ok())
	{
		if (lidar->IsFrameReady())
		{
			lidar_pub.publish(lidar->GetLaserScan());  // Fixed Frame:  lidar_frame
			lidar->ResetFrameReady();
#if 0 
			sensor_msgs::LaserScan data = lidar->GetLaserScan();
			unsigned int lens = (data.angle_max - data.angle_min) / data.angle_increment;  
			std::cout << "current_speed: " << lidar->GetSpeed() << " " 
			          << "len: " << lens << " "
					  << "angle_min: " << RADIAN_TO_ANGLED(data.angle_min) << " "
					  << "angle_max: " << RADIAN_TO_ANGLED(data.angle_max) << std::endl; 
			std::cout << "----------------------------" << std::endl;
			for (int i = 0; i < lens; i++)
			{
				std::cout << "range: " <<  data.ranges[i] << " " 
						  << "intensites: " <<  data.intensities[i] << std::endl;
			}
			std::cout << "----------------------------" << std::endl;
#endif
		}
	}
    return 0;
}
