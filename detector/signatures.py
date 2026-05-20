import re

patterns = {

    "SQL Injection": [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"(?i)(union|select|insert|drop|delete|update|or 1=1)"
    ],

    "XSS Attack": [
        r"(?i)<script.*?>.*?</script.*?>",
        r"(?i)onerror=",
        r"(?i)alert\("
    ],

    "Directory Traversal": [
        r"\.\./",
        r"\.\.\\"
    ]
}

severity_map = {
    "SQL Injection": "HIGH",
    "XSS Attack": "MEDIUM",
    "Directory Traversal": "HIGH"
}


def detect_attack(data):

    for attack_type, regex_list in patterns.items():

        for pattern in regex_list:

            if re.search(pattern, data):

                return {
                    "type": attack_type,
                    "severity": severity_map[attack_type]
                }

    return None