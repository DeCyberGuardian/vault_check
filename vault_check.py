import argparse
import json
import getpass

from utils.helpers import banner
from core.system import system_summary
from core.processes import process_check
from core.network import network_summary
from core.online_intel import online_checks
from core.risk_engine import calculate_risk
from core.hibp import check_password_pwned


def main():
    parser = argparse.ArgumentParser(
        description="The Intelligence Vault — vault_check"
    )
    parser.add_argument(
        "--online",
        action="store_true",
        help="Enable optional online intelligence checks"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    args = parser.parse_args()

    # Banner ALWAYS shows (design decision)
    banner()

    results = {}

    # Core checks
    results["system"] = system_summary()
    results["processes"] = process_check()
    results["network"] = network_summary()

    # Optional online intelligence
    if args.online:
        results["online"] = online_checks()
    else:
        results["online"] = None

    # Optional HIBP check (explicit consent)
    hibp_result = None
    if args.online:
        consent = input("\nRun HIBP password exposure check? (y/N): ").strip().lower()
        if consent == "y":
            password = getpass.getpass(
                "Enter password to check (input hidden, not stored): "
            )
            hibp_result = check_password_pwned(password)

    results["hibp"] = hibp_result

    # Risk evaluation
    risk, recommendations = calculate_risk(results)
    results["risk_level"] = risk
    results["recommendations"] = recommendations

    # Output handling
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if hibp_result is not None:
            print("\n[ Breach Exposure Check ]")
            if hibp_result > 0:
                print(f"⚠ Password found in breaches {hibp_result} times")
            else:
                print("✔ Password not found in known breaches")

        print("\n[ Overall Risk Level ]")
        print(risk)

        print("\n[ Recommendations ]")
        for r in recommendations:
            print(f"- {r}")


if __name__ == "__main__":
    main()
