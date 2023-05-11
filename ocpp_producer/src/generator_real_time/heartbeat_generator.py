import json
import uuid

from dateutil import parser
from datetime import datetime, timezone
from typing import Dict

from ocpp.v16 import call


class GenerateHeartbeats:

    def _heartbeat_payload(self):
        return call.HeartbeatPayload().__dict__

    def decorate(self, charge_point_id: uuid, data: Dict, timestamp: str):
        return {
            "charge_point_id": str(charge_point_id),
            "action": "Heartbeat",
            "message_id": str(uuid.uuid4()),
            "message_type": 2,
            "body": json.dumps(data),
            "write_timestamp": timestamp,
            "write_timestamp_epoch": int(parser.parse(timestamp).timestamp())
        }

    def generate(self, charge_point_id: str):
        now = datetime.now(timezone.utc)
        charge_point_id = charge_point_id
        data = self._heartbeat_payload()
        return self.decorate(charge_point_id=charge_point_id, data=data, timestamp=now.isoformat())
