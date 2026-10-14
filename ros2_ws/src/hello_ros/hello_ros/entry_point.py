"""ROS 2 entry point that runs the subscriber and gRPC server together."""

import os

import rclpy

from hello_ros.grpc_server import start_grpc_server
from hello_ros.subscriber import HelloSubscriber

DEFAULT_GRPC_HOST = os.environ.get("GRPC_HOST", "127.0.0.1")
DEFAULT_GRPC_PORT = int(os.environ.get("GRPC_PORT", "50051"))


def main(args: list[str] | None = None) -> None:
    """Run ROS callbacks while the gRPC server serves its own worker threads."""
    rclpy.init(args=args)

    subscriber = HelloSubscriber()
    grpc_server = None

    try:
        # Starting gRPC returns immediately; ROS keeps processing callbacks here.
        grpc_server = start_grpc_server(
            host=DEFAULT_GRPC_HOST,
            port=DEFAULT_GRPC_PORT,
        )
        subscriber.get_logger().info(
            f"gRPC server listening on {DEFAULT_GRPC_HOST}:{DEFAULT_GRPC_PORT}"
        )
        rclpy.spin(subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop new gRPC work and wait briefly for in-flight calls before cleanup.
        if grpc_server is not None:
            grpc_server.stop(grace=1).wait()
        subscriber.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
