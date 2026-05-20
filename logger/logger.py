from datetime import datetime
import pytz
import os

LOG_FILE = "logs/attacks.log"

def log_attack(attack_data):

    os.makedirs("logs", exist_ok=True)

    india = pytz.timezone('Asia/Kolkata')

    timestamp = datetime.now(india).strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"{timestamp} | "
        f"{attack_data['ip']} | "
        f"{attack_data['attack_type']} | "
        f"{attack_data['severity']}\n"
    )

    with open(LOG_FILE, "a") as file:
        file.write(log_entry)