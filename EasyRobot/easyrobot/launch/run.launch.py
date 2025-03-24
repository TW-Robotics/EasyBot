from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
def generate_launch_description():

    #Nicht die Vollständige Movegroup launchen! Nodes werden doppelt geladen
    move_group = IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('moveit_easyrobot'),'launch','move_group.launch.py'])]))
    robot = IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('easyrobot'),'launch','gz.launch.py'])]))
    
    
    
    
    return LaunchDescription([robot,move_group])
