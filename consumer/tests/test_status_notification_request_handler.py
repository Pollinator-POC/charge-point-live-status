from unittest.mock import Mock

from status_notification_request_handler import StatusNotificationRequestHandler
import json


class TestStatusNotificationRequestHandler:

    def test_process(self):
        writer = Mock()
        writer.write.return_value = True
        payload = json.dumps({
            "message_id": "338c112c-420c-4df4-8318-2160875eb532",
            "message_type": 2,
            "charge_point_id": "01a0f039-7685-4a7f-9ef6-8d262a7898fb",
            "action": "StatusNotification",
            "write_timestamp": "2023-01-01T12:54:07.750286+00:00",
            "body": json.dumps({
                "connector_id": 1,
                "error_code": "NoError",
                "status": "Preparing",
                "timestamp": "2023-01-01T12:54:07.750286+00:00",
                "info": None,
                "vendor_id": None,
                "vendor_error_code": None
            }),
            "write_timestamp_epoch":1672577647750
        })
        transformer = StatusNotificationRequestHandler(writer)
        result = transformer.process(payload)
        assert result == {
            'action': 'StatusNotification',
            'charge_point_id': '01a0f039-7685-4a7f-9ef6-8d262a7898fb',
            'connector_id': 1,
            'error_code': 'NoError',
            'info': None,
            'message_id': '338c112c-420c-4df4-8318-2160875eb532',
            'message_type': 2,
            'status': 'Preparing',
            'timestamp': '2023-01-01T12:54:07.750286+00:00',
            'vendor_error_code': None,
            'vendor_id': None,
            'write_timestamp': '2023-01-01T12:54:07.750286+00:00',
            'write_timestamp_epoch': 1672577647750
        }

    def test__status_notification_request_reshaper(self):
        writer = Mock()
        writer.write.return_value = True
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
        transformer = StatusNotificationRequestHandler(writer)
        result = transformer._extractor(data)

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
