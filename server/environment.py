import random

class SecureEnvironment:

    def __init__(self):
        self.reset()

    def reset(self):
        self.state_data = {
            "active_users": 100,
            "attack_level": 0.2,
            "server_load": 50,
            "encryption_level": 1,
            "firewall": False
        }

        self.step_count = 0
        self.total_breaches = 0
        self.current_attack = "none"

        return self._obs(0, False)

    def step(self, action):
        self.step_count += 1

        # === APPLY ACTIONS ===
        if action["increase_encryption"]:
            self.state_data["encryption_level"] += 1

        if action["activate_firewall"]:
            self.state_data["firewall"] = True

        self.state_data["active_users"] = max(
            0, self.state_data["active_users"] - action["block_users"]
        )

        self.state_data["server_load"] += action["allocate_resources"]

        # === 🔥 ADAPTIVE ATTACKER ===
        if self.state_data["encryption_level"] > 3:
            self.current_attack = "insider"
            self.state_data["attack_level"] += random.uniform(0.2, 0.4)

        elif self.state_data["server_load"] > 80:
            self.current_attack = "ddos"
            self.state_data["attack_level"] += random.uniform(0.3, 0.5)

        else:
            if random.random() < 0.4:
                self.current_attack = random.choice(["ddos", "breach"])
                self.state_data["attack_level"] += random.uniform(0.1, 0.3)
            else:
                self.current_attack = "none"

        # === SYSTEM PRESSURE ===
        self.state_data["server_load"] += self.state_data["active_users"] * 0.05

        # === BREACH CALCULATION ===
        breach_prob = self.state_data["attack_level"] / (
            self.state_data["encryption_level"] + 1
        )

        if self.state_data["firewall"]:
            breach_prob *= 0.7

        breach = random.random() < min(1.0, breach_prob)

        # === REWARD SYSTEM ===
        reward = 0

        if breach:
            reward -= 1.5
            self.total_breaches += 1
        else:
            reward += 0.8

        if self.state_data["server_load"] > 120:
            reward -= 0.6

        if self.state_data["encryption_level"] > 3:
            reward -= 0.2

        if action["block_users"] > 5:
            reward -= 0.5

        reward += max(0, (5 - self.state_data["encryption_level"])) * 0.1

        if self.state_data["firewall"] and self.current_attack != "none":
            reward += 0.3

        done = self.step_count >= 50

        return self._obs(reward, done)

    def _obs(self, reward, done):
        return {
            "active_users": self.state_data["active_users"],
            "attack_level": self.state_data["attack_level"],
            "server_load": self.state_data["server_load"],
            "encryption_level": self.state_data["encryption_level"],
            "threat_type": self.current_attack,
            "reward": reward,
            "done": done
        }

    @property
    def state(self):
        return {
            "step_count": self.step_count,
            "breaches": self.total_breaches
        }
