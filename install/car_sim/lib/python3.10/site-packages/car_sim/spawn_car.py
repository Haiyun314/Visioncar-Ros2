import rclpy
from rclpy.node import Node
from ros_gz_interfaces.srv import SpawnEntity

class SpawnUrdfNode(Node):
    def __init__(self):
        super().__init__('spawn_urdf_node')
        
        self.cli = self.create_client(SpawnEntity, '/world/car_world/create')
        
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /world/car_world/create service...')
        
        # Load URDF XML from file
        urdf_file = '/home/parallels/ros2_ws_car/src/car_sim/urdf/car.urdf'  # CHANGE THIS PATH
        with open(urdf_file, 'r') as file:
            urdf_xml = file.read()

        # Create request
        req = SpawnEntity.Request()
        req.entity_factory.name = 'my_robot'
        req.entity_factory.sdf = urdf_xml
        req.entity_factory.pose.position.x = 0.0
        req.entity_factory.pose.position.y = 0.0
        req.entity_factory.pose.position.z = 0.0
        req.entity_factory.pose.orientation.x = 0.0
        req.entity_factory.pose.orientation.y = 0.0
        req.entity_factory.pose.orientation.z = 0.0
        req.entity_factory.pose.orientation.w = 1.0


        # Call the service asynchronously
        self.future = self.cli.call_async(req)
        self.future.add_done_callback(self.spawn_response_callback)

    def spawn_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Spawn response: {response.success}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
        finally:
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = SpawnUrdfNode()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
