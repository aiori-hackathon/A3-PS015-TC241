# CONNECTIQ
### Explainable Home and Last-Mile Connectivity Diagnosis

**AIORI-3 Hackathon | Problem Statement: PS-015**

**Team:** CONNECTIQ

**Repository:** [A3-PS015-TC241](https://github.com/aiori-hackathon/A3-PS015-TC241)

---

## 1. Project Overview

CONNECTIQ is a network diagnostics platform designed to identify and explain connectivity problems affecting home and last-mile internet connections.

It combines browser-based measurements with Python backend network probes to evaluate connectivity, DNS resolution, TCP connection performance and ICMP packet loss.

The system uses a transparent, rule-based diagnosis engine to interpret collected measurements, identify warning conditions, suggest possible causes and recommend troubleshooting actions.

Its objective is to make network troubleshooting easier to understand through measurable evidence and explainable results.

## 2. Problem Statement

**PS-015: Explainable Home and Last-Mile Connectivity Diagnosis**

Users often experience:
- Slow internet connections.
- Intermittent connectivity.
- DNS resolution failures.
- High connection delays.
- Packet loss.
- Unstable network performance.

Traditional troubleshooting tools often provide raw technical measurements without explaining their meaning.

CONNECTIQ addresses this problem by collecting network measurements and presenting understandable diagnostic results.

## 3. Objectives

- Measure internet reachability.
- Check DNS resolution.
- Measure TCP connection setup time.
- Estimate ICMP packet loss.
- Identify possible network issues.
- Explain findings using evidence.
- Recommend practical troubleshooting actions.
- Generate downloadable diagnostic reports.
- Provide a simple web-based dashboard.

## 4. Key Features

### 4.1 Network Reachability
Checks whether the selected hostname accepts a TCP connection on the configured port.

### 4.2 DNS Resolution
Measures DNS lookup time and retrieves resolved IP addresses.

### 4.3 TCP Connectivity
Performs repeated TCP connection attempts and calculates:
- Successful attempts.
- Failed attempts.
- Average connection setup time.
- Minimum connection setup time.
- Maximum connection setup time.

### 4.4 ICMP Packet Loss
Uses the operating system's ping utility to estimate packet loss.

### 4.5 Explainable Diagnosis Engine
Uses rule-based logic to classify results:

| Diagnosis | Meaning |
|---|---|
| NO_ISSUES_DETECTED | No configured warning conditions detected |
| ISSUES_DETECTED | One or more warning conditions observed |
| INCONCLUSIVE | Insufficient valid measurements |

Severity levels:

- HIGH
- MEDIUM
- LOW
- NONE
- UNKNOWN

The engine also provides:
- Measurement evidence.
- Possible causes.
- Recommended troubleshooting actions.
- Diagnostic limitations.

### 4.6 Diagnostic Reports
Generates downloadable JSON reports containing diagnostic measurements and findings.

### 4.7 Web Dashboard
Provides a responsive interface to:
- Enter a hostname.
- Start diagnostics.
- View measurement results.
- Understand detected issues.
- Download diagnostic reports.

## 5. System Architecture

```text
                 USER
                   |
                   v
          CONNECTIQ WEB DASHBOARD
             HTML / CSS / JS
                   |
          Browser Measurements
          HTTP Reachability
          HTTP Response Time
                   |
                   v
             FASTAPI BACKEND
                   |
          ---------------------
          |         |         |
          v         v         v
         DNS       TCP      ICMP
        Probe     Probe     Probe
          |         |         |
          ---------------------
                   |
                   v
           TELEMETRY RESULTS
                   |
                   v
          DIAGNOSIS ENGINE
          Rule-Based Analysis
                   |
          ---------------------
          |         |         |
          v         v         v
       Findings  Severity  Recommendations
          |         |         |
          ---------------------
                   |
                   v
           REPORT GENERATOR
                   |
                   v
          DOWNLOADABLE JSON
```

## 6. Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML5 |
| Styling | CSS3 |
| Browser logic | JavaScript |
| Backend | Python |
| API framework | FastAPI |
| API server | Uvicorn |
| Network measurements | Python socket and OS ping |
| Data format | JSON |
| Testing | Pytest |
| Version control | Git and GitHub |

## 7. Project Folder Structure

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
└── .gitignore
```

## 8. Installation and Setup

### Requirements

- Windows, Linux or macOS.
- Python 3.10 or later recommended.
- Git.
- VS Code or another code editor.
- Internet connection for external network tests.

### Step 1: Clone the Repository

```bash
git clone https://github.com/aiori-hackathon/A3-PS015-TC241.git
```

### Step 2: Open the Project Folder

```bash
cd A3-PS015-TC241
```

### Step 3: Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
```

### Step 4: Activate the Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Start the Backend Server

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 7: Open the Application

Open the following address in your browser:

```text
http://127.0.0.1:8000
```

Dashboard:

```text
http://127.0.0.1:8000/dashboard.html
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 9. How to Use CONNECTIQ

1. Start the FastAPI backend.
2. Open the CONNECTIQ dashboard.
3. Enter a valid hostname, such as `google.com`.
4. Click Run Diagnosis.
5. Wait for the measurements to complete.
6. Review HTTP reachability and response time.
7. Review DNS, TCP and ICMP measurements.
8. Read the overall diagnosis and severity.
9. Review possible causes and recommended actions.
10. Download the generated diagnostic report.

## 10. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application homepage |
| GET | `/health` | Backend health check |
| POST | `/api/diagnostics` | Submit diagnostic measurements |
| GET | `/api/reports/{filename}` | Download a diagnostic report |
| GET | `/docs` | Interactive API documentation |

### Example Health Check

Request:

```http
GET /health
```

### Example Diagnostic Request

```json
{
  "hostname": "google.com",
  "http_reachable": true,
  "http_response_time_ms": 120.5,
  "browser_error": null
}
```

The backend performs its configured network probes and returns diagnostic results.

## 11. Diagnosis Methodology

CONNECTIQ uses a transparent rule-based inference engine.

It evaluates:

1. Target reachability.
2. DNS resolution.
3. ICMP packet loss.
4. TCP connection failures.
5. TCP connection setup time.

The engine uses the available measurements to determine whether warning conditions exist.

Possible outputs include:

- NO_ISSUES_DETECTED
- ISSUES_DETECTED
- INCONCLUSIVE

The engine reports possible causes rather than claiming a confirmed root cause.

## 12. Testing

The project uses Pytest for automated testing.

Run all tests:

```powershell
python -m pytest -v
```

Check Python syntax:

```powershell
python -m py_compile .\backend\main.py .\src\diagnostics.py
```

### Current Test Results

**Latest recorded test run: 6 passed.**

The tests cover:
- System and network diagnostic output.
- Insufficient measurement handling.
- High-severity DNS failure.
- Medium-severity partial TCP failures.
- No-warning-condition diagnosis.
- System information fields.

## 13. Technical Limitations

CONNECTIQ reports only what its configured measurements support.

Important limitations:

- Browser JavaScript does not provide unrestricted ICMP access.
- Browser-based HTTP requests are affected by CORS and browser security policies.
- TCP connection setup time is not the same as pure round-trip latency.
- ICMP packet loss can be affected by firewall filtering and rate limiting.
- A failed connection to a public hostname does not prove the home gateway is down.
- Loaded latency and jitter require dedicated measurements.
- Possible causes are diagnostic hypotheses, not confirmed root causes.
- Results from a public endpoint do not fully characterize every device or segment of a home network.

## 14. Security Considerations

Before public deployment, the application requires production security checks, including:

- Strict hostname and destination IP validation.
- Protection against private-network and loopback address access.
- DNS rebinding protection.
- Request rate limiting.
- Connection and execution timeouts.
- Restricted CORS origins.
- HTTPS deployment.
- Safe report filename validation.
- Controlled report storage and access.

The local development server is not intended for unrestricted public exposure.

## 15. Future Enhancements

Planned improvements include:

1. Scheduled network measurements.
2. Multiple diagnostic endpoints.
3. Loaded latency measurement.
4. Jitter calculation.
5. Improved gateway and local-network diagnostics.
6. Network congestion testing.
7. Historical performance tracking.
8. Graphical measurement trends.
9. Enhanced PDF reports.
10. Public cloud deployment.
11. Improved root-cause inference.
12. User-friendly troubleshooting guidance.

## 16. Expected Impact

CONNECTIQ aims to help users understand connectivity problems through:
- Measurable network evidence.
- Transparent diagnostic decisions.
- Understandable explanations.
- Practical troubleshooting recommendations.
- Downloadable reports.

The platform is designed to support explainable network troubleshooting for home and last-mile connectivity.

## 17. Team Information

**Team Name:** CONNECTIQ

**Event:** AIORI-3 Hackathon

**Problem Statement:** PS-015

**Project Title:** Explainable Home and Last-Mile Connectivity Diagnosis

**GitHub Repository:**

https://github.com/aiori-hackathon/A3-PS015-TC241

## 18. License

Add the appropriate license after confirming the project's ownership and hackathon requirements.

---

**CONNECTIQ**

*Making network diagnostics measurable, understandable and explainable.*
