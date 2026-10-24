
from src.diagnostics import run_diagnostics


def test_diagnostics_returns_system_and_network():
    result = run_diagnostics("localhost", 1)

    assert "system" in result
    assert "network" in result
    assert "status" in result["network"]