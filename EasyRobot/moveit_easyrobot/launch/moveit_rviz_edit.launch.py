#!/usr/bin/env python3

import os
import xacro
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    
    rviz_config = os.path.join(
        get_package_share_directory("moveit_easyrobot"),
        "config",
        "moveit.rviz"
    )

    # Robot description
    robot_description_config = xacro.process_file(
        os.path.join(
            get_package_share_directory("easyrobot"),
            "urdf",
            "gzbot.urdf",
        )
    )
    robot_description = {"robot_description": robot_description_config.toxml()}

    # SRDF
    robot_description_semantic_path = os.path.join(
        get_package_share_directory("moveit_easyrobot"),
        "config",
        "easyrobot.srdf",
    )
    with open(robot_description_semantic_path, "r") as file:
        robot_description_semantic_config = file.read()

    robot_description_semantic = {"robot_description_semantic": robot_description_semantic_config}

    # OMPL 
    ompl_planning_pipeline_config = {
        "move_group": {
            "planning_plugins": ["ompl_interface/OMPLPlanner"],
            "request_adapters": [
                "default_planning_request_adapters/ResolveConstraintFrames",
                "default_planning_request_adapters/ValidateWorkspaceBounds",
                "default_planning_request_adapters/CheckStartStateBounds",
                "default_planning_request_adapters/CheckStartStateCollision",
            ],
            "response_adapters": [
                "default_planning_response_adapters/AddTimeOptimalParameterization",
                "default_planning_response_adapters/ValidateSolution",
                "default_planning_response_adapters/DisplayMotionPath",
            ],
            "start_state_max_bounds_error": 0.1,
            
        }
    }
    ompl_planning_yaml_path = os.path.join(
        get_package_share_directory("moveit_easyrobot"),
        "config",
        "ompl_planning.yaml",
    )
    with open(ompl_planning_yaml_path, "r") as file:
        ompl_planning_yaml = yaml.safe_load(file)
    ompl_planning_pipeline_config["move_group"].update(ompl_planning_yaml)

    # Kinematics
    kinematics_yaml_path = os.path.join(
        get_package_share_directory("moveit_easyrobot"),
        "config",
        "kinematics.yaml",
    )
    with open(kinematics_yaml_path, "r") as file:
        kinematics_yaml = yaml.safe_load(file)

    robot_description_kinematics = {"robot_description_kinematics": kinematics_yaml}

    # Joint Limits
    joint_limits_yaml_path = os.path.join(
        get_package_share_directory("moveit_easyrobot"),
        "config",
        "joint_limits.yaml",
    )
    with open(joint_limits_yaml_path, "r") as file:
        joint_limits_yaml = yaml.safe_load(file)
    robot_description_joint_limits = {"robot_description_planning": joint_limits_yaml}

    ld = LaunchDescription()
    use_sim = LaunchConfiguration('use_sim')
    declare_use_sim = DeclareLaunchArgument(
        'use_sim',
        default_value='true',
        description='Start robot in Gazebo simulation.')
    ld.add_action(declare_use_sim)

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config],
        parameters=[
            robot_description,
            robot_description_semantic,
            ompl_planning_pipeline_config,
            robot_description_kinematics,
            robot_description_joint_limits,
            {'use_sim_time': use_sim},
        ]
    )

    ld.add_action(rviz)

    return ld
