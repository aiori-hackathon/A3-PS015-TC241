from src.network_probes import check_hostname, get_system_info


def diagnose_network(network, dns, tcp, icmp):
    """Generate transparent, evidence-based network diagnosis."""

    findings = []
    evidence_count = 0

    def add_finding(
        title, severity, evidence, causes, actions,
        interpretation, confidence
    ):
        findings.append({
            "finding": title,
            "severity": severity,
            "evidence": evidence,
            "possible_causes": causes,
            "recommendation": actions,
            "interpretation": interpretation,
            "confidence": confidence
        })

    # Rule 1: Target reachability
    network_status = network.get("status")

    if network_status == "Online":
        evidence_count += 1

    elif network_status in ("Offline or unreachable", "Offline"):
        add_finding(
            "Target TCP connection failed",
            "HIGH",
            network.get("error") or network_status,
            [
                "Remote service unavailable",
                "Firewall or port filtering",
                "Local connectivity problem",
                "Incorrect hostname or port"
            ],
            [
                "Check internet connectivity.",
                "Verify the hostname and service port.",
                "Check firewall settings.",
                "Repeat the test using another authorized endpoint."
            ],
            "The target did not accept the TCP connection during this test. "
            "This does not identify the exact point of failure.",
            "Medium"
        )

    # Rule 2: DNS resolution
    dns_status = dns.get("status")

    if dns_status == "Success":
        evidence_count += 1

    elif dns_status == "Failed":
        evidence_count += 1
        add_finding(
            "DNS resolution failed",
            "HIGH",
            dns.get("error") or "Hostname lookup failed",
            [
                "Incorrect hostname",
                "DNS server unavailable",
                "DNS configuration problem",
                "DNS traffic blocked"
            ],
            [
                "Verify the hostname spelling.",
                "Check the configured DNS server.",
                "Try another trusted DNS resolver.",
                "Repeat the lookup."
            ],
            "The system could not resolve the hostname into an IP address. "
            "This points to a name-resolution problem, but its source is unknown.",
            "High"
        )

    # Rule 3: ICMP packet loss
    loss = icmp.get("packet_loss_percent")

    if loss is not None:
        evidence_count += 1

        if loss > 0:
            severity = "HIGH" if loss >= 50 else "MEDIUM"

            add_finding(
                "ICMP packet loss observed",
                severity,
                f"{loss}% packet loss",
                [
                    "Network congestion",
                    "Unstable network connection",
                    "ICMP traffic filtering",
                    "Remote endpoint rate limiting"
                ],
                [
                    "Repeat the packet-loss test.",
                    "Compare results with another authorized endpoint.",
                    "Check Wi-Fi or Ethernet stability.",
                    "Compare ICMP results with TCP measurements."
                ],
                "Some ICMP packets did not receive a response. "
                "Packet loss alone does not prove application traffic is affected.",
                "Medium"
            )

    # Rule 4: TCP probe failures
    attempts = tcp.get("attempts", 0)
    failed = tcp.get("failed_attempts", 0)

    if attempts > 0:
        evidence_count += 1

        if failed > 0:
            failure_rate = (failed / attempts) * 100
            severity = "HIGH" if failure_rate >= 50 else "MEDIUM"

            add_finding(
                "TCP connection failures observed",
                severity,
                f"{failed} of {attempts} attempts failed "
                f"({failure_rate:.1f}%)",
                [
                    "Remote service instability",
                    "Firewall or port filtering",
                    "Intermittent network connectivity",
                    "Server-side connection limits"
                ],
                [
                    "Repeat the TCP connection test.",
                    "Verify the target service is available.",
                    "Check firewall rules.",
                    "Compare results with another authorized endpoint."
                ],
                "Repeated TCP connection attempts failed. "
                "The failure rate indicates connection instability "
                "during this measurement.",
                "High" if failure_rate >= 50 else "Medium"
            )

    # Rule 5: High TCP connection setup time
    average = tcp.get("average_latency_ms")

    if average is not None and average > 150:
        severity = "HIGH" if average > 300 else "MEDIUM"

        add_finding(
            "High TCP connection setup time",
            severity,
            f"Average TCP connection setup time: {average} ms",
            [
                "Network delay",
                "Remote server response delay",
                "Network congestion",
                "Routing or connection establishment delays"
            ],
            [
                "Repeat the measurement several times.",
                "Compare with another authorized endpoint.",
                "Check whether other applications experience delays.",
                "Compare measurements at different times."
            ],
            "TCP connection establishment took longer than the "
            "configured threshold. This is not a pure round-trip "
            "latency measurement.",
            "Medium"
        )

    # Overall diagnosis
    if evidence_count < 2:
        status = "INCONCLUSIVE"
        overall_severity = "UNKNOWN"
        summary = (
            "Not enough valid measurements to assess the connection."
        )

    elif findings:
        status = "ISSUES_DETECTED"

        severity_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        overall_severity = max(
            (item["severity"] for item in findings),
            key=lambda value: severity_order[value]
        )

        summary = (
            "One or more warning conditions were observed. "
            "Measurements support the findings, but possible causes "
            "are hypotheses and are not confirmed root causes."
        )

    else:
        status = "NO_ISSUES_DETECTED"
        overall_severity = "NONE"
        summary = (
            "No configured warning conditions were detected in these "
            "measurements. This does not guarantee the network is healthy."
        )

    return {
        "status": status,
        "severity": overall_severity,
        "summary": summary,
        "evidence_count": evidence_count,
        "findings": findings,
        "limitations": [
            "A failed TCP connection does not prove the gateway is down.",
            "ICMP filtering can affect packet-loss measurements.",
            "TCP connection time is not pure round-trip latency.",
            "Congestion and loaded jitter require dedicated measurements.",
            "Possible causes are hypotheses, not confirmed root causes.",
            "Confidence describes evidence strength, not statistical probability."
        ]
    }


def run_diagnostics(hostname="google.com", port=443):
    """Run the basic diagnostic checks."""
    return {
        "system": get_system_info(),
        "network": check_hostname(hostname, port),
    }
