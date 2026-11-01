document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".simulation-option");
    const runButton = document.getElementById("run-simulation");
    const status = document.getElementById("simulation-status");
    const results = document.getElementById("simulation-results");

    if (!runButton || !status || !results) {
        console.error("Simulation interface elements are missing.");
        return;
    }

    let selectedScenario = "dns_failure";

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            selectedScenario = button.dataset.scenario;

            buttons.forEach(item => item.classList.remove("selected"));
            button.classList.add("selected");

            status.textContent = `Selected scenario: ${selectedScenario}`;
            results.hidden = true;
        });
    });

    runButton.addEventListener("click", async () => {
        runButton.disabled = true;
        status.textContent = "Running simulation...";
        results.hidden = true;

        try {
            const response = await fetch(
                `/api/simulations/${encodeURIComponent(selectedScenario)}`,
                { method: "POST" }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Simulation failed.");
            }

            document.getElementById("sim-status").textContent =
                data.diagnosis.status;

            document.getElementById("sim-severity").textContent =
                data.diagnosis.severity;

            document.getElementById("sim-summary").textContent =
                data.diagnosis.summary;

            const findings = document.getElementById("sim-findings");
            findings.replaceChildren();

            data.diagnosis.findings.forEach(finding => {
                const card = document.createElement("article");
                card.className = "simulation-finding";

                const heading = document.createElement("h4");
                heading.textContent = finding.finding;

                const severity = document.createElement("p");
                severity.textContent = `Severity: ${finding.severity}`;

                const evidence = document.createElement("p");
                evidence.textContent = `Evidence: ${finding.evidence}`;

                const causes = document.createElement("p");
                causes.textContent =
                    `Possible causes: ${finding.possible_causes.join(", ")}`;

                const recommendations = document.createElement("p");
                recommendations.textContent =
                    `Recommendations: ${finding.recommendation.join(" ")}`;

                card.append(heading, severity, evidence, causes, recommendations);
                findings.appendChild(card);
            });

            results.hidden = false;
            status.textContent = "Simulation completed successfully.";

        } catch (error) {
            status.textContent = `Error: ${error.message}`;
        } finally {
            runButton.disabled = false;
        }
    });
});
