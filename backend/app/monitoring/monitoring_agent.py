import time
import random


def monitor_system():
    while True:
        fake_attack = {
            "ip": f"192.168.1.{random.randint(1,255)}",
            "threat": random.choice([
                "Brute Force",
                "Phishing",
                "Spoofing",
                "Port Scan"
            ]),
            "severity": random.choice([
                "Low",
                "Medium",
                "Critical"
            ])
        }

        print(fake_attack)

        time.sleep(1)


monitor_system()