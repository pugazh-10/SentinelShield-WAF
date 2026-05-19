import json
from datetime import datetime

LOG_FILE = "logs/attacks.log"


def log_attack(ip, attack_type, severity, payload):

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "attack_type": attack_type,
        "severity": severity,
        "payload": str(payload)
    }

    with open(LOG_FILE, "a") as file:
        file.write(json.dumps(log_entry) + "\n")