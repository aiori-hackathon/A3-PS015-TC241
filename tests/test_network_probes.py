
from src.network_probes import get_system_info


def test_system_info_has_expected_fields():
    info = get_system_info()

    assert "operating_system" in info
    assert "python_version" in info
    assert "hostname" in info