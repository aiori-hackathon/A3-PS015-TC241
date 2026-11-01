# CONNECTIQ
### Explainable Home and Last-Mile Connectivity Diagnosis

**AIORI-3 Hackathon | PS-015 | Team CONNECTIQ**

## 1. Project Overview

CONNECTIQ is a web-based network diagnostic platform designed to identify and explain connectivity problems in home and last-mile networks.

It performs active network probing, collects network telemetry, and applies deterministic rule-based inference to identify potential connectivity faults.

## 2. Problem Statement

The project addresses:
- Internet connectivity failures.
- DNS resolution failures.
- TCP connection failures.
- Packet loss.
- Unstable network connectivity.

## 3. System Architecture

1. Web Dashboard: Displays diagnostic results.
2. FastAPI Backend: Handles API requests.
3. Network Probe Modules: Perform DNS, TCP, host reachability and ICMP measurements.
4. Telemetry Collection: Organizes measurement results.
5. Rule-Based Inference Engine: Evaluates evidence and classifies faults.
6. Report Generator: Produces JSON diagnostic reports.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend and diagnostic logic |
| FastAPI | REST API |
| HTML5 | Frontend structure |
| CSS3 | Dashboard styling |
| JavaScript | Frontend interaction |
| DNS, TCP, ICMP | Network measurements |
| JSON | Diagnostic reports |
| Pytest | Automated testing |
| Git and GitHub | Version control |
| Render | Deployment |

## 5. Project Structure

- backend/main.py
- backend/simulations.py
- src/diagnostics.py
- src/network_probes.py
- src/report_generator.py
- frontend/index.html
- frontend/dashboard.html
- frontend/css/style.css
- frontend/js/api.js
- frontend/js/app.js
- frontend/js/diagnostics.js
- frontend/js/simulations.js
- tests/

## 6. Implemented Features

### Network Diagnostics
- Host reachability checks.
- DNS resolution and lookup-time measurement.
- TCP connection establishment and timing.
- ICMP packet-loss measurement where supported.

### Explainable Diagnostic Engine

The system uses deterministic, rule-based inference, not machine learning.

Each finding includes:
- Finding description.
- Severity classification.
- Supporting evidence.
- Possible causes.
- Recommended corrective action.
- Evidence interpretation.
- Qualitative confidence assessment.

Confidence represents evidence strength, not statistical probability.

### Diagnostic Status

| Status | Meaning |
|---|---|
| NO_ISSUES_DETECTED | No issue detected in available measurements |
| ISSUES_DETECTED | Evidence indicates potential problems |
| INCONCLUSIVE | Insufficient evidence for reliable diagnosis |

### Fault Simulation

| Scenario | Simulated condition |
|---|---|
| DNS Failure | DNS resolution failure |
| TCP Failure | TCP connection failure |
| Packet Loss | Simulated 60% packet loss |

Simulations do not modify the user's real network.

## 7. REST API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/simulations | Lists simulations |
| POST | /api/simulations/dns_failure | DNS failure simulation |
| POST | /api/simulations/tcp_failure | TCP failure simulation |
| POST | /api/simulations/packet_loss | Packet-loss simulation |

Unknown scenarios return HTTP 400.

## 8. Testing and Validation

Automated testing uses Pytest.

Run: python -m pytest .\tests -v

Latest recorded result: 6 tests passed.

Tests cover response structure, network information, insufficient evidence, DNS failure, partial TCP failure and healthy network classification.

## 9. Local Setup

Prerequisites: Python, Git and a code editor.

Clone the repository:
git clone https://github.com/aiori-hackathon/A3-PS015-TC241.git

Install dependencies:
pip install -r requirements.txt

Start the backend:
uvicorn backend.main:app --reload

Local API documentation:
http://127.0.0.1:8000/docs

## 10. Live Deployment

- GitHub: https://github.com/aiori-hackathon/A3-PS015-TC241
- Website: https://a3-ps015-tc241.onrender.com
- Dashboard: https://a3-ps015-tc241.onrender.com/dashboard.html
- API documentation: https://a3-ps015-tc241.onrender.com/docs

Deployment platform: Render.

Latest recorded application deployment: 2b34ac4.

## 11. Technical Limitations

- ICMP measurements depend on permissions and executable availability.
- The Render environment lacked the ping executable during recorded tests.
- Browser security and CORS restrictions limit certain cross-origin HTTP probes.
- TCP connection time is not equivalent to round-trip time, throughput or webpage loading time.
- Failed probes do not always identify the exact root cause.
- Gateway-level diagnosis and loaded-latency measurement are not implemented.

Unavailable measurements must not be interpreted as zero.

## 12. Future Enhancements

These are proposed, not completed:
- Gateway and router diagnostics.
- Loaded-latency and jitter measurement.
- Scheduled network monitoring.
- Historical telemetry storage.
- Performance trend visualization.
- More detailed fault localization.
- Automated escalation reports.

## 13. Conclusion

CONNECTIQ combines active network probing, telemetry collection, explainable rule-based inference and structured diagnostic reporting to make network troubleshooting easier to understand.

**Project:** CONNECTIQ
**Hackathon:** AIORI-3
**Problem Statement:** PS-015
**Team:** CONNECTIQ
