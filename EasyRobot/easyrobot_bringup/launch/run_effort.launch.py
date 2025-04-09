from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution

def generate_launch_description():
    ###Move Group MoveIt###
    move_group = IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('moveit_easyrobot'), 'launch','move_group_edit.launch.py'])])) 
    
    ###RVIZ###
    launch_rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('moveit_easyrobot'),'launch','moveit_rviz_edit.launch.py'])]))
    
    ###Gazebo and Robot###
    robot = IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('easyrobot'),'launch','gz_effort.launch.py'])]))
    
    return LaunchDescription([robot,launch_rviz,move_group])
