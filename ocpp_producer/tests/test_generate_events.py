from charger_outage_configuration import ChargerOutageConfiguration
from generate_events import GenerateEvents
from generator_real_time.generator_real_time_events import GenerateRealTimeEvents


class TestGenerateEvents:

    def test_generate_events(self):
        input = [
            {
                "network": "Alpha",
                "outage_rate": 0.85
            },
            {
                "network": "Gamma",
                "outage_rate": 0.85
            }
        ]

        events = GenerateEvents(
            charger_outage_configuration=ChargerOutageConfiguration(),
            generate_real_time_events=GenerateRealTimeEvents()
        ).generate(input)
        assert len(events) == 13076