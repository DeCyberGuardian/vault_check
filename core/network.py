import psutil
import socket

def network_summary() -> dict:
    """
    Return network interfaces and their active IPv4 addresses.
    Core-safe: no printing, returns structured dict.
    """
    addresses = psutil.net_if_addrs()
    active_ips = []

    for iface, addr_list in addresses.items():
        for addr in addr_list:
            if addr.family == socket.AF_INET:
                ip = addr.address
                if ip and not ip.startswith("127."):
                    active_ips.append({
                        "interface": iface,
                        "ip": ip
                    })

    return {
        "interfaces": active_ips  # snake_case for consistency
    }
