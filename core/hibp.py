import hashlib
import requests

HIBP_API = "https://api.pwnedpasswords.com/range/"

def check_password_pwned(password: str) -> int | None:
    """
    Uses k-anonymity to check if a password has appeared in breaches.
    No full password or hash is ever sent.
    Returns count if pwned, 0 if not, None on error.
    """
    try:
        sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        res = requests.get(HIBP_API + prefix, timeout=5)
        if res.status_code != 200:
            return None

        for line in res.text.splitlines():
            parts = line.split(":")
            if len(parts) != 2:
                continue
            hash_suffix, count = parts
            if hash_suffix.upper() == suffix:
                return int(count)
        return 0

    except Exception:
        return None
