import os
import xacro

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    easybot_package = get_package_share_directory('easybot_description')
    gz_package = get_package_share_directory('ros_gz_sim')

    robot_description_file = os.path.join(easybot_package, 'urdf', 'gzbot.urdf')
    robot_description_config = xacro.process_file(
        robot_description_file
    )
    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare('easybot_description'),
            'config',
            'easybot_controller_position.yaml',
        ]
    )

    robot_description = {'robot_description': robot_description_config.toxml()}

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[robot_description],
        #parameters=[robot_description,{'use_sim_time':True}],
    )

    # Gazebo Harmonic Launch
    gazebo = IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(gz_package, 'launch', 'gz_sim.launch.py')),launch_arguments={'gz_args': '-r empty.sdf','use_sim_time':'True'}.items(),)

    # Spawn Robot in Gazebo
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        parameters=[{'name': 'easybot_description',
                    'topic': 'robot_description',
                    'use_sim_time':True}],
        output='screen',
    )
    
    #Joint State Broadcaster
    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        parameters=[{'use_sim_time':True}] 
    )
    
    #Controller Spawner with Controller Manager
    controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'easybot_controller',
            '--param-file',
            robot_controllers,
            ],
        parameters=[{'use_sim_time':True}]
    )
    
    # Gazebo Harmonic - ROS2 Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Clock (IGN -> ROS2)
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            # Joint states (IGN -> ROS2)
            '/world/empty/model/easybot/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
        ],
        remappings=[
            ('/world/empty/model/easybot/joint_state', 'joint_states'),
        ],
        parameters=[{'use_sim_time':True}],
        output='screen'
    )

    return LaunchDescription([robot_state_publisher,gazebo,spawn,bridge,joint_state_broadcaster,controller])

