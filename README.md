# ROS 2 – gRPC Integration Prototype

This architecture experiment sends a text message through a ROS 2 publisher, a ROS 2 subscriber, a gRPC service, a Flask HTTP endpoint, and a browser page.

```text
ROS 2 publisher -> ROS 2 subscriber -> Thread-safe in-memory store
                                              ^
                                              | reads latest message
                                       ROS 2 process
                                       (gRPC server)
                                             ^
                                             | gRPC request/response
                                      Flask (gRPC client)
                                             ^
                                             | HTTP/JSON
                                      Browser frontend
```

The publisher sends a message once per second. The subscriber stores the latest message in a shared dictionary protected by a lock. Every five seconds, it appends a JSONL record containing the ROS message type and data.

The gRPC service reads the latest value under the same lock. Flask calls the gRPC service and returns the response as JSON. The browser communicates only with Flask.

## Requirements

- Ubuntu with ROS 2 Humble installed
- Python 3.10+
- `colcon`
- Python virtual environment support

Install missing system dependencies if needed:

```bash
sudo apt install python3-venv python3-colcon-common-extensions
```

## First-time setup

Run these commands from the project root:

```bash
cd ~/ros2-grpc-integration
source /opt/ros/humble/setup.bash

python3 -m venv --system-site-packages .venv
source .venv/bin/activate

python -m pip install Flask grpcio grpcio-tools "setuptools>=77,<80"

python -m grpc_tools.protoc \
  -I proto \
  --python_out=ros2_ws/src/hello_ros \
  --grpc_python_out=ros2_ws/src/hello_ros \
  proto/hello.proto

cd ros2_ws
colcon build
```

## Run the application

Open three terminals.

### Terminal 1 — ROS 2 publisher

```bash
cd ~/ros2-grpc-integration
source /opt/ros/humble/setup.bash
source .venv/bin/activate
source ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=10

python -m hello_ros.publisher
```

### Terminal 2 — ROS 2 subscriber and gRPC server

```bash
cd ~/ros2-grpc-integration
source /opt/ros/humble/setup.bash
source .venv/bin/activate
source ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=10

python -m hello_ros.entry_point
```

### Terminal 3 — Flask backend

```bash
cd ~/ros2-grpc-integration
source .venv/bin/activate
python -m flask --app flask_app.app run --host 127.0.0.1 --port 5000
```

## Test the application

Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser. The page displays the latest message.

Test the JSON endpoint from a terminal:

```bash
curl http://127.0.0.1:5000/hello
```

Example response:

```json
{"message": "Hello 4"}
```

## Configuration and logging

- The gRPC server listens on `127.0.0.1:50051`.
- Telemetry is appended to `messages.jsonl` in the bridge process's working directory, assuming a relative history path is configured.
- File errors are logged without stopping the subscriber.
