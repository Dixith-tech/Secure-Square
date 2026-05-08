suspicious_keywords = [
    "paypa1",
    "free-money",
    "verify-account",
    "bank-login"
]


def detect_phishing(url):
    for keyword in suspicious_keywords:
        if keyword in url:
            return True

    return False