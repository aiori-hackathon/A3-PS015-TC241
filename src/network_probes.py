
import platform
import socket
import subprocess
import time
import re


def check_hostname(hostname="google.com", port=443, timeout=3):
    """Check TCP connectivity and measure connection time."""
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
    """Collect basic system information."""
    return {
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "hostname": socket.gethostname(),
    }


def measure_dns_response(hostname="google.com"):
    """Measure system hostname-resolution time."""
    start = time.perf_counter()

    try:
        addresses = socket.getaddrinfo(
            hostname, None, type=socket.SOCK_STREAM
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        return {
            "host": hostname,
            "status": "Success",
            "dns_lookup_ms": round(elapsed_ms, 2),
            "resolved_addresses": sorted({
                item[4][0] for item in addresses
            }),
            "error": None,
        }
    except OSError as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000

        return {
            "host": hostname,
            "status": "Failed",
            "dns_lookup_ms": round(elapsed_ms, 2),
            "resolved_addresses": [],
            "error": str(exc),
        }


def measure_tcp_latency(hostname="google.com", port=443,
                        count=5, timeout=3):
    """Measure repeated TCP connection times."""
    results = []

    for _ in range(count):
        result = check_hostname(hostname, port, timeout)
        results.append(result["latency_ms"])
        time.sleep(0.2)

    successful = [value for value in results if value is not None]
    failed = count - len(successful)

    return {
        "host": hostname,
        "port": port,
        "attempts": count,
        "successful_attempts": len(successful),
        "failed_attempts": failed,
        "tcp_probe_failure_percent": round(
            failed / count * 100, 2
        ) if count else None,
        "latency_samples_ms": results,
        "average_latency_ms": round(
            sum(successful) / len(successful), 2
        ) if successful else None,
        "min_latency_ms": round(min(successful), 2)
        if successful else None,
        "max_latency_ms": round(max(successful), 2)
        if successful else None,
    }


def measure_icmp_packet_loss(hostname="google.com", count=4):
    """Measure ICMP echo results using the system ping command."""
    if count < 1:
        raise ValueError("count must be at least 1")

    if platform.system() == "Windows":
        command = ["ping", "-n", str(count), "-w", "1000", hostname]
    else:
        command = ["ping", "-c", str(count), hostname]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=count * 2 + 5,
            errors="replace",
        )
        output = completed.stdout + "\n" + completed.stderr

        if platform.system() == "Windows":
            match = re.search(r"\((\d+)%\s*loss\)", output, re.I)
        else:
            match = re.search(r"(\d+(?:\.\d+)?)%\s*packet loss",
                              output, re.I)

        if not match:
            return {
                "host": hostname,
                "status": "Unknown",
                "packet_loss_percent": None,
                "error": "Could not parse ping output. ICMP may be blocked.",
            }

        loss = float(match.group(1))

        return {
            "host": hostname,
            "status": "Completed",
            "packet_loss_percent": loss,
            "error": None,
        }

    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "host": hostname,
            "status": "Failed",
            "packet_loss_percent": None,
            "error": str(exc),
        }
