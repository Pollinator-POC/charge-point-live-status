from typing import Dict


class HeartbeatRequestWriter:
    def __init__(self, client):
        self.client = client

    def write(self, data: Dict):
        key = {
            "charge_point_id": {
                "S": str(data["charge_point_id"] or "")
            },
        }
        expression_attribute_names = {
            "#LNHT": "last_known_heartbeat_timestamp"
        }

        expression_attribute_values = {
            ":ht": {
                "S": str(data["write_timestamp"] or "")
            }
        }
        self.client.update_item(
            TableName="ChargePointLiveStatus",
            Key=key,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            UpdateExpression='SET #LNHT = :ht',
            ReturnValues='ALL_NEW',
        )