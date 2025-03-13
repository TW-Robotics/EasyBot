import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
 
 
def generate_launch_description():
    # Get the path to the URDF file
    urdf_file_name = 'gzbot.urdf'
    # Use LaunchConfiguration to allow override via command line
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    # Change this to your actual package name that contains the URDF
    package_name = 'easyrobot'

    urdf_file = os.path.join(
    get_package_share_directory(package_name),
    'urdf',
    urdf_file_name)

    # Create a robot_state_publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': Command(['xacro ', urdf_file]) if urdf_file.endswith('.xacro') 
                                else Command(['cat ', urdf_file])
       }]
    ) 
    # Create a joint_state_publisher node
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time
       }]
    )
    # Add the GUI for controlling joints if there are movable joints in your URDF
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    # Create an RViz configuration file
    rviz_config_file = os.path.join(get_package_share_directory('easyrobot'),'config','easyrobot.rviz')
    # Create an RViz node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file] ,
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    # Create the launch description and populate
    ld = LaunchDescription()
    # Declare the launch options
    ld.add_action(DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='easyrobot'))
    # Add nodes to launch description
    ld.add_action(robot_state_publisher_node)
    #ld.add_action(joint_state_publisher_node)
    ld.add_action(joint_state_publisher_gui_node)
    ld.add_action(rviz_node)
    return ld
