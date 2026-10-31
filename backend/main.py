from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
from datetime import datetime
import re
import ipaddress
import socket

from src.network_probes import (
    check_hostname,
    measure_dns_response,
    measure_tcp_latency,
    measure_icmp_packet_loss,
)
from src.diagnostics import diagnose_network
from src.report_generator import save_report

app = FastAPI(
    title="CONNECTIQ API",
    description="Explainable Home and Last-Mile Connectivity Diagnosis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_public_hostname(hostname: str):
    try:
        addresses = socket.getaddrinfo(
            hostname,
            443,
            type=socket.SOCK_STREAM
        )
    except socket.gaierror:
        raise HTTPException(
            status_code=400,
            detail="Hostname could not be resolved."
        )

    resolved_ips = {
        item[4][0].split("%")[0]
        for item in addresses
    }

    if not resolved_ips:
        raise HTTPException(
            status_code=400,
            detail="No IP addresses found for hostname."
        )

    for address in resolved_ips:
        ip = ipaddress.ip_address(address)

        if not ip.is_global:
            raise HTTPException(
                status_code=400,
                detail="Private or non-public network targets are not allowed."
            )

    return resolved_ips

class BrowserDiagnostics(BaseModel):
    hostname: str = Field(default="google.com", min_length=1, max_length=253)
    http_reachable: Optional[bool] = None
    http_response_time_ms: Optional[float] = Field(default=None, ge=0)
    browser_error: Optional[str] = None


@app.get("/")
def home():
    frontend_file = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
    return FileResponse(frontend_file, media_type="text/html")


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "CONNECTIQ FastAPI Backend"
    }


@app.post("/api/diagnostics")
def receive_diagnostics(data: BrowserDiagnostics):
    hostname = data.hostname.strip()

    if not re.fullmatch(
        r"(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)(?:\.(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?))*",
        hostname
    ):
        raise HTTPException(
            status_code=400,
            detail="Enter a valid hostname."
        )

    validate_public_hostname(hostname)

    try:
        network = check_hostname(hostname, port=443)
        dns = measure_dns_response(hostname)
        tcp = measure_tcp_latency(hostname, port=443, count=5)
        icmp = measure_icmp_packet_loss(hostname, count=4)

        diagnosis = diagnose_network(network, dns, tcp, icmp)

        timestamp = datetime.now().astimezone().isoformat()

        report_data = {
            "project": "CONNECTIQ",
            "team": "CONNECTIQ",
            "generated_at": timestamp,
            "hostname": hostname,
            "browser_measurements": {
                "http_reachable": data.http_reachable,
                "http_response_time_ms": data.http_response_time_ms,
                "browser_error": data.browser_error
            },
            "backend_measurements": {
                "network": network,
                "dns": dns,
                "tcp": tcp,
                "icmp": icmp
            },
            "diagnosis": diagnosis
        }

        report_path = save_report(report_data)

        return {
            "project": "CONNECTIQ",
            "received": True,
            "hostname": hostname,
            "generated_at": timestamp,
            "browser_measurements": report_data["browser_measurements"],
            "backend_measurements": report_data["backend_measurements"],
            "diagnosis_status": diagnosis["status"],
            "severity": diagnosis["severity"],
            "message": diagnosis["summary"],
            "evidence_count": diagnosis["evidence_count"],
            "findings": diagnosis["findings"],
            "limitations": diagnosis["limitations"],
            "report_filename": report_path.name,
            "report_url": f"/api/reports/{report_path.name}"
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Diagnostic execution or report generation failed: {str(exc)}"
        )


@app.get("/api/reports/{filename}")
def download_report(filename: str):
    if not re.fullmatch(r"report_[0-9]{8}_[0-9]{6}\.json", filename):
        raise HTTPException(status_code=400, detail="Invalid report filename.")

    reports_dir = Path(__file__).resolve().parent.parent / "reports"
    report_path = reports_dir / filename

    if not report_path.is_file():
        raise HTTPException(status_code=404, detail="Report not found.")

    return FileResponse(
        path=report_path,
        media_type="application/json",
        filename=filename
    )





# Serve the CONNECTIQ frontend through FastAPI
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")



