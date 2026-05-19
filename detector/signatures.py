SQLI_PATTERNS = [
    r"(?i)(union\s+select)",
    r"(?i)(or\s+1=1)",
    r"(?i)('--)",
    r"(?i)(drop\s+table)",
    r"(?i)(insert\s+into)"
]

XSS_PATTERNS = [
    r"(?i)(<script>)",
    r"(?i)(javascript:)",
    r"(?i)(onerror=)",
    r"(?i)(alert\()"
]

COMMAND_INJECTION_PATTERNS = [
    r"(?i)(;\s*cat)",
    r"(?i)(;\s*ls)",
    r"(?i)(&&)",
    r"(?i)(\|\|)"
]

TRAVERSAL_PATTERNS = [
    r"(\.\./)",
    r"(\.\.\\)"
]

LFI_PATTERNS = [
    r"(?i)(/etc/passwd)",
    r"(?i)(php://input)"
]