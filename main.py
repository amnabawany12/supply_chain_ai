
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from crew import run_supply_chain_analysis


# PROJECT PATHS

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
REPORTS_DIR = BASE_DIR / "reports"

# Create folders automatically
FRONTEND_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


# FASTAPI APPLICATION

app = FastAPI(
    title="SupplyChain AI",
    description="Multi-Agent Supply Chain Crisis Management System",
    version="2.0.0"
)


# REQUEST MODEL

class CrisisRequest(BaseModel):

    product: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0, le=1000000)
    supplier: str = Field(min_length=1, max_length=100)
    delay_days: int = Field(ge=0, le=365)
    deadline_days: int = Field(gt=0, le=365)
    problem: str = Field(min_length=5, max_length=2000)


# PDF REPORT GENERATION

def create_pdf_report(report_text):

    filename = (
        f"recovery_report_"
        f"{datetime.now():%Y%m%d_%H%M%S_%f}.pdf"
    )

    filepath = REPORTS_DIR / filename

    document = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    content = [
        Paragraph("SupplyChain AI", styles["Title"]),
        Paragraph(
            "Supply Chain Crisis Recovery Report",
            styles["Heading2"]
        ),
        Spacer(1, 15),
        Paragraph(
            f"Generated: {datetime.now():%d %B %Y, %I:%M %p}",
            styles["Normal"]
        ),
        Spacer(1, 20)
    ]

    # Preserve report formatting safely
    for line in str(report_text).splitlines():

        if line.strip():
            content.append(
                Paragraph(escape(line), styles["BodyText"])
            )
        else:
            content.append(Spacer(1, 7))

    document.build(content)

    return filename


# FRONTEND

@app.get("/")
def home():

    index_file = FRONTEND_DIR / "index.html"

    if not index_file.is_file():
        raise HTTPException(
            status_code=404,
            detail="Frontend index.html not found."
        )

    return FileResponse(index_file)


app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)


# CRISIS ANALYSIS API

@app.post("/api/analyze")
def analyze_crisis(request: CrisisRequest):

    try:

        result = run_supply_chain_analysis(
            product=request.product,
            quantity=request.quantity,
            supplier=request.supplier,
            delay_days=request.delay_days,
            deadline_days=request.deadline_days,
            problem=request.problem
        )

        report_filename = create_pdf_report(result)

        return {
            "status": "success",
            "message": "Crisis analysis completed successfully.",
            "report": result,
            "pdf_url": f"/reports/{report_filename}"
        }

    except Exception as error:

        print("CRISIS ANALYSIS ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail=f"Crisis analysis failed: {str(error)}"
        )


# PDF DOWNLOAD

@app.get("/reports/{filename}")
def download_report(filename: str):

    if Path(filename).name != filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    filepath = REPORTS_DIR / filename

    if not filepath.is_file() or filepath.suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=404,
            detail="PDF report not found."
        )

    return FileResponse(
        path=str(filepath),
        media_type="application/pdf",
        filename=filename
    )


# HEALTH CHECK

@app.get("/api/health")
def health_check():

    return {
        "status": "online",
        "application": "SupplyChain AI",
        "agents": 6,
        "framework": "CrewAI"
    }


# API INFORMATION

@app.get("/api")
def api_information():

    return {
        "project": "SupplyChain AI",
        "description": "Multi-Agent Crisis Management System",
        "features": [
            "Crisis Detection",
            "Supplier Research",
            "Inventory Analysis",
            "Logistics Optimization",
            "Risk Assessment",
            "Recovery Planning",
            "PDF Report Generation"
        ]
    }
