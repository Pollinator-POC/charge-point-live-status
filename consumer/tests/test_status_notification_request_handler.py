import base64

from transformer import Transformer
import json


class TestTransformer:

    def test_process(self):

        payload = '{"message_id": "fede980d-2f2f-4dc0-93bc-ad64b375caa0", "message_type": 2, "charge_point_id": "94073806-8222-430e-8ca4-fab78b58fb67", "action": "StatusNotification", "write_timestamp": "2023-01-01T10:43:13.900215+00:00", "body": {"connector_id": 2, "error_code": "NoError", "status": "Charging", "timestamp": "2023-01-01T10:43:13.900215+00:00", "info": null, "vendor_id": null, "vendor_error_code": null}, "write_timestamp_epoch": 1672569793900}'
        transformer = Transformer()
        result = transformer.process(payload)
        assert result == {
            "action": "StatusNotification",
            "charge_point_id": "94073806-8222-430e-8ca4-fab78b58fb67",
            "connector_id": 2,
            "error_code": "NoError",
            "info": None,
            "message_id": "fede980d-2f2f-4dc0-93bc-ad64b375caa0",
            "message_type": 2,
            "status": "Charging",
            "timestamp": "2023-01-01T10:43:13.900215+00:00",
            "vendor_error_code": None,
            "vendor_id": None,
            "write_timestamp": "2023-01-01T10:43:13.900215+00:00",
            "write_timestamp_epoch": 1672569793900
        }

    def test__status_notification_request_reshaper(self):
        data = {
            "message_id": "338c112c-420c-4df4-8318-2160875eb532",
            "message_type": 2,
            "charge_point_id": "01a0f039-7685-4a7f-9ef6-8d262a7898fb",
            "action": "StatusNotification",
            "write_timestamp": "2023-01-01T12:54:07.750286+00:00",
            "body": {
                "connector_id": 1,
                "error_code": "NoError",
                "status": "Preparing",
                "timestamp": "2023-01-01T12:54:07.750286+00:00",
                "info": None,
                "vendor_id": None,
                "vendor_error_code": None
            },
            "write_timestamp_epoch":1672577647750
        }
        transformer = Transformer()
        result = transformer._status_notification_request_extractor(data)

        assert result == {
            "message_id": "338c112c-420c-4df4-8318-2160875eb532",
            "message_type": 2,
            "charge_point_id": "01a0f039-7685-4a7f-9ef6-8d262a7898fb",
            "action": "StatusNotification",
            "write_timestamp": "2023-01-01T12:54:07.750286+00:00",
            "connector_id": 1,
            "error_code": "NoError",
            "status": "Preparing",
            "timestamp": "2023-01-01T12:54:07.750286+00:00",
            "info": None,
            "vendor_id": None,
            "vendor_error_code": None,
            "write_timestamp_epoch": 1672577647750
        }
