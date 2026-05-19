import re

from detector.signatures import (
    SQLI_PATTERNS,
    XSS_PATTERNS,
    COMMAND_INJECTION_PATTERNS,
    TRAVERSAL_PATTERNS,
    LFI_PATTERNS
)

def check_patterns(data, patterns):

    for pattern in patterns:
        if re.search(pattern, data):
            return True

    return False


def detect_attack(request_data):

    payload = str(request_data)

    if check_patterns(payload, SQLI_PATTERNS):
        return {
            "type": "SQL Injection",
            "severity": "HIGH"
        }

    if check_patterns(payload, XSS_PATTERNS):
        return {
            "type": "XSS Attack",
            "severity": "MEDIUM"
        }

    if check_patterns(payload, COMMAND_INJECTION_PATTERNS):
        return {
            "type": "Command Injection",
            "severity": "CRITICAL"
        }

    if check_patterns(payload, TRAVERSAL_PATTERNS):
        return {
            "type": "Directory Traversal",
            "severity": "HIGH"
        }

    if check_patterns(payload, LFI_PATTERNS):
        return {
            "type": "Local File Inclusion",
            "severity": "HIGH"
        }

    return None