import requests
import time

BASE_URL = "https://gowtham0826-secure-openenv.hf.space"

def run_agent():
    # Reset environment
    res = requests.post(f"{BASE_URL}/reset")
    state = res.json()

    total_reward = 0

    while not state["done"]:
        action = {
            "increase_encryption": state["attack_level"] > 0.3,
            "block_users": 2 if state["threat_type"] != "none" else 1,
            "allocate_resources": 5,
            "activate_firewall": state["threat_type"] == "ddos"
        }

        res = requests.post(f"{BASE_URL}/step", json=action)
        state = res.json()

        total_reward += state["reward"]

        time.sleep(0.2)  # avoid spamming

    # Final score
    score = requests.get(f"{BASE_URL}/score").json()

    return {
        "total_reward": total_reward,
        "final_score": score
    }


if __name__ == "__main__":
    result = run_agent()
    print("Agent Result:", result)
