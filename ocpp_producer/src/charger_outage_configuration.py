import random
from typing import Dict, List, Union

import pandas as pd
from pandas import DataFrame


class ChargerOutageConfiguration:

    def generate(self, outage_configuration: list[Union[dict[str, Union[str, float]], dict[str, Union[str, float]]]], filepath: str = "ChargePointData.csv") -> DataFrame:
        df = pd.read_csv(filepath)
        df['outage'] = False
        charge_point_ids_with_outages = self._flatten_lists_of_lists(
            [self._generate_outage_list(input_df=df, network=x["network"], outage_rate=x["outage_rate"]) for x in
             outage_configuration])
        df.loc[df['charge_point_id'].isin(charge_point_ids_with_outages), 'outage'] = True
        return df

    def _generate_outage_list(self, input_df: DataFrame, network: str, outage_rate: float):
        network_cps = input_df.loc[input_df['Network'] == network]
        outage_size = int(len(network_cps) * outage_rate)
        return random.choices(network_cps['charge_point_id'].values, k=outage_size)

    def _flatten_lists_of_lists(self, list_of_lists):
        return [item for sublist in list_of_lists for item in sublist]
