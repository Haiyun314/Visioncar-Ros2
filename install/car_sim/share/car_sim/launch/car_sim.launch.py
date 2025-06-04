from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    car_sim_dir = get_package_share_directory('car_sim')
    urdf_path = os.path.join(car_sim_dir, 'urdf', 'car.urdf')
    world_path = os.path.join(car_sim_dir, 'world', 'car_world.sdf')

    # Use official ROS-GZ launch file and pass your world
    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ]),
        launch_arguments={'world': world_path}.items()
    )

    return LaunchDescription([
        gz_sim_launch,

        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package='car_sim',
                    executable='spawn_car',
                    output='screen',
                )
            ]
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            arguments=[urdf_path],
            output='screen'
        ),
    ])
