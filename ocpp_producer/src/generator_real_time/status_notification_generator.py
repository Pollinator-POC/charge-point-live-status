import json
import uuid
import random

from dateutil import parser
from datetime import datetime, timezone
from typing import Dict

from ocpp.v16 import call
from ocpp.v16.enums import ChargePointErrorCode, ChargePointStatus



class GenerateStatusNotifications:
    def _gen_random_error_code(self, status: str):
        if status == "faulted":
            return ChargePointErrorCode._member_names_[random.randint(0, len(ChargePointStatus._member_names_) - 1)]
        else:
            return "no_error"

    def _status_notification_payload(self, timestamp):
        random_status = ChargePointStatus._member_names_[
            random.randint(0, len(ChargePointStatus._member_names_) - 1)]
        random_error_code = self._gen_random_error_code(random_status)
        return call.StatusNotificationPayload(
            connector_id=1,
            error_code=getattr(ChargePointErrorCode, random_error_code),
            status=getattr(ChargePointStatus, random_status),
            timestamp=timestamp
        ).__dict__

    def decorate(self, charge_point_id: uuid, data: Dict, timestamp: str):
        return {
            "charge_point_id": str(charge_point_id),
            "action": "StatusNotification",
            "message_id": str(uuid.uuid4()),
            "message_type": 2,
            "body": json.dumps(data),
            "write_timestamp": timestamp,
            "write_timestamp_epoch": int(parser.parse(data["timestamp"]).timestamp())
        }

    def generate(self, charge_point_id: str):
        now = datetime.now(timezone.utc)
        charge_point_id = charge_point_id
        data = self._status_notification_payload(now.isoformat())
        return self.decorate(charge_point_id=charge_point_id, data=data, timestamp=now.isoformat())