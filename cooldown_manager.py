import time
class ServerCooldownManager:
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

class UserCooldownManager:
    def __init__(self):
        self.cooldowns = {}

    def is_on_cooldown(self, user_id: int, cooldown_type: str) -> bool:
        current_time = time.time()
        return (
            cooldown_type in self.cooldowns and
            user_id in self.cooldowns[cooldown_type] and
            current_time < self.cooldowns[cooldown_type][user_id]
        )

    def get_remaining_time(self, user_id: int, cooldown_type: str) -> int:
        current_time = time.time()
        if (
            cooldown_type in self.cooldowns and
            user_id in self.cooldowns[cooldown_type]
        ):
            cooldown_end = self.cooldowns[cooldown_type][user_id]
            remaining_time = cooldown_end - current_time
            return max(0, int(remaining_time))
        return 0

    def set_cooldown(self, user_id: int, cooldown_type: str, seconds: int | bool):
        if cooldown_type not in self.cooldowns:
            self.cooldowns[cooldown_type] = {}
        self.cooldowns[cooldown_type][user_id] = time.time() + seconds
        
    def remove_cooldown(self, user_id: int, cooldown_type: str):
        if cooldown_type in self.cooldowns and user_id in self.cooldowns[cooldown_type]:
            del self.cooldowns[cooldown_type][user_id]