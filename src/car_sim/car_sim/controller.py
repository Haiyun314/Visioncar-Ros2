import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, NavSatFix
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge

class SensorProcessor(Node):
    def __init__(self):
        super().__init__('sensor_processor')
        self.bridge = CvBridge()
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.gps_sub = self.create_subscription(NavSatFix, '/gps', self.gps_callback, 10)
        self.current_image = None
        self.current_gps = None

    def image_callback(self, msg):
        self.current_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    def gps_callback(self, msg):
        self.current_gps = (msg.latitude, msg.longitude)

    def get_state(self):
        return self.current_image, self.current_gps

class ControlNode(Node):
    def __init__(self, sensor_processor):
        super().__init__('control_node')
        self.sensor_processor = sensor_processor
        self.cmd_pub = self.create_publisher(Twist, '/diff_drive_controller/cmd_vel_unstamped', 10)
        self.timer = self.create_timer(0.1, self.control_loop) 

    def control_loop(self):
        image, gps = self.sensor_processor.get_state()
        if image is None or gps is None:
            missing = []
            if image is None:
                missing.append("image")
            if gps is None:
                missing.append("gps")
            self.get_logger().warn(f"Missing sensor data: {', '.join(missing)}")
            return
        linear_vel, angular_vel = self.control_algorithm(image, gps)

        cmd = Twist()
        cmd.linear.x = linear_vel
        cmd.angular.z = angular_vel
        self.cmd_pub.publish(cmd)
        self.get_logger().info(f'Publishing cmd: linear={linear_vel}, angular={angular_vel}')

    def control_algorithm(self, image, gps):
        return 0.5, 0.0

def main(args=None):
    rclpy.init(args=args)
    sensor_processor = SensorProcessor()
    control_node = ControlNode(sensor_processor)

    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(sensor_processor)
    executor.add_node(control_node)
    try:
        executor.spin()
    finally:
        sensor_processor.destroy_node()
        control_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
