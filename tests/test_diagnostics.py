from src.diagnostics import run_diagnostics, diagnose_network


def test_diagnostics_returns_system_and_network():
    result = run_diagnostics("localhost", 1)

    assert "system" in result
    assert "network" in result
    assert "status" in result["network"]


def test_inconclusive_when_evidence_is_insufficient():
    result = diagnose_network(
        {},
        {},
        {},
        {}
    )

    assert result["status"] == "INCONCLUSIVE"
    assert result["severity"] == "UNKNOWN"


def test_high_severity_for_dns_failure():
    result = diagnose_network(
        {"status": "Online"},
        {"status": "Failed", "error": "DNS lookup failed"},
        {},
        {}
    )

    assert result["status"] == "ISSUES_DETECTED"
    assert result["severity"] == "HIGH"
    assert result["findings"][0]["possible_causes"]
    assert result["findings"][0]["recommendation"]


def test_medium_severity_for_partial_tcp_failures():
    result = diagnose_network(
        {"status": "Online"},
        {"status": "Success"},
        {"attempts": 5, "failed_attempts": 1},
        {"packet_loss_percent": 0}
    )

    assert result["status"] == "ISSUES_DETECTED"
    assert result["severity"] == "MEDIUM"


def test_no_issues_detected():
    result = diagnose_network(
        {"status": "Online"},
        {"status": "Success"},
        {
            "attempts": 5,
            "failed_attempts": 0,
            "average_latency_ms": 50
        },
        {"packet_loss_percent": 0}
    )

    assert result["status"] == "NO_ISSUES_DETECTED"
    assert result["severity"] == "NONE"