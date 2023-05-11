from botocore.stub import Stubber
import boto3
from status_notification_request_writer import StatusNotificationRequestWriter


class TestStatusNotificationWriter:
    def test_updates_record(self):
        response = {
            "Attributes": {
                "charge_point_id": {
                    "S": "795c5e9f-43b6-4bb6-b589-a026dabdb28b",
                },
                "error_code": {
                    "S": "No Error",
                },
                "event_timestamp": {
                    "S": "2023-01-01T09:00:00+0:00",
                },
                "status": {
                    "S": "Charging",
                },
                "vendor_error_code": {
                    "S": "",
                },
                "vendor_id": {
                    "S": "",
                },
            },
        }

        client = boto3.client("dynamodb", region_name="eu-central-1")

        with Stubber(client) as stubber:
            stubber.add_response("update_item", response, {
                'ExpressionAttributeNames': {
                    '#EC': 'error_code',
                    '#ET': 'event_timestamp',
                    '#S': 'status',
                    '#VEC': 'vendor_error_code',
                    '#VID': 'vendor_id'
                },
                'ExpressionAttributeValues': {
                    ':ec': {'S': 'NoError'},
                    ':et': {'S': '2023-01-01T10:43:13.900215+00:00'},
                    ':s': {'S': 'Charging'},
                    ':vec': {'S': ''},
                    ':vid': {'S': ''}
                },
                'Key': {'charge_point_id': {'S': '795c5e9f-43b6-4bb6-b589-a026dabdb28b'}},
                'ReturnValues': 'ALL_NEW',
                'TableName': 'ChargePointLiveStatus',
                'UpdateExpression': 'SET #ET = :et, #EC = :ec, #S = :s, #VEC = :vec, #VID = :vid'
            })
            payload = {
                "action": "StatusNotification",
                "charge_point_id": "795c5e9f-43b6-4bb6-b589-a026dabdb28b",
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
            result = StatusNotificationRequestWriter(client).write(payload)
            assert result == None

