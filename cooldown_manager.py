import time
class CooldownManager:
    def __init__(self):
        self.cooldowns = {}

    def is_on_cooldown(self, server_id: int) -> bool:
        current_time = time.time()
        if server_id in self.cooldowns:
            cooldown_end = self.cooldowns[server_id]
            if current_time < cooldown_end:
                return True
        return False

    def get_remaining_time(self, server_id: int) -> int:
        current_time = time.time()
        if server_id in self.cooldowns:
            cooldown_end = self.cooldowns[server_id]
            remaining_time = cooldown_end - current_time
            if remaining_time > 0:
                return int(remaining_time)
        return 0

    def set_cooldown(self, server_id: int, seconds: int):
        self.cooldowns[server_id] = time.time() + seconds