import json
import uuid
import random

from dateutil import parser
from datetime import datetime, timezone, timedelta
from typing import Callable, Dict
from freezegun import freeze_time

from ocpp.v16 import call, call_result
from ocpp.v16.enums import ChargePointErrorCode, ChargePointStatus
import pandas as pd
from pandas import to_datetime, DataFrame


class GenerateStatusNotifications:
    def pulse(self, starting_time: str, ending_time: str, freq=60):
        collect = []
        with freeze_time(starting_time) as frozen_datetime:
            while (now := datetime.now(timezone.utc)) < parser.parse(ending_time):
                result = self._status_notification_payload(timestamp=now.isoformat())
                collect.append(result)
                frozen_datetime.tick(freq)
        return collect
    def _gen_random_error_code(self, status: str):
        if status == "faulted":
            return ChargePointErrorCode._member_names_[random.randint(0, len(ChargePointStatus._member_names_) - 1)]
        else:
            return "no_error"

    def _status_notification_payload(self, timestamp):
        random_status = ChargePointStatus._member_names_[random.randint(0, len(ChargePointStatus._member_names_)-1)]
        random_error_code = self._gen_random_error_code(random_status)
        return call.StatusNotificationPayload(
            connector_id=1,
            error_code=getattr(ChargePointErrorCode, random_error_code),
            status=getattr(ChargePointStatus, random_status),
            timestamp=timestamp
        ).__dict__

    def decorate(self, charge_point_id: uuid, data: Dict):
        return {
            "charge_point_id": str(charge_point_id),
            "action": "StatusNotification",
            "message_id": str(uuid.uuid4()),
            "message_type": 2,
            "body": json.dumps(data),
            "write_timestamp": data["timestamp"],
            "write_timestamp_epoch": int(parser.parse(data["timestamp"]).timestamp())
        }

    def generate(self, charger_list) -> DataFrame:
        collect = []
        for charge_point_id in charger_list:
           collect = collect + [ self.decorate(charge_point_id, x) for x in self.pulse("2023-01-01T09:00:00+00:00", "2023-01-01T18:00:00+00:00") ]
        df = pd.DataFrame(collect)
        return df