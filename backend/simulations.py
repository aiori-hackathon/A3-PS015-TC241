from src.diagnostics import diagnose_network


def run_simulation(scenario: str):
    """Run simulated network fault scenarios without real network probes."""

    scenarios = {
        "dns_failure": {
            "network": {
                "status": "Online",
                "latency_ms": 25,
                "error": None
            },
            "dns": {
                "status": "Failed",
                "dns_lookup_ms": None,
                "error": "Simulated DNS resolution failure"
            },
            "tcp": {
                "attempts": 5,
                "successful_attempts": 5,
                "failed_attempts": 0,
                "average_latency_ms": 25
            },
            "icmp": {
                "packet_loss_percent": None
            }
        },

        "tcp_failure": {
            "network": {
                "status": "Offline or unreachable",
                "latency_ms": None,
                "error": "Simulated TCP connection failure"
            },
            "dns": {
                "status": "Success",
                "dns_lookup_ms": 10,
                "error": None
            },
            "tcp": {
                "attempts": 5,
                "successful_attempts": 0,
                "failed_attempts": 5,
                "average_latency_ms": None
            },
            "icmp": {
                "packet_loss_percent": None
            }
        },

        "packet_loss": {
            "network": {
                "status": "Online",
                "latency_ms": 80,
                "error": None
            },
            "dns": {
                "status": "Success",
                "dns_lookup_ms": 12,
                "error": None
            },
            "tcp": {
                "attempts": 5,
                "successful_attempts": 5,
                "failed_attempts": 0,
                "average_latency_ms": 80
            },
            "icmp": {
                "packet_loss_percent": 60
            }
        }
    }

    if scenario not in scenarios:
        raise ValueError("Unknown simulation scenario.")

    measurements = scenarios[scenario]

    diagnosis = diagnose_network(
        measurements["network"],
        measurements["dns"],
        measurements["tcp"],
        measurements["icmp"]
    )

    return {
        "simulation": True,
        "scenario": scenario,
        "measurements": measurements,
        "diagnosis": diagnosis
    }