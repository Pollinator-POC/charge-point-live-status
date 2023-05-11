import json
from typing import Dict


class GenericHandler:

    def process(self, payload: str):
        data = json.loads(payload)
        result = self._extractor(data)
        return result

    def _extractor(self, data: Dict) -> Dict:
        return {
            "message_id": data["message_id"],
            "message_type": data["message_type"],
            "charge_point_id": data["charge_point_id"],
            "action": data["action"],
            "write_timestamp": data["write_timestamp"],
            "write_timestamp_epoch": data["write_timestamp_epoch"],
            "body": data["body"]
        }