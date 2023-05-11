from generator_real_time.heartbeat_generator import GenerateHeartbeats
from generator_real_time.status_notification_generator import GenerateStatusNotifications


class GenerateRealTimeEvents:
    def generate(self, charge_point_id):
        status_notification = GenerateStatusNotifications().generate(charge_point_id=charge_point_id)
        heartbeat = GenerateHeartbeats().generate(charge_point_id=charge_point_id)
        return [
            status_notification,
            heartbeat
        ]