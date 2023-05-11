from charger_outage_configuration import ChargerOutageConfiguration
import pandas as pd

class TestChargerOutageConfiguration:
    def test_generate_outage_list(self):
        df = pd.DataFrame([
            {
                "charge_point_id": 1,
                "Network": "Alpha",
            },
            {
                "charge_point_id": 2,
                "Network": "Alpha",
            },
            {
                "charge_point_id": 3,
                "Network": "Alpha",
            },
            {
                "charge_point_id": 4,
                "Network": "Alpha",
            },
            {
                "charge_point_id": 5,
                "Network": "Gamma",
            },
            {
                "charge_point_id": 6,
                "Network": "Beta",
            }

        ])


        result = ChargerOutageConfiguration()._generate_outage_list(input_df = df, network="Alpha", outage_rate=0.5)
        assert len(result) == 2

        result = ChargerOutageConfiguration()._generate_outage_list(input_df=df, network="Alpha", outage_rate=1.0)
        assert set(result) == set([1, 2, 3, 4])
        assert len(result) == 4

    def test_generate(self):
        input = [
            {
                "network": "Alpha",
                "outage_rate": 1.0
            },
            {
                "network": "Gamma",
                "outage_rate": 1.0
            }
        ]

        df = pd.DataFrame([
            {
                "charge_point_id": 1,
                "Network": "Alpha",
            },
            {
                "charge_point_id": 2,
                "Network": "Alpha",
            },
            {
                "charge_point_id": 3,
                "Network": "Alpha",
            },
            {
                "charge_point_id": 4,
                "Network": "Alpha",
            },
            {
                "charge_point_id": 5,
                "Network": "Gamma",
            },
            {
                "charge_point_id": 6,
                "Network": "Beta",
            }

        ])

        result = ChargerOutageConfiguration()._generate(outage_configuration=input, df=df)
        assert result.to_dict(orient="records") == [
            {'Network': 'Alpha', 'charge_point_id': 1, 'outage': True},
            {'Network': 'Alpha', 'charge_point_id': 2, 'outage': True},
            {'Network': 'Alpha', 'charge_point_id': 3, 'outage': True},
            {'Network': 'Alpha', 'charge_point_id': 4, 'outage': True},
            {'Network': 'Gamma', 'charge_point_id': 5, 'outage': True},
            {'Network': 'Beta', 'charge_point_id': 6, 'outage': False}
        ]