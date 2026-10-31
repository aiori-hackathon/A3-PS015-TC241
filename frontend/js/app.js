document.addEventListener("DOMContentLoaded", async () => {
    const statusElement = document.getElementById("backend-status");

    if (!statusElement) return;

    const result = await checkBackend();

    if (result) {
        statusElement.textContent = "Backend Connected";
        statusElement.className = "connection-status connected";
    } else {
        statusElement.textContent = "Backend Offline";
        statusElement.className = "connection-status disconnected";
    }
});
