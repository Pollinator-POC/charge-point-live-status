from typing import Callable


class Router:
    def __init__(self, heartbeat_request_handler, status_notification_request_handler, generic_handler):
        self.heartbeat_request_handler = heartbeat_request_handler
        self.status_notification_request_handler = status_notification_request_handler
        self.generic_handler = generic_handler

    def _request_handlers(self, action):
        return {
            "Heartbeat": self.heartbeat_request_handler,
            "StatusNotification": self.status_notification_request_handler,
        }.get(action, self.generic_handler)

    def get_handler(self, action: str, message_type: str) -> Callable:
        if message_type == 2:
            return self._request_handlers(action)
        else:
            return self.generic_handler
