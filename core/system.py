import platform
import subprocess
import sys


def _check_firewall() -> str:
    system = platform.system()

    try:
        # Windows Firewall
        if system == "Windows":
            result = subprocess.check_output(
                ["netsh", "advfirewall", "show", "allprofiles"],
                stderr=subprocess.DEVNULL
            ).decode()
            return "Enabled" if "ON" in result else "Disabled"

        # Linux (UFW / firewalld)
        if system == "Linux":
            try:
                ufw = subprocess.check_output(
                    ["ufw", "status"],
                    stderr=subprocess.DEVNULL
                ).decode()
                return "Enabled" if "Status: active" in ufw else "Disabled"
            except Exception:
                try:
                    firewalld = subprocess.check_output(
                        ["systemctl", "is-active", "firewalld"],
                        stderr=subprocess.DEVNULL
                    ).decode().strip()
                    return "Enabled" if firewalld == "active" else "Disabled"
                except Exception:
                    return "Unknown"

        return "Unknown"

    except Exception:
        return "Unknown"


def _check_disk_encryption() -> str:
    system = platform.system()

    try:
        if system == "Windows":
            result = subprocess.check_output(
                ["manage-bde", "-status"],
                stderr=subprocess.DEVNULL
            ).decode()
            return "Enabled" if "Protection On" in result else "Disabled"

        if system == "Linux":
            # Linux disk encryption detection is complex, depends on LUKS
            return "Unknown (depends on LUKS configuration)"

    except Exception:
        return "Unknown"


def system_summary() -> dict:
    """
    Return system information for vault_check.
    Core-safe: no printing, no side effects.
    """
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "disk_encryption": _check_disk_encryption(),
        "firewall": _check_firewall(),
        "python_version": sys.version.split()[0]
    }

    return info
