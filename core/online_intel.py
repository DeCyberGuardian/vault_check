import requests

def online_checks() -> dict:
    """
    Perform optional online intelligence checks.
    Core-safe: returns structured dict, no printing.
    """
    ip = "Unavailable"
    reputation = "Unavailable"

    try:
        ip_resp = requests.get("https://api.ipify.org", timeout=5)
        if ip_resp.ok and ip_resp.text:
            ip = ip_resp.text.strip()
        # Placeholder for more advanced IP reputation logic
        reputation = "No known issues (basic check)"
    except Exception:
        pass  # Silent fail, returns default values

    return {
        "public_ip": ip,
        "reputation": reputation,
        "source": "basic check"
    }
