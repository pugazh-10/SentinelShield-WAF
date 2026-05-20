from flask import Flask, request, jsonify, render_template

from detector.analyzer import detect_attack
from logger.logger import log_attack
from limiter.rate_limiter import is_rate_limited

import json
from collections import Counter

app = Flask(__name__)

LOG_FILE = "logs/attacks.log"


@app.route("/")
def home():
    return "SentinelShield WAF Running"


@app.route("/inspect", methods=["GET", "POST"])
def inspect_request():

    ip = request.remote_addr

    request_data = {
        "ip": ip,
        "method": request.method,
        "url": request.url,
        "headers": dict(request.headers),
        "args": request.args.to_dict(),
        "body": request.get_data(as_text=True)
    }

    # RATE LIMIT CHECK
    if is_rate_limited(ip):

        log_attack(
            ip=ip,
    attack_type="Rate Limit Exceeded",
    severity="MEDIUM",
    payload=request_data
        )

        return jsonify({
            "status": "BLOCKED",
            "reason": "Too many requests"
        }), 429

    # ATTACK DETECTION
    attack = detect_attack(request_data)

    if attack:

        log_attack(
           ip=ip,
        attack_type=attack["type"],
        severity=attack["severity"],
        payload=request_data
    )

    return jsonify({
        "status": "BLOCKED",
        "attack_type": attack["type"],
        "severity": attack["severity"]
    }), 403

    return jsonify({
        "status": "SAFE"
    })


@app.route("/dashboard")
def dashboard():

    logs = []

    try:

        with open(LOG_FILE, "r") as file:

            for line in file:
                logs.append(json.loads(line))

    except FileNotFoundError:
        pass

    total_attacks = len(logs)

    attack_counts = Counter(
        log["attack_type"] for log in logs
    )

    ip_counts = Counter(
        log["ip"] for log in logs
    )

    logs = list(reversed(logs[-10:]))

    return render_template(
        "dashboard.html",
        total_attacks=total_attacks,
        attack_counts=attack_counts,
        ip_counts=ip_counts,
        logs=logs
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)