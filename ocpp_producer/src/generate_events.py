import json
from typing import Dict, Tuple, Union, List

from charger_outage_configuration import ChargerOutageConfiguration
from generator_real_time.generator_real_time_events import GenerateRealTimeEvents


class GenerateEvents:
    def __init__(self, charger_outage_configuration: ChargerOutageConfiguration, generate_real_time_events: GenerateRealTimeEvents):
        self.charge_outage_configuration = charger_outage_configuration
        self.generate_real_time_events = generate_real_time_events

    def generate(self, outage_configuration: list[Union[dict[str, Union[str, float]], dict[str, Union[str, float]]]]) -> List[Dict]:
        config = self.charge_outage_configuration.generate(
            outage_configuration=outage_configuration,
            filepath="ChargePointData.csv"
        )
        collect = []
        for i in config["charge_point_id"].tolist():
            events = self.generate_real_time_events.generate(i)
            for e in events:
                message_type = e["message_type"]
                action = e["action"]
                payload = json.dumps(e)
                result = {
                    "action": action,
                    "message_type": message_type,
                    "payload": payload
                }
                collect.append(result)
        return collect