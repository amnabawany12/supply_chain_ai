const crisisForm = document.getElementById("crisisForm");
const analyzeButton = document.getElementById("analyzeButton");

const loadingSection = document.getElementById("loadingSection");
const loadingText = document.getElementById("loadingText");

const resultsSection = document.getElementById("results");
const reportContent = document.getElementById("reportContent");

const downloadButton = document.getElementById("downloadButton");
const copyButton = document.getElementById("copyButton");
const resetButton = document.getElementById("resetButton");

const systemStatus = document.getElementById("systemStatus");
const toast = document.getElementById("toast");

let currentReport = "";

let toastTimer;

// TOAST MESSAGE
function showToast(message, isError = false) {
    toast.textContent = message;
    toast.className = isError ? "toast show error" : "toast show";

    clearTimeout(toastTimer);

    toastTimer = setTimeout(() => {
        toast.className = "toast";
    }, 3500);
}

// CHECK BACKEND CONNECTION
async function checkSystem() {
    try {
        const response = await fetch("/api/health");

        if (!response.ok) {
            throw new Error("Backend unavailable");
        }

        const data = await response.json();

        systemStatus.textContent = data.status === "online"
            ? "Online"
            : "Offline";

    } catch (error) {
        systemStatus.textContent = "Offline";
        console.error("Health Check Error:", error);
    }
}

// COLLECT FORM DATA
function getFormData() {
    return {
        product: document.getElementById("product").value.trim(),

        quantity: Number(
            document.getElementById("quantity").value
        ),

        supplier: document.getElementById("supplier").value.trim(),

        delay_days: Number(
            document.getElementById("delayDays").value
        ),

        deadline_days: Number(
            document.getElementById("deadlineDays").value
        ),

        problem: document.getElementById("problem").value.trim()
    };
}

// VALIDATE DATA
function validateData(data) {
    if (!data.product || !data.supplier || !data.problem) {
        showToast("Please complete all required fields.", true);
        return false;
    }

    if (!Number.isInteger(data.quantity) ||
        data.quantity < 1 || data.quantity > 1000000) {
        showToast("Enter a valid affected quantity.", true);
        return false;
    }

    if (!Number.isInteger(data.delay_days) ||
        data.delay_days < 0 || data.delay_days > 365) {
        showToast("Enter a valid shipment delay.", true);
        return false;
    }

    if (!Number.isInteger(data.deadline_days) ||
        data.deadline_days < 1 || data.deadline_days > 365) {
        showToast("Enter a valid delivery deadline.", true);
        return false;
    }

    if (data.problem.length < 5 || data.problem.length > 2000) {
        showToast("Problem description must be 5-2000 characters.", true);
        return false;
    }

    return true;
}

// SHOW LOADING
function startLoading() {
    loadingSection.hidden = false;
    resultsSection.hidden = true;

    loadingText.textContent =
        "Connecting to the CrewAI multi-agent system...";

    analyzeButton.disabled = true;
    analyzeButton.innerHTML = "✧ Analyzing...";

    loadingSection.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}

// STOP LOADING
function stopLoading() {
    loadingSection.hidden = true;

    analyzeButton.disabled = false;
    analyzeButton.innerHTML =
        "<span>✧</span> Analyze Crisis <span>→</span>";
}

// DISPLAY REPORT
function displayReport(data) {
    currentReport = String(data.report || "");

    reportContent.textContent = currentReport;

    if (data.pdf_url) {
        downloadButton.href = data.pdf_url;
        downloadButton.style.display = "inline-block";
    } else {
        downloadButton.style.display = "none";
    }

    resultsSection.hidden = false;

    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

// ANALYZE CRISIS
crisisForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const formData = getFormData();

    if (!validateData(formData)) {
        return;
    }

    startLoading();

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Crisis analysis failed."
            );
        }

        if (data.status !== "success") {
            throw new Error(
                data.message || "Analysis was not successful."
            );
        }

        displayReport(data);

        showToast("Crisis analysis completed successfully!");

    } catch (error) {

        console.error("Analysis Error:", error);

        showToast(error.message, true);

    } finally {
        stopLoading();
    }

});

// COPY REPORT
copyButton.addEventListener("click", async function() {

    if (!currentReport) {
        showToast("No report available to copy.", true);
        return;
    }

    try {
        await navigator.clipboard.writeText(currentReport);

        showToast("Report copied successfully!");

    } catch (error) {
        showToast("Unable to copy report.", true);
    }

});

// RESET FORM
resetButton.addEventListener("click", function() {

    setTimeout(() => {
        resultsSection.hidden = true;
        loadingSection.hidden = true;

        currentReport = "";

        reportContent.textContent = "";

        downloadButton.href = "#";

        showToast("Form has been reset.");

    }, 0);

});

// INITIALIZE APPLICATION
document.addEventListener("DOMContentLoaded", function() {
    checkSystem();
});