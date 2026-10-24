
import json
from pathlib import Path
from datetime import datetime


def save_report(data):
    reports_dir = Path(__file__).resolve().parent.parent / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"report_{timestamp}.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return report_path