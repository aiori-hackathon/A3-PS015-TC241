
import streamlit as st

from src.diagnostics import run_diagnostics, diagnose_network
from src.report_generator import save_report
from src.network_probes import (
    measure_dns_response,
    measure_tcp_latency,
    measure_icmp_packet_loss,
)

st.set_page_config(
    page_title="CONNECTIQ",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 CONNECTIQ")
st.subheader("Network Diagnostics Dashboard")
st.write("Measure connectivity, DNS response, TCP latency, and packet loss.")

hostname = st.text_input("Hostname", value="google.com")
port = st.number_input(
    "TCP port",
    min_value=1,
    max_value=65535,
    value=443,
    step=1,
)

if st.button("Run Diagnostics", type="primary"):
    if not hostname.strip():
        st.error("Please enter a hostname.")
    else:
        host = hostname.strip()

        with st.spinner("Running network probes..."):
            try:
                
                result = run_diagnostics(host, int(port))

                dns = measure_dns_response(host)
                tcp = measure_tcp_latency(host, int(port), count=5)
                icmp = measure_icmp_packet_loss(host, count=4)

                result["probes"] = {
                    "dns": dns,
                    "tcp": tcp,
                    "icmp": icmp,
                }

                diagnosis = diagnose_network(
                    result["network"],
                    dns,
                    tcp,
                    icmp,
                )

                result["diagnosis"] = diagnosis
                st.session_state["diagnostic_result"] = result

            except Exception as exc:
                st.error(f"Diagnostics failed: {exc}")

if "diagnostic_result" in st.session_state:
    result = st.session_state["diagnostic_result"]
    network = result["network"]
    probes = result["probes"]
    dns = probes["dns"]
    tcp = probes["tcp"]
    icmp = probes["icmp"]

    st.divider()
    st.subheader("System Information")
    st.json(result["system"])

    st.subheader("Connectivity")
    if network["status"] == "Online":
        st.success(f'{network["host"]} is reachable')
    else:
        st.warning(network["status"])
        st.caption(network.get("error") or "")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "TCP connection time",
            f'{network["latency_ms"]} ms'
            if network.get("latency_ms") is not None
            else "Unavailable",
        )

    with col2:
        st.metric(
            "DNS lookup time",
            f'{dns["dns_lookup_ms"]} ms'
            if dns.get("dns_lookup_ms") is not None
            else "Unavailable",
        )

    with col3:
        loss = icmp.get("packet_loss_percent")
        st.metric(
            "ICMP packet loss",
            f"{loss}%"
            if loss is not None
            else "Unavailable",
        )

    st.subheader("Repeated TCP Measurements")

    col1, col2, col3 = st.columns(3)

    with col1:
        avg = tcp.get("average_latency_ms")
        st.metric(
            "Average latency",
            f"{avg} ms" if avg is not None else "Unavailable",
        )

    with col2:
        st.metric(
            "Minimum latency",
            f'{tcp["min_latency_ms"]} ms'
            if tcp.get("min_latency_ms") is not None
            else "Unavailable",
        )

    with col3:
        st.metric(
            "Maximum latency",
            f'{tcp["max_latency_ms"]} ms'
            if tcp.get("max_latency_ms") is not None
            else "Unavailable",
        )

    st.write(
        f'TCP attempts: {tcp["successful_attempts"]} successful, '
        f'{tcp["failed_attempts"]} failed out of {tcp["attempts"]}.'
    )

    st.caption(
        "TCP connection time includes connection setup overhead. "
        "It is not a pure round-trip-time measurement."
    )
    
    st.divider()
    st.subheader("🧠 Explainable Diagnosis")

    diagnosis = result["diagnosis"]
    status = diagnosis["status"]

    if status == "NO_ISSUES_DETECTED":
        st.success(diagnosis["summary"])
    elif status == "INCONCLUSIVE":
        st.warning(diagnosis["summary"])
    else:
        st.error(diagnosis["summary"])

    st.write(f"Valid evidence checks: {diagnosis['evidence_count']}")

    if diagnosis["findings"]:
        st.markdown("### Findings and Recommended Actions")

        for item in diagnosis["findings"]:
            with st.expander(item["finding"]):
                st.write("**Evidence:**", item["evidence"])
                st.write("**Recommended action:**", item["recommendation"])
    else:
        st.info("No configured warning conditions were detected.")

    with st.expander("Diagnosis limitations"):
        for limitation in diagnosis["limitations"]:
            st.write(f"- {limitation}")

    with st.expander("View detailed probe results"):
        st.write("DNS results")
        st.json(dns)

        st.write("TCP results")
        st.json(tcp)

        st.write("ICMP results")
        st.json(icmp)

    report_path = save_report(result)
    st.success(f"Report saved: {report_path.name}")

    st.download_button(
        "Download JSON Report",
        data=report_path.read_bytes(),
        file_name=report_path.name,
        mime="application/json",
    )
