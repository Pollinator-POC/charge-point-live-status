from typing import Dict


class StatusNotificationRequestWriter:
    def __init__(self, client):
        self.client = client

    def write(self, data: Dict):
        key = {
            "charge_point_id": {
                "S": str(data["charge_point_id"] or "")
            },
        }
        expression_attribute_names = {
            "#ET": "event_timestamp",
            "#EC": "error_code",
            "#S": "status",
            "#VEC": "vendor_error_code",
            "#VID": "vendor_id",
        }

        expression_attribute_values = {
            ":et": {
                "S": str(data["write_timestamp"] or "")
            },
            ":ec": {
                "S": str(data["error_code"] or "")
            },
            ":s": {
                "S": str(data["status"] or "")
            },
            ":vec": {
                "S": str(data["vendor_error_code"] or "")
            },
            ":vid": {
                "S": str(data["vendor_id"] or "")
            }
        }
        self.client.update_item(
            TableName="ChargePointLiveStatus",
            Key=key,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            UpdateExpression='SET #ET = :et, #EC = :ec, #S = :s, #VEC = :vec, #VID = :vid',
            ReturnValues='ALL_NEW',
        )

    # def write(self, data: Dict):
    #     self._status_notification_request(data)
    #
    # def _status_notification_request(self, data: Dict):
    #     item = {
    #         "charge_point_id": {
    #             "S": str(data["charge_point_id"] or "")
    #         },
    #         "event_timestamp": {
    #             "S": str(data["timestamp"] or ""),
    #         },
    #         "error_code": {
    #             "S": str(data["error_code"] or "")
    #         },
    #         "status": {
    #             "S": str(data["status"] or "")
    #         },
    #         "vendor_error_code": {
    #             "S": str(data["vendor_error_code"] or "")
    #         },
    #         "vendor_id": {
    #             "S": str(data["vendor_id"] or "")
    #         }
    #     }
    #     self.client.put_item(TableName="ChargePointLiveStatus", Item=item)
    #
