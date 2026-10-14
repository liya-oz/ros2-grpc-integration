"""Small gRPC client used by the Flask HTTP route."""

import os

import grpc

import hello_pb2
import hello_pb2_grpc

DEFAULT_GRPC_TARGET = "127.0.0.1:50051"


def get_latest_message(
    server_address: str | None = None,
    timeout: float = 2.0,
) -> hello_pb2.GetLatestMessageResponse:
    """Call the ROS process and return its latest-message response."""
    target = server_address or os.environ.get(
        "HELLO_GRPC_TARGET",
        DEFAULT_GRPC_TARGET,
    )

    # The prototype uses a local, non-TLS channel as allowed by its scope.
    with grpc.insecure_channel(target) as channel:
        stub = hello_pb2_grpc.HelloMessageServiceStub(channel)
        request = hello_pb2.GetLatestMessageRequest()
        return stub.GetLatestMessage(request, timeout=timeout)
