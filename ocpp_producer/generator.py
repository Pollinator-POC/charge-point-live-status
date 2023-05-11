import pandas as pd
from heartbeat_generator import GenerateHeartbeats
from status_notification_generator import GenerateStatusNotifications
from pandas import to_datetime
from datetime import datetime, timezone



num_chargers = 10
charger_list = list(range(1, num_chargers+1))


status_notifications_df = GenerateStatusNotifications().generate(charger_list)
heartbeats_df = GenerateHeartbeats().generate(charger_list)
df = pd.concat([status_notifications_df, heartbeats_df])

df["write_timestamp_for_sorting"] = to_datetime(df["write_timestamp"])
df.sort_values(by=['write_timestamp_for_sorting'], ascending=True, inplace=True)
df.drop(["write_timestamp_for_sorting"], axis=1, inplace=True)
now = int(datetime.now(timezone.utc).timestamp())
df.to_json(f"./data/{now}.json", orient="records")