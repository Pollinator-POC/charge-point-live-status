import json
import uuid

from dateutil import parser
from datetime import datetime, timezone
from typing import Dict
from freezegun import freeze_time

from ocpp.v16 import call
import pandas as pd
from pandas import DataFrame


class GenerateHeartbeats:
    def pulse(self, starting_time: str, ending_time: str, freq=60):
        collect = []
        with freeze_time(starting_time) as frozen_datetime:
            while (now := datetime.now(timezone.utc)) < parser.parse(ending_time):
                result = self._heartbeat_payload(timestamp=now.isoformat())
                collect.append(result)
                frozen_datetime.tick(freq)
        return collect

    def _heartbeat_payload(self, timestamp: str):
        return call.HeartbeatPayload().__dict__, timestamp

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

    def generate(self, charger_list) -> DataFrame:
        collect = []
        for charge_point_id in charger_list:
           collect = collect + [ self.decorate(charge_point_id, x, timestamp) for x, timestamp in self.pulse("2023-01-01T09:00:00+00:00", "2023-01-01T18:00:00+00:00") ]
        df = pd.DataFrame(collect)
        return df