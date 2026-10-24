
import platform
import socket
import subprocess
import time


def check_hostname(hostname="google.com", port=443, timeout=3):
    """Check whether a TCP connection can be established."""
    start = time.perf_counter()

    try:
        with socket.create_connection(
            (hostname, port), timeout=timeout
        ):
            latency_ms = (time.perf_counter() - start) * 1000

        return {
            "host": hostname,
            "port": port,
            "status": "Online",
            "latency_ms": round(latency_ms, 2),
            "error": None,
        }
    except OSError as exc:
        return {
            "host": hostname,
            "port": port,
            "status": "Offline or unreachable",
            "latency_ms": None,
            "error": str(exc),
        }


def get_system_info():
    return {
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "hostname": socket.gethostname(),
    }