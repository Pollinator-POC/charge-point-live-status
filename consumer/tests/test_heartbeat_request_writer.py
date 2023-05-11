from botocore.stub import Stubber
import boto3
from heartbeat_request_writer import HeartbeatRequestWriter


class TestHeartbeatRequestWriter:
    def test_updates_record(self):
        response = {
            "Attributes": {
                "charge_point_id": {
                    "S": "795c5e9f-43b6-4bb6-b589-a026dabdb28b",
                },
                "last_known_heartbeat_timestamp": {
                    "S": "2023-01-01T09:00:00+00:00",
                },
            },
        }

        client = boto3.client("dynamodb", region_name="eu-central-1")

        with Stubber(client) as stubber:
            stubber.add_response("update_item", response, {
                "ExpressionAttributeNames": {"#LNHT": "last_known_heartbeat_timestamp"},
                "ExpressionAttributeValues": {":ht": {"S": "2023-01-01T09:00:00+00:00"}},
                "Key": {"charge_point_id": {"S": "795c5e9f-43b6-4bb6-b589-a026dabdb28b"}},
                "ReturnValues": "ALL_NEW",
                "TableName": "ChargePointLiveStatus",
                "UpdateExpression": "SET #LNHT = :ht"
            })
            result = HeartbeatRequestWriter(client).write({
                "charge_point_id": "795c5e9f-43b6-4bb6-b589-a026dabdb28b",
                "write_timestamp": "2023-01-01T09:00:00+00:00"
            })
            assert result == None

