"""gRPC service that reads the latest message from the shared store."""

from concurrent.futures import ThreadPoolExecutor

import grpc

import hello_pb2
import hello_pb2_grpc
from hello_ros.subscriber import shared_data, shared_data_lock


class HelloMessageService(hello_pb2_grpc.HelloMessageServiceServicer):
    """Serve the latest message without handling ROS topics directly."""

    def GetLatestMessage(
        self,
        _request: hello_pb2.GetLatestMessageRequest,
        context: grpc.ServicerContext,
    ) -> hello_pb2.GetLatestMessageResponse:
        """Read the shared store and put its value in the RPC response."""
        with shared_data_lock:
            latest_message = shared_data["message_data"]
        return hello_pb2.GetLatestMessageResponse(message=latest_message)


def start_grpc_server(
    host: str = "127.0.0.1",
    port: int = 50051,
) -> grpc.Server:
    """Start a gRPC server whose worker threads handle incoming requests."""
    server = grpc.server(ThreadPoolExecutor(max_workers=4))
    service = HelloMessageService()
    hello_pb2_grpc.add_HelloMessageServiceServicer_to_server(service, server)

    bound_port = server.add_insecure_port(f"{host}:{port}")
    if bound_port == 0:
        raise RuntimeError(f"Could not bind the gRPC server to {host}:{port}")

    server.start()
    return server
