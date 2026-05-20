from flask import Flask, request, jsonify, render_template, redirect
from detector.signatures import detect_attack
from logger.logger import log_attack
from limiter.rate_limiter import is_rate_limited
from collections import Counter
import os

app = Flask(__name__)

# -----------------------------
# HOME ROUTE
# Redirect directly to dashboard
# -----------------------------
@app.route("/")
def home():
    return redirect("/dashboard")


# -----------------------------
# REQUEST INSPECTION ROUTE
# -----------------------------
@app.route("/inspect")
def inspect():

    ip = request.remote_addr

    # RATE LIMIT CHECK
    if is_rate_limited(ip):

        attack_data = {
            "ip": ip,
            "attack_type": "Rate Limit Exceeded",
            "severity": "HIGH"
        }

        log_attack(attack_data)

        return jsonify({
            "status": "blocked",
            "reason": "Rate limit exceeded"
        }), 429

    # GET FULL REQUEST INPUT
    data = request.query_string.decode()

    # DETECT ATTACK
    attack = detect_attack(data)

    if attack:

        attack_data = {
            "ip": ip,
            "attack_type": attack["type"],
            "severity": attack["severity"]
        }

        log_attack(attack_data)

        return jsonify({
            "status": "blocked",
            "attack": attack
        }), 403

    return jsonify({
        "status": "safe",
        "message": "No threats detected"
    })


# -----------------------------
# DASHBOARD ROUTE
# -----------------------------
@app.route("/dashboard")
def dashboard():

    logs = []

    attack_counts = Counter()
    ip_counts = Counter()

    log_file = "logs/attacks.log"

    if os.path.exists(log_file):

        with open(log_file, "r") as file:

            for line in file.readlines():

                try:

                    parts = line.strip().split(" | ")

                    timestamp = parts[0]
                    ip = parts[1]
                    attack_type = parts[2]
                    severity = parts[3]

                    log_entry = {
                        "timestamp": timestamp,
                        "ip": ip,
                        "attack_type": attack_type,
                        "severity": severity
                    }

                    logs.append(log_entry)

                    attack_counts[attack_type] += 1
                    ip_counts[ip] += 1

                except:
                    pass

    total_attacks = len(logs)

    logs.reverse()

    return render_template(
        "dashboard.html",
        logs=logs,
        total_attacks=total_attacks,
        attack_counts=attack_counts,
        ip_counts=ip_counts
    )


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)