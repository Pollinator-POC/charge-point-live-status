from typing import Dict, List, Union

import boto3


class DataReader:
    def __init__(self, storage_client: boto3.client):
        self.storage_client = storage_client

    def read(self, table_name: str) -> List[Dict]:
        items = [self._unpack(x) for x in self.get_all(table_name)["Items"]]
        return items

    def _unpack(self, data: Dict):
        return {
            "charge_point_id": data.get("charge_point_id", {}).get("S", ""),
            "status_timestamp": data.get("event_timestamp", {}).get("S", ""),
            "error_code": data.get("error_code", {}).get("S", ""),
            "status": data.get("status", {}).get("S", ""),
            "vendor_error_code": data.get("vendor_error_code", {}).get("S", ""),
            "vendor_id": data.get("vendor_id", {}).get("S", ""),
            "last_known_heartbeat_timestamp": data.get("last_known_heartbeat_timestamp", {}).get("S", ""),
        }

    def get_all(self, table_name: str) -> Union[Dict, List]:
        response = self.storage_client.scan(
            TableName=table_name,
        )

        return response
