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

    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ]),
        launch_arguments={'gz_args': f'-r {world_path}'}.items()
    )

    return LaunchDescription([
        gz_sim_launch,

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/world/car_world/create@ros_gz_interfaces/srv/SpawnEntity',
                '/world/car_world/remove@ros_gz_interfaces/srv/DeleteEntity',
                '/world/car_world/set_pose@ros_gz_interfaces/srv/SetEntityPose',
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
            ],
            output='screen'
        ),

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
