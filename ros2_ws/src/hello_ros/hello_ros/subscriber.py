import json
import threading
import time
from pathlib import Path

from rclpy.node import Node
from std_msgs.msg import String

MESSAGE_TYPE = "std_msgs/msg/String"
SAVE_INTERVAL_SECONDS = 5

shared_data: dict[str, str] = {
    "message_type": "",
    "message_data": "",
}
shared_data_lock = threading.Lock()


class HelloSubscriber(Node):

    def __init__(self, history_path: str | Path = "messages.jsonl") -> None:
        super().__init__("hello_subscriber")
        self._history_path = Path(history_path)
        self._file_lock = threading.Lock()
        self._last_save_time = time.time()
        self._subscription = self.create_subscription(
            String,
            "/hello",
            self.hello_message_callback,
            10,
        )

    def hello_message_callback(self, message: String) -> None:
        """Update the shared message and save it to the history file."""
        record = {
            "message_type": MESSAGE_TYPE,
            "message_data": message.data,
        }

        with shared_data_lock:
            shared_data["message_type"] = record["message_type"]
            shared_data["message_data"] = record["message_data"]

        with self._file_lock:
            current_time = time.time()
            if current_time - self._last_save_time < SAVE_INTERVAL_SECONDS:
                return

            try:
                with self._history_path.open("a", encoding="utf-8") as history_file:
                    json.dump(record, history_file)
                    history_file.write("\n")
            except OSError as error:
                self.get_logger().error(
                    f"Could not append message to {self._history_path}: {error}"
                )
            else:
                self._last_save_time = time.time()
