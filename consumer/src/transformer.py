import base64
from typing import Dict, Callable

import json


class Transformer:

    def process(self, payload: str):
        data = json.loads(payload)
        result = self._router(data["action"], data["message_type"])(data)
        return result


    def _request_extractors(self) -> Dict:
        return {
            "Heartbeat": self._heartbeat_request_extractor,
            "StatusNotification": self._status_notification_request_extractor
        }

    def _router(self, action: str, message_type: str) -> Callable:
        if message_type == 2:
            return self._request_extractors()[action]
        else:
            return self._generic_extractor

    def _generic_extractor(self, data):
        return {
            "message_id": data["message_id"],
            "message_type": data["message_type"],
            "charge_point_id": data["charge_point_id"],
            "action": data["action"],
            "write_timestamp": data["write_timestamp"],
            "write_timestamp_epoch": data["write_timestamp_epoch"],
            "body": data["body"]
        }

    def _heartbeat_request_extractor(self, data: Dict) -> Dict:
        return {
            "message_id": data["message_id"],
            "message_type": data["message_type"],
            "charge_point_id": data["charge_point_id"],
            "action": data["action"],
            "write_timestamp": data["write_timestamp"],
            "write_timestamp_epoch": data["write_timestamp_epoch"],
        }

    def _status_notification_request_extractor(self, data: Dict) -> Dict:
        flattened = {
            "message_id": data["message_id"],
            "message_type": data["message_type"],
            "charge_point_id": data["charge_point_id"],
            "action": data["action"],
            "write_timestamp": data["write_timestamp"],
            "write_timestamp_epoch": data["write_timestamp_epoch"],
            "connector_id": data["body"]["connector_id"],
            "error_code": data["body"]["error_code"],
            "status": data["body"]["status"],
            "timestamp": data["body"]["timestamp"],
            "info": data["body"]["info"],
            "vendor_id": data["body"]["vendor_id"],
            "vendor_error_code": data["body"]["vendor_error_code"],
        }

        return flattened
