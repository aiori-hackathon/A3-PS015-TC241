# CONNECTIQ
## Project Technical Documentation

**Project Title:** Explainable Home and Last-Mile Connectivity Diagnosis  
**Hackathon:** AIORI-3  
**Problem Statement:** PS-015  
**Team Name:** CONNECTIQ  
**Repository:** https://github.com/aiori-hackathon/A3-PS015-TC241  
**Technology:** Python, FastAPI, HTML, CSS, JavaScript

---

# 1. Introduction

CONNECTIQ is a web-based network diagnostic platform developed to identify, analyze and explain connectivity problems affecting home and last-mile internet networks.

Internet users frequently experience slow connectivity, DNS failures, intermittent connections and packet loss. Conventional troubleshooting tools often display technical measurements without explaining their meaning or suggesting corrective actions.

CONNECTIQ addresses this challenge through browser-based measurements, backend network probes and an explainable rule-based diagnosis engine.

The platform collects network measurements, analyzes the results and generates diagnostic findings with possible causes and recommended troubleshooting actions.

# 2. Problem Definition

## 2.1 Problem Statement

Explainable Home and Last-Mile Connectivity Diagnosis.

The main problem is the difficulty users face when identifying the reasons behind poor internet connectivity.

Common connectivity problems include:

- Internet connection failure.
- DNS resolution failure.
- High connection setup time.
- Packet loss.
- Intermittent connectivity.
- Network instability.
- Remote service unavailability.

## 2.2 Proposed Solution

CONNECTIQ provides a centralized dashboard that collects network measurements and processes them through a Python backend.

The system evaluates the collected evidence and produces an understandable diagnostic report.

The proposed solution focuses on:

1. Network measurement.
2. Telemetry collection.
3. Rule-based inference.
4. Explainable findings.
5. Severity classification.
6. Troubleshooting recommendations.
7. Diagnostic report generation.

# 3. Project Objectives

The primary objectives are:

- Develop a simple web-based network diagnostic platform.
- Measure HTTP reachability and response time.
- Perform DNS resolution checks.
- Measure TCP connection setup time.
- Estimate ICMP packet loss.
- Identify connectivity warning conditions.
- Generate explainable diagnostic findings.
- Classify issue severity.
- Recommend troubleshooting actions.
- Generate downloadable JSON reports.
- Provide a foundation for scheduled and multi-endpoint diagnostics.

# 4. Proposed System Architecture

The system follows a frontend-backend architecture.

## 4.1 Architecture Diagram

```text
                   USER
                     |
                     v
            CONNECTIQ WEB INTERFACE
                     |
              HTML / CSS / JS
                     |
          -------------------------
          |                       |
          v                       v
    HTTP Reachability       HTTP Response Time
          |                       |
          -----------+-------------
                     |
                     v
              FASTAPI BACKEND
                     |
          -------------------------
          |           |           |
          v           v           v
        DNS         TCP         ICMP
       PROBE       PROBE       PROBE
          |           |           |
          -----------+-------------
                     |
                     v
             TELEMETRY COLLECTOR
                     |
                     v
              DIAGNOSIS ENGINE
                     |
          -------------------------
          |           |           |
          v           v           v
       FINDINGS    SEVERITY   RECOMMENDATIONS
          |           |           |
          -----------+-------------
                     |
                     v
             REPORT GENERATOR
                     |
                     v
              JSON REPORT
                     |
                     v
                USER
```

## 4.2 Architecture Components

### A. Frontend Layer

Technologies:
- HTML5
- CSS3
- JavaScript

Responsibilities:
- Accept hostname input.
- Start diagnostic tests.
- Perform browser-based HTTP measurements.
- Communicate with the backend API.
- Display measurement results.
- Display diagnostic findings.
- Provide report download functionality.

### B. Backend Layer

Technology: Python with FastAPI.

Responsibilities:
- Receive browser measurements.
- Validate diagnostic requests.
- Execute network probes.
- Process measurement results.
- Generate diagnostic responses.
- Save reports.

### C. Network Probe Layer

The network probe module performs:

- DNS resolution.
- TCP connection measurements.
- ICMP packet-loss measurements.
- Basic hostname reachability checks.
- System information collection.

### D. Diagnosis Engine

The diagnosis engine applies transparent rule-based conditions to collected measurements.

It identifies warning conditions and produces:

- Diagnosis status.
- Overall severity.
- Evidence.
- Possible causes.
- Recommended actions.
- Diagnostic limitations.

### E. Report Generator

The report generator saves diagnostic results in JSON format.

Reports include measurement data, diagnosis results and supporting findings.

# 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| Uvicorn | Backend server |
| HTML5 | Webpage structure |
| CSS3 | Interface design |
| JavaScript | Browser interactions |
| Python Socket | DNS and TCP measurements |
| OS Ping Utility | ICMP packet-loss measurement |
| JSON | Diagnostic report format |
| Pytest | Automated testing |
| Git | Version control |
| GitHub | Repository management |

# 6. Functional Modules

## 6.1 Browser Diagnostics Module

File: `frontend/js/diagnostics.js`

This module performs browser-based measurements.

It collects:

- Target hostname.
- HTTP reachability.
- HTTP response time.
- Browser error information.

The browser uses JavaScript Fetch API to request the target endpoint.

The system records the elapsed time using the browser performance clock.

Browser restrictions such as CORS and network policies affect these measurements.

A failed browser request does not automatically prove the target server is offline.

## 6.2 API Communication Module

File: `frontend/js/api.js`

This module connects the frontend to the FastAPI backend.

Responsibilities:

- Send diagnostic measurements.
- Receive backend results.
- Check backend availability.
- Access generated reports.

The API base URL follows the current application origin.

## 6.3 Network Probe Module

File: `src/network_probes.py`

This module performs backend network measurements.

### DNS Measurement

Uses Python socket functions to resolve the target hostname.

Collected information:

- DNS status.
- DNS lookup time.
- Resolved IP addresses.
- Error information.

### TCP Measurement

Attempts repeated TCP connections to the target service.

Collected information:

- Number of attempts.
- Successful attempts.
- Failed attempts.
- Average connection setup time.
- Minimum connection setup time.
- Maximum connection setup time.

TCP connection setup time is not equivalent to pure round-trip latency.

### ICMP Measurement

Uses the operating system's ping utility.

Collected information:

- ICMP test status.
- Number of packets sent.
- Packet-loss percentage.
- Measurement errors.

ICMP filtering and rate limiting can affect the results.

### System Information

Collects basic system information, including:

- Operating system.
- Operating system version.
- Python version.
- Hostname.

## 6.4 Diagnosis Engine

File: `src/diagnostics.py`

The diagnosis engine evaluates collected measurements.

### Diagnostic Rules

| Rule | Measurement | Purpose |
|---|---|---|
| Rule 1 | Target reachability | Identify connection failures |
| Rule 2 | DNS resolution | Identify lookup failures |
| Rule 3 | ICMP packet loss | Identify packet-loss warnings |
| Rule 4 | TCP failures | Identify unsuccessful connection attempts |
| Rule 5 | TCP setup time | Identify unusually high connection times |

### Diagnosis Status

The system produces three primary statuses.

**NO_ISSUES_DETECTED**

No configured warning conditions were detected in the available measurements.

**ISSUES_DETECTED**

One or more configured warning conditions were observed.

**INCONCLUSIVE**

The available evidence is insufficient to produce a reliable assessment.

### Severity Classification

The system classifies findings into:

- HIGH
- MEDIUM
- LOW
- NONE
- UNKNOWN

Severity depends on the configured diagnostic rules and thresholds.

These thresholds are application heuristics, not universal networking standards.

### Explainable Findings

Each finding includes:

1. Finding title.
2. Severity.
3. Supporting evidence.
4. Possible causes.
5. Recommended troubleshooting actions.

The system reports possible causes as hypotheses. It does not claim to confirm the exact root cause.

# 7. Diagnostic Workflow

The complete workflow is:

1. User opens the CONNECTIQ dashboard.
2. User enters a hostname.
3. Browser validates the hostname format.
4. Browser performs an HTTP reachability measurement.
5. Browser calculates HTTP response time when available.
6. Browser sends measurements to the FastAPI backend.
7. Backend validates the request and target.
8. Backend performs DNS measurements.
9. Backend performs repeated TCP connection tests.
10. Backend estimates ICMP packet loss.
11. Telemetry results are collected.
12. Diagnosis engine evaluates the measurements.
13. System classifies the diagnosis and severity.
14. Possible causes and recommendations are generated.
15. Diagnostic report is saved.
16. Dashboard displays the results.
17. User downloads the report when required.

# 8. Project Directory Structure

```text
CONNECTIQ/
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── app.js
│       ├── api.js
│       └── diagnostics.js
│
├── src/
│   ├── __init__.py
│   ├── diagnostics.py
│   ├── network_probes.py
│   └── report_generator.py
│
├── tests/
│   ├── test_diagnostics.py
│   └── test_network_probes.py
│
├── reports/
│
├── requirements.txt
├── README.md
└── PROJECT_DOCUMENTATION.md
```

# 9. Installation and Execution

## 9.1 System Requirements

- Windows, Linux or macOS.
- Python 3.10 or later recommended.
- Git.
- Visual Studio Code.
- Internet connection.

## 9.2 Clone Repository

```bash
git clone https://github.com/aiori-hackathon/A3-PS015-TC241.git
```

## 9.3 Open Project

```bash
cd A3-PS015-TC241
```

## 9.4 Create Virtual Environment

```powershell
python -m venv .venv
```

## 9.5 Activate Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

## 9.6 Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 9.7 Start Backend

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

## 9.8 Open Application

Homepage:

`http://127.0.0.1:8000`

Dashboard:

`http://127.0.0.1:8000/dashboard.html`

API documentation:

`http://127.0.0.1:8000/docs`

# 10. API Documentation

The FastAPI application provides the following endpoints.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application homepage |
| GET | `/health` | Backend health check |
| POST | `/api/diagnostics` | Execute diagnostic workflow |
| GET | `/api/reports/{filename}` | Download diagnostic report |
| GET | `/docs` | Interactive API documentation |

## 10.1 Diagnostic Request Example

```json
{
  "hostname": "google.com",
  "http_reachable": true,
  "http_response_time_ms": 120.5,
  "browser_error": null
}
```

## 10.2 Diagnostic Response

The API returns information such as:

- Project name.
- Target hostname.
- Measurement timestamp.
- Browser measurements.
- Backend measurements.
- Diagnosis status.
- Overall severity.
- Evidence count.
- Diagnostic findings.
- Limitations.
- Report filename.
- Report download URL.

The exact response fields follow the current backend implementation.

# 11. Testing and Validation

CONNECTIQ uses Pytest for automated testing.

### Run Automated Tests

```powershell
python -m pytest -v
```

### Check Python Syntax

```powershell
python -m py_compile .\backend\main.py .\src\diagnostics.py
```

### Current Verified Test Results

Latest recorded test run:

**6 tests passed.**

The tests cover:

| Test | Expected Result |
|---|---|
| System and network diagnostic output | PASSED |
| Insufficient evidence | PASSED |
| High-severity DNS failure | PASSED |
| Medium-severity partial TCP failures | PASSED |
| No warning conditions | PASSED |
| System information fields | PASSED |

These results represent the latest recorded test run, not a guarantee that every deployment environment has been validated.

# 12. Security Considerations

Security is important before public deployment.

Required production improvements include:

- Strict hostname validation.
- Public destination IP validation.
- Protection against private and loopback address access.
- DNS rebinding protection.
- Request rate limiting.
- Network probe timeouts.
- Restricted CORS configuration.
- HTTPS.
- Safe report filename handling.
- Controlled report storage.

The current local development configuration must not be exposed directly to unrestricted public traffic.

# 13. Technical Limitations

The following limitations apply to the current implementation:

1. Browser JavaScript does not provide unrestricted ICMP access.
2. Browser HTTP measurements depend on CORS and browser security restrictions.
3. TCP connection setup time is not pure round-trip latency.
4. ICMP packet loss can be affected by filtering and rate limiting.
5. A failed public TCP connection does not establish that the home gateway is down.
6. Loaded jitter and congestion require dedicated measurement methods.
7. Public endpoint results do not fully characterize the entire home network.
8. Diagnostic recommendations are based on possible causes, not confirmed root causes.

# 14. Future Scope

The following enhancements are proposed for future development.

### Network Measurement Enhancements

- Loaded latency measurement.
- Jitter calculation.
- Multiple diagnostic endpoints.
- Scheduled network probes.
- Gateway reachability checks.
- Local network diagnostics.

### Dashboard Enhancements

- Historical measurement charts.
- Diagnostic trend analysis.
- Improved report visualization.
- PDF report generation.
- Mobile-friendly interface.

### Diagnosis Enhancements

- More detailed inference rules.
- Better evidence correlation.
- Confidence scoring.
- Improved root-cause localization.
- Automated troubleshooting guidance.

### Deployment Enhancements

- Public cloud hosting.
- HTTPS configuration.
- Production monitoring.
- Secure API access.
- Controlled diagnostic execution.

# 15. Expected Outcomes

CONNECTIQ aims to provide:

- Understandable network measurements.
- Transparent diagnostic decisions.
- Clear severity classification.
- Evidence-based findings.
- Practical troubleshooting recommendations.
- Downloadable diagnostic reports.

The platform provides a foundation for explainable home and last-mile connectivity diagnosis.

# 16. Conclusion

CONNECTIQ combines browser-based measurements, Python network probes and a rule-based diagnosis engine to make connectivity troubleshooting more understandable.

The platform evaluates DNS resolution, TCP connection performance, ICMP packet loss and HTTP reachability.

It converts collected measurements into structured findings, severity classifications and troubleshooting recommendations.

The project demonstrates how network measurements and explainable rule-based reasoning can support practical connectivity diagnosis.

# 17. Project Information

**Project:** CONNECTIQ  
**Hackathon:** AIORI-3  
**Problem Statement:** PS-015  
**Project Title:** Explainable Home and Last-Mile Connectivity Diagnosis  
**GitHub Repository:** https://github.com/aiori-hackathon/A3-PS015-TC241

---

**CONNECTIQ**

*Making Network Diagnostics Measurable, Understandable and Explainable.*
