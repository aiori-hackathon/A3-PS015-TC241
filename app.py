
import streamlit as st
from src.diagnostics import run_diagnostics
from src.report_generator import save_report

st.set_page_config(
    page_title="CONNECTIQ",
    page_icon="🌐",
    layout="centered",
)

st.title("🌐 CONNECTIQ")
st.subheader("Network Diagnostics Dashboard")

st.write("Check basic network connectivity from this computer.")

hostname = st.text_input("Hostname", value="google.com")
port = st.number_input(
    "TCP port",
    min_value=1,
    max_value=65535,
    value=443,
)

if st.button("Run Diagnostics"):
    if not hostname.strip():
        st.error("Please enter a hostname.")
    else:
        with st.spinner("Checking connection..."):
            result = run_diagnostics(hostname.strip(), int(port))

        st.subheader("System Information")
        st.json(result["system"])

        st.subheader("Network Result")
        network = result["network"]

        if network["status"] == "Online":
            st.success(f'{hostname} is reachable')
            st.metric("Connection latency", f'{network["latency_ms"]} ms')
        else:
            st.warning(network["status"])
            st.caption(network["error"] or "")

        report_path = save_report(result)
        st.success(f"Report saved: {report_path.name}")

        st.download_button(
            "Download JSON Report",
            data=report_path.read_bytes(),
            file_name=report_path.name,
            mime="application/json",
        )