# EasyBot
This is the Repo of the Easybot (ROS Jazzy) with a MoveIt2 Config and Gazebo Harmonic
## Usage
1. Do the git clone below (in ros2_ws/src):
```
git clone https://github.com/TW-Robotics/EasyBot.git
```
2. Build your Workspace with (in ros2_ws): 
```
colcon build
```
3. Source you Install directory with (assuming ros2_ws is in your home and you are using bash):
```
source ~/ros2_ws/install/setup.bash
```

![easyrobot](EasyRobot/easyrobot/misc/easyrobot_rviz.png "easyrobot in rviz")

## Launching the EasyBot in Gazebo with MoveIt Control
```
ros2 launch easyrobot_bringup run.launch.py
```
This launches a Gazebo Empty World with the EasyBot spawned 0.5 meters clear of the ground plane

## Issues
* Default Planner has to be choosen in RViz (Context --> OMPL --> Planner Dropdown --> choose RRTConnect)

## To-Do
* DH-Convention for EasyRobot
* ~~MoveIt branch with Moveit Configuration~~
* Different Controllers (velocity and effort planned)
* Adding different OMPL Planners for testing
