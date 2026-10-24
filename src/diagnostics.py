
from src.network_probes import check_hostname, get_system_info


def run_diagnostics(hostname="google.com", port=443):
    return {
        "system": get_system_info(),
        "network": check_hostname(hostname, port),
    }