const API_BASE_URL = window.location.origin;

async function checkBackend() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) throw new Error("Backend health check failed");
        return await response.json();
    } catch (error) {
        console.error("Backend connection error:", error);
        return null;
    }
}

async function sendDiagnostics(measurements) {
    const response = await fetch(`${API_BASE_URL}/api/diagnostics`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(measurements)
    });

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
}

function downloadDiagnosticReport(reportUrl, filename) {
    const link = document.createElement("a");
    link.href = `${API_BASE_URL}${reportUrl}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
}

