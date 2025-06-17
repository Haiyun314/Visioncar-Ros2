# VisionCar-ROS2

**VisionCar-ROS2** is a ROS 2-based simulation of a 4-wheeled car that uses a front camera to follow a visual path and avoid moving objects in Gazebo.
<img src="./images/sim_car_running.gif" alt="Alt text" width="600" height="400"/>


## Features

- Simulates a 4-wheeled robot in Gazebo
- Uses a front-facing camera for visual path tracking
- Integrates basic control strategies
- Avoids dynamic (moving) obstacles
- Publishes and subscribes to standard ROS 2 topics
- Prepares for reinforcement learning integration using PPO (Proximal Policy Optimization)

## Test
```bash
source auto_build.bash

ros2 topic pub --rate 10 /diff_drive_controller/cmd_vel_unstamped geometry_msgs/msg/Twist '{linear: {x: -1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'

```

## Goal

Enable the robot to:
- Follow a visual path without falling off the road
- Avoid moving obstacles in its environment
- Reach a defined target using reinforcement learning strategies

## Future Work

- Implement PPO-based control
- Add more complex environments
- Improve sensor fusion and perception

## Requirements

- ROS 2 (Humble )
- Gazebo (Fortress )
- `ros_gz` bridge for simulation interface
- `diff_drive_controller`, `joint_state_broadcaster`, and related ROS 2 control plugins

## References
- https://control.ros.org/humble/doc/gz_ros2_control/doc/index.html#ign-ros2-control
- https://gazebosim.org/libs/sensors/

Feel free to customize further with installation and usage instructions.
