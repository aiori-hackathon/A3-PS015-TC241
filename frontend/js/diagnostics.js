document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("start-diagnosis");
    const hostnameInput = document.getElementById("hostname");

    if (!button || !hostnameInput) {
        console.error("Dashboard elements not found.");
        return;
    }

    button.addEventListener("click", runBrowserDiagnostics);
});

async function runBrowserDiagnostics() {
    const button = document.getElementById("start-diagnosis");
    const hostname = document.getElementById("hostname").value.trim();

    const reachability = document.getElementById("reachability");
    const responseTime = document.getElementById("response-time");
    const status = document.getElementById("diagnosis-status");
    const message = document.getElementById("diagnosis-message");

    const hostnamePattern = /^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)(?:\.(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?))*$/;

    if (!hostnamePattern.test(hostname)) {
        message.textContent = "Enter a valid hostname, such as google.com.";
        return;
    }

    button.disabled = true;
    button.textContent = "Running Diagnostics...";

    reachability.textContent = "Testing";
    responseTime.textContent = "Measuring";
    status.textContent = "PENDING";
    message.textContent = "Running network measurements. Please wait.";

    const measurements = {
        hostname,
        http_reachable: null,
        http_response_time_ms: null,
        browser_error: null
    };

    try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 8000);
        const startTime = performance.now();

        try {
            const response = await fetch(`https://${hostname}/`, {
                method: "GET",
                mode: "cors",
                cache: "no-store",
                signal: controller.signal
            });

            measurements.http_response_time_ms =
                Number((performance.now() - startTime).toFixed(2));

            measurements.http_reachable = response.ok;
        } finally {
            clearTimeout(timeout);
        }
    } catch (error) {
        measurements.browser_error =
            error.name === "AbortError"
                ? "TIMEOUT"
                : "CORS_OR_NETWORK_ERROR";
    }

    if (measurements.http_reachable === true) {
        reachability.textContent = "HTTP Reachable";
        responseTime.textContent =
            `${measurements.http_response_time_ms} ms`;
    } else if (measurements.http_reachable === false) {
        reachability.textContent = "HTTP Response Received";
        responseTime.textContent =
            `${measurements.http_response_time_ms} ms`;
    } else {
        reachability.textContent = "Unknown";
        responseTime.textContent = "Unavailable";
    }

    try {
        const result = await sendDiagnostics(measurements);

        status.textContent = result.diagnosis_status;
       setText("diagnosis-severity", result.severity ?? "UNKNOWN");
        message.textContent = result.message;

        displayBackendMeasurements(result.backend_measurements);
        displayFindings(result.findings);
        displayLimitations(result.limitations);

        if (result.report_url && result.report_filename) {
            const reportButton = document.getElementById("download-report");
            const reportStatus = document.getElementById("report-status");
            const reportFilename = document.getElementById("report-filename");

            if (reportButton) {
                reportButton.href = `${API_BASE_URL}${result.report_url}`;
                reportButton.download = result.report_filename;
                reportButton.hidden = false;
            }

            if (reportStatus) {
                reportStatus.textContent = "Report generated successfully.";
            }

            if (reportFilename) {
                reportFilename.textContent = `Report filename: ${result.report_filename}`;
            }



            message.textContent +=
                " Your diagnostic report has been generated and is ready to download.";
        }

    } catch (error) {
        status.textContent = "BACKEND ERROR";
        message.textContent =
            "Could not receive the diagnosis or generate the report.";
        console.error("Diagnosis error:", error);
    } finally {
        button.disabled = false;
        button.textContent = "Run Diagnosis";
    }
}

function displayBackendMeasurements(data) {
    if (!data) return;

    setText("network-status", data.network?.status ?? "Unavailable");
    setText("network-latency", formatMs(data.network?.latency_ms));

    setText("dns-status", data.dns?.status ?? "Unavailable");
    setText("dns-time", formatMs(data.dns?.dns_lookup_ms));

    setText(
        "tcp-status",
        data.tcp
            ? `${data.tcp.successful_attempts}/${data.tcp.attempts} successful`
            : "Unavailable"
    );

    setText("tcp-average", formatMs(data.tcp?.average_latency_ms));
    setText("tcp-min", formatMs(data.tcp?.min_latency_ms));
    setText("tcp-max", formatMs(data.tcp?.max_latency_ms));

    setText("icmp-status", data.icmp?.status ?? "Unavailable");

    setText(
        "packet-loss",
        data.icmp?.packet_loss_percent == null
            ? "Unavailable"
            : `${data.icmp.packet_loss_percent}%`
    );
}

function displayFindings(findings) {
    const container = document.getElementById("diagnostic-findings");
    if (!container) return;

    container.replaceChildren();

    if (!findings || findings.length === 0) {
        const item = document.createElement("p");
        item.textContent = "No configured warning conditions detected.";
        container.appendChild(item);
        return;
    }

    findings.forEach((finding) => {
        const card = document.createElement("article");
        const heading = document.createElement("h3");
        const severity = document.createElement("p");
        const evidence = document.createElement("p");
        const causesHeading = document.createElement("h4");
        const causesList = document.createElement("ul");
        const recommendationsHeading = document.createElement("h4");
        const recommendationsList = document.createElement("ul");

        heading.textContent = finding.finding ?? "Diagnostic finding";
        severity.textContent = `Severity: ${finding.severity ?? "UNKNOWN"}`;
        evidence.textContent = `Evidence: ${finding.evidence ?? "Unavailable"}`;

        causesHeading.textContent = "Possible causes";
        (finding.possible_causes || []).forEach((cause) => {
            const item = document.createElement("li");
            item.textContent = cause;
            causesList.appendChild(item);
        });

        recommendationsHeading.textContent = "Recommended actions";
        const recommendations = Array.isArray(finding.recommendation)
            ? finding.recommendation
            : [finding.recommendation].filter(Boolean);

        recommendations.forEach((recommendation) => {
            const item = document.createElement("li");
            item.textContent = recommendation;
            recommendationsList.appendChild(item);
        });

        card.append(
            heading,
            severity,
            evidence,
            causesHeading,
            causesList,
            recommendationsHeading,
            recommendationsList
        );

        container.appendChild(card);
    });
}
function displayLimitations(limitations) {
    const container = document.getElementById("diagnostic-limitations");
    if (!container) return;

    container.replaceChildren();

    (limitations || []).forEach((limitation) => {
        const item = document.createElement("li");
        item.textContent = limitation;
        container.appendChild(item);
    });
}

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
}

function formatMs(value) {
    return value == null ? "Unavailable" : `${value} ms`;
}




