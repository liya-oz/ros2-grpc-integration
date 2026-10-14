import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HelloPublisher(Node):

    def __init__(self) -> None:
        super().__init__("hello_publisher")
        self._publisher = self.create_publisher(String, "/hello", 10)
        self._message_number = 0
        self._timer = self.create_timer(1.0, self._publish_hello)

    def _publish_hello(self) -> None:
        message = String()
        self._message_number += 1
        message.data = f"Hello {self._message_number}"
        self._publisher.publish(message)


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = HelloPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
