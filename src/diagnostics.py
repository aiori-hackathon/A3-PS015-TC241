
from src.network_probes import check_hostname, get_system_info


def diagnose_network(network, dns, tcp, icmp):
    """Explain network findings using transparent rules."""

    findings = []
    evidence_count = 0

    
    # Rule 1: Target reachability
    network_status = network.get("status")

    if network_status == "Online":
        evidence_count += 1

    elif network_status in ("Offline or unreachable", "Offline"):
        findings.append({
            "finding": "Target TCP connection failed",
            "evidence": network.get("error") or network_status,
            "recommendation": (
                "Check local connectivity, target hostname, port, "
                "firewall rules, and remote service availability."
            ),
        })

    # Unknown or missing status is not treated as a confirmed failure.


    # Rule 2: DNS resolution
    if dns.get("status") == "Failed":
        findings.append({
            "finding": "DNS resolution failed",
            "evidence": dns.get("error") or "Hostname lookup failed",
            "recommendation": (
                "Check the hostname, DNS server configuration, "
                "and DNS connectivity."
            ),
        })
    elif dns.get("status") == "Success":
        evidence_count += 1

    # Rule 3: ICMP packet loss
    loss = icmp.get("packet_loss_percent")

    if loss is not None:
        evidence_count += 1

        if loss > 0:
            findings.append({
                "finding": "ICMP packet loss observed",
                "evidence": f"{loss}% packet loss",
                "recommendation": (
                    "Repeat the test and compare results with another "
                    "authorized endpoint. ICMP filtering can affect results."
                ),
            })

    # Rule 4: TCP probe failures
    attempts = tcp.get("attempts", 0)
    failed = tcp.get("failed_attempts", 0)

    if attempts > 0:
        evidence_count += 1

        if failed > 0:
            findings.append({
                "finding": "TCP connection failures observed",
                "evidence": f"{failed} of {attempts} attempts failed",
                "recommendation": (
                    "Repeat the test and check service availability, "
                    "firewall rules, and network stability."
                ),
            })

    # Rule 5: High TCP connection time
    # This is a configurable screening threshold, not a universal standard.
    average = tcp.get("average_latency_ms")

    if average is not None and average > 150:
        findings.append({
            "finding": "High TCP connection setup time",
            "evidence": f"Average connection time: {average} ms",
            "recommendation": (
                "Repeat measurements and compare with a known-good "
                "endpoint. TCP setup time includes more than network RTT."
            ),
        })

    if evidence_count < 2:
        status = "INCONCLUSIVE"
        summary = "Not enough valid measurements to assess the connection."
    elif findings:
        status = "ISSUES_DETECTED"
        summary = (
            "One or more warning conditions were observed. "
            "The underlying cause is not confirmed."
        )
    else:
        status = "NO_ISSUES_DETECTED"
        summary = (
            "No configured warning conditions were detected in these "
            "measurements. This does not guarantee the network is healthy."
        )

    return {
        "status": status,
        "summary": summary,
        "evidence_count": evidence_count,
        "findings": findings,
        "limitations": [
            "A failed TCP connection does not prove the gateway is down.",
            "ICMP filtering can affect packet-loss measurements.",
            "TCP connection time is not pure round-trip latency.",
            "Congestion and loaded jitter require dedicated measurements.",
        ],
    }


def run_diagnostics(hostname="google.com", port=443):
    """Run the basic diagnostic checks."""
    return {
        "system": get_system_info(),
        "network": check_hostname(hostname, port),
    }
