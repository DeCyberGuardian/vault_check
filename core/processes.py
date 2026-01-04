import psutil
import platform

SYSTEM_PATHS = {
    "Windows": [
        "C:\\Windows\\System32",
        "C:\\Windows",
        "C:\\Program Files",
        "C:\\Program Files (x86)"
    ],
    "Linux": [
        "/usr/bin/",
        "/bin/",
        "/sbin/",
        "/lib/",
        "/lib64/"
    ],
    "Darwin": [  # macOS
        "/usr/bin/",
        "/bin/",
        "/sbin/",
        "/usr/sbin/",
        "/Library/",
        "/System/"
    ]
}

SUSPICIOUS_KEYWORDS = [
    "\\Temp",
    "/tmp",
    "/var/tmp",
    "Downloads",
    ".cache",
    ".local"
]


def process_check() -> dict:
    """
    Scan running processes for non-standard execution paths.
    Fully safe: returns dict, no printing, handles None and unexpected values.
    """
    system = platform.system()
    flagged = []

    for proc in psutil.process_iter(['name', 'exe']):
        try:
            name = proc.info.get("name") or ""
            exe = proc.info.get("exe") or ""

            # Skip empty exe
            if not exe.strip():
                continue

            exe_lower = exe.lower()

            # Check suspicious keywords safely
            if any((k or "").lower() in exe_lower for k in SUSPICIOUS_KEYWORDS):
                flagged.append(f"{name} ({exe})")
                continue  # skip to next process

            # Check if exe is outside trusted system paths
            trusted = SYSTEM_PATHS.get(system, [])
            if not any(exe.startswith(p) for p in trusted):
                flagged.append(f"{name} ({exe})")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        except Exception:
            continue  # Catch-all for unexpected edge cases

    return {
        "suspicious_processes": list(set(flagged)),  # deduplicate
        "count": len(flagged)
    }
