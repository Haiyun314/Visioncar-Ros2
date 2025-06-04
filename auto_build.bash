rm -rf build/ install/ log/
colcon build --packages-select car_sim
source install/setup.bash
LIBGL_ALWAYS_SOFTWARE=1 ros2 launch car_sim car_sim.launch.py