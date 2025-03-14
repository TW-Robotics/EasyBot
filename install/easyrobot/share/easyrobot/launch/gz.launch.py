import os
import xacro

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    easybot_package = get_package_share_directory('easyrobot')
    gz_package = get_package_share_directory('ros_gz_sim')

    robot_description_file = os.path.join(easybot_package, 'urdf', 'gzbot.urdf')
    robot_description_config = xacro.process_file(
        robot_description_file
    )
    robot_description = {'robot_description': robot_description_config.toxml()}

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[robot_description],
    )

    # Gazebo Sim
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_package, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    # RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(easybot_package, 'config', 'easyrobot.rviz')],
    )

    # Spawn
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        parameters=[{'name': 'easyrobot',
                    'topic': 'robot_description'}],
        output='screen',
    )

    # Gz - ROS Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Clock (IGN -> ROS2)
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            # Joint states (IGN -> ROS2)
            '/world/empty/model/easyrobot/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
        ],
        remappings=[
            ('/world/empty/model/easyrobot/joint_state', 'joint_states'),
        ],
        output='screen'
    )


    return LaunchDescription([robot_state_publisher,gazebo,rviz,spawn,bridge])

