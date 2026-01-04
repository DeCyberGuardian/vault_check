def calculate_risk(results: dict):
    """
    Evaluate overall risk based on system, processes, and network results.
    Returns a risk level and actionable recommendations.
    Core-safe: no printing, no side effects.
    """

    score = 0
    recommendations = []

    # Process checks
    processes = results.get("processes", {}).get("suspicious_processes", [])
    if processes:
        score += 1
        recommendations.append("Review processes running from non-standard paths")

    # Firewall check
    firewall = results.get("system", {}).get("firewall")
    if isinstance(firewall, str) and firewall.lower() == "disabled":
        score += 1
        recommendations.append("Enable and configure a host-based firewall")

    # Disk encryption check
    encryption = results.get("system", {}).get("disk_encryption")
    if isinstance(encryption, str) and encryption.lower() == "disabled":
        score += 1
        recommendations.append("Enable full disk encryption")

    # Risk level assignment
    if score == 0:
        level = "LOW"
    elif score == 1:
        level = "MODERATE"
    else:
        level = "ELEVATED"

    if not recommendations:
        recommendations.append("Maintain current security hygiene")

    return level, recommendations
