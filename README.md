# clinic_delivery_robot
This repository is for TTTC2343 Project

This repository was an editted repository to make it fits our needs.
The original repository is build by rodriguesrenato, and the link is
https://github.com/rodriguesrenato/warehouse_robot_simulation?tab=readme-ov-file

For this project we changed some items from the original repository. Some of the changes include:
1. Created a new map to satisfy our environment, which is a clinic environment
2. Changed the coordinates for the models to fit into our simulation world
3. Added more 'dispatch' models, and placed them in each room in the world

This project was done with the respective spec:
- Ubuntu 20.04.6
- ROS Noetic

# Installation
Before running the simulation, we first need to install the depencies needed for the system (This process is similar to the one from the original repository)

Assuming the workspace is /catkin_ws,  
To clone the repository, we use the command:
```
cd ~/catkin_ws/src && git clone https://github.com/AizadHaiqalSaw/clinic_delivery_robot.git
```
To do mapping, we also need:
```
git clone https://github.com/ros-perception/slam_gmapping.git
```
and
```
git clone https://github.com/ros-teleop/teleop_twist_keyboard
```

Required dependencies:
```
sudo apt-get install ros-noetic-amcl
sudo apt-get install ros-noetic-move-base
sudo apt-get install ros-noetic-dwa-local-planner
sudo apt-get install ros-noetic-map-server
sudo apt-get install ros-noetic-teleop-twist-keyboard 
sudo apt-get install ros-noetic-gmapping
sudo apt-get install ros-noetic-slam-gmapping
```

***IMPORTANT***
Before building the workspace, please move the '    warehouse_robot_simulation    ' file from the GitHub cloned file '*clinic_delivery_robot*' into '*catkin_ws/src*' (or the workspace currently used)

After cloning and installing everything, we would need to build and source it:
```
cd ~/catkin_ws && catkin_make
source devel/setup.bash
```
This repository also relies on Xterm for the execution of the project.  
To install Xterm, use:
```
sudo apt-get install xterm
```
And finally we would need to make the scripts executable:
```
cd ~/catkin_ws/src/warehouse_robot_simulation/scripts && chmod +x *.sh
```


# Simulation

To simualate the project world, we use a script, and the command to use this scripts is as below:
```
cd ~/catkin_ws/src/warehouse_robot_simulation/scripts && ./clinic_simulation.sh
```
Using this script, it also place the robot in the world, and launch RVis to visualize the robot's sensors.  
If the included map is unsatisfactory, use this command to map a new map:
```
cd ~/catkin_ws/src/warehouse_robot_simulation/scripts && ./clinic_mapping_slam.sh
```
This script launches the map and the robot, and also teleOp to control the robot during mapping.  
After finished mapping the world, use this command to save the map:
```
rosrun map_server map_saver -f clinic.
```


After launching the world, and robot, we can use the command in a new terminal:
```
roslaunch warehouse_robot_simulation clinic_simulation.launch
```

This command places the 'dispatch' and 'storage' that would be used in the delivery simulation.  
The delivery system works using order. User can send order by sending a message to a topic.  
The format for sending the message is as below:
```
rostopic pub /warehouse/order/add std_msgs/String "data: '<Dispatch_name> <Product_name> <Quantity>'"
```
The <Product_name> and <Quantity> can be duplicated if the dispatch would request for more products.
    For example:
```
rostopic pub /warehouse/order/add std_msgs/String "data: 'Dispatch1 ProductR 2 ProductG 3'"
```
This command shows that the robot would get 2 ProductR and 3 ProductG, and sends them to Dispatch1.



Other than that, we also added a program that allows the user to input a room's name, and the robot would move to the location.  
To trigger the program, first we launch the world and robot using the same script as above:
```
cd ~/catkin_ws/src/warehouse_robot_simulation/scripts && ./clinic_simulation.sh
```
Then, in a new terminal, we enter command:
```
rosrun warehouse_robot_simulation clinic_send_goal.py
```
Using this command, in the same terminal, user can enter a room name that the robot would move to, if the user forgot the rooms name, user can enter 'list' which would list out all the available rooms.  
This program would keep on running until user use the button combination 'CTRL+C', then 'ENTER' to exit the program.
