from typing import Dict

import json

from status_notification_request_writer import StatusNotificationRequestWriter



class StatusNotificationRequestHandler:

    def __init__(self, writer: StatusNotificationRequestWriter):
        self.writer = writer

    def process(self, payload: str):
        data = json.loads(payload)
        data["body"] = json.loads(data["body"])
        result = self._extractor(data)
        self.writer.write(result)
        return result


    def _extractor(self, data: Dict) -> Dict:
        return {
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