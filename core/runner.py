"""
core.runner

Shared execution engine for vault_check.
Used by both CLI (v1) and GUI (v2).

Design principles:
- No printing
- No user interaction
- No persistence
- Deterministic outputs
"""

from core.system import system_summary
from core.processes import process_check
from core.network import network_summary
from core.online_intel import online_checks
from core.hibp import check_password_pwned
from core.risk_engine import calculate_risk


def run_checks(
    *,
    online: bool = False,
    hibp_password: str | None = None
) -> dict:
    """
    Run vault_check security hygiene checks.

    Args:
        online (bool): Enable optional online intelligence checks
        hibp_password (str | None): Password for HIBP k-anonymity check (optional)

    Returns:
        dict: Structured results including risk level and recommendations
    """

    results: dict = {}

    # Local checks (always run)
    results["system"] = system_summary()
    results["processes"] = process_check()
    results["network"] = network_summary()

    # Online intelligence (explicit opt-in)
    if online:
        results["online"] = online_checks()
    else:
        results["online"] = None

    # HIBP password exposure check (explicit opt-in)
    if online and hibp_password:
        results["hibp"] = check_password_pwned(hibp_password)
    else:
        results["hibp"] = None

    # Risk evaluation
    risk_level, recommendations = calculate_risk(results)

    results["risk_level"] = risk_level
    results["recommendations"] = recommendations

    return results
