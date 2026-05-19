import time


request_tracker = {}

REQUEST_LIMIT = 10
TIME_WINDOW = 60


def is_rate_limited(ip):

    current_time = time.time()

    if ip not in request_tracker:
        request_tracker[ip] = []

    request_tracker[ip] = [
        timestamp
        for timestamp in request_tracker[ip]
        if current_time - timestamp < TIME_WINDOW
    ]

    request_tracker[ip].append(current_time)

    if len(request_tracker[ip]) > REQUEST_LIMIT:
        return True

    return False