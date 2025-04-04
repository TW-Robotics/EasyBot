from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
#from launch.actions import 
#from launch_ros.actions import Node

###Testing###
#move_group = #IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('moveit_easyrobot'),'launch','move_group.launch.py'])]),launch_arguments=[("use_si##m_time", "True")])
#    #move_group = IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('moveit_easyrobot'),'launch','move_group.launch.py'])]), ##launch_arguments={'use_sim_time': 'true'}.items())
#    
#    #set_sim_time = SetParameters([("/move_group", {"use_sim_time": True})])
#    
#    sim_time = DeclareLaunchArgument(
#        'use_sim_time', 
#        default_value='true', 
#        description='Parameter for Sim Time'
#    ) Testing


###Launch file starts here###

def generate_launch_description():
    
    move_group = IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('moveit_easyrobot'), 'launch','move_group_edit.launch.py'])]))    
    launch_rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('moveit_easyrobot'),'launch','moveit_rviz_edit.launch.py'])]))
    robot = IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('easyrobot'),'launch','gz.launch.py'])]))
    
    return LaunchDescription([robot,launch_rviz,move_group])
