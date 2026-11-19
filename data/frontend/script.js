
const form = document.getElementById("crisisForm");

const button = document.getElementById("analyzeBtn");

const loading = document.getElementById("loading");

const report = document.getElementById("report");

const pdfLink = document.getElementById("pdfLink");


form.addEventListener("submit", async function(event) {

    event.preventDefault();

    button.disabled = true;
    button.textContent = "Analyzing Crisis...";

    loading.classList.remove("hidden");
    report.classList.add("hidden");
    pdfLink.classList.add("hidden");

    const data = {

        product: document.getElementById("product").value,

        quantity: Number(
            document.getElementById("quantity").value
        ),

        supplier: document.getElementById("supplier").value,

        delay_days: Number(
            document.getElementById("delay").value
        ),

        deadline_days: Number(
            document.getElementById("deadline").value
        ),

        problem: document.getElementById("problem").value

    };


    try {

        const response = await fetch("/api/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });


        const result = await response.json();

        if (!response.ok) {

            throw new Error(
                result.detail || "Analysis failed."
            );

        }


        report.textContent = result.report;

        pdfLink.href = result.pdf_url;

        pdfLink.classList.remove("hidden");


    } catch (error) {

        report.textContent =
            "Error: " + error.message;

    } finally {

        loading.classList.add("hidden");

        report.classList.remove("hidden");

        button.disabled = false;

        button.textContent = "Analyze Crisis with AI Agents";

    }

});
