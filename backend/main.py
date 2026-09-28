
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ai.legal_ai import generate_legal_document
from backend.services.document_export import create_docx, create_pdf


# ============================================================
# LegalEase API
# ============================================================

app = FastAPI(
    title="LegalEase API",
    description="AI-powered legal document generation platform",
    version="1.0.0",
)


# ============================================================
# Request Model
# ============================================================

class DocumentRequest(BaseModel):
    document_type: str = Field(
        min_length=1,
        max_length=150,
        description="Type of legal document",
    )
    details: str = Field(
        min_length=1,
        max_length=15000,
        description="Information required to generate the document",
    )


# ============================================================
# Basic Routes
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Welcome to LegalEase API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


# ============================================================
# Generate Legal Document as Text
# ============================================================

@app.post("/generate-document")
def generate_document(request: DocumentRequest):
    try:
        document = generate_legal_document(
            request.document_type,
            request.details,
        )

        return {
            "status": "success",
            "document_type": request.document_type,
            "document": document,
        }

    except Exception as error:
        print(f"Document generation error: {error}")
        raise HTTPException(
            status_code=502,
            detail="Document generation failed. Please try again later.",
        )


# ============================================================
# Generate and Download DOCX
# ============================================================

@app.post("/generate-document/docx")
def generate_document_docx(request: DocumentRequest):
    try:
        document = generate_legal_document(
            request.document_type,
            request.details,
        )

        file_buffer = create_docx(document)

        return StreamingResponse(
            file_buffer,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            headers={
                "Content-Disposition": (
                    'attachment; filename="LegalEase_Document.docx"'
                )
            },
        )

    except Exception as error:
        print(f"DOCX generation error: {error}")
        raise HTTPException(
            status_code=502,
            detail="DOCX generation failed. Please try again later.",
        )


# ============================================================
# Generate and Download PDF
# ============================================================

@app.post("/generate-document/pdf")
def generate_document_pdf(request: DocumentRequest):
    try:
        document = generate_legal_document(
            request.document_type,
            request.details,
        )

        file_buffer = create_pdf(document)

        return StreamingResponse(
            file_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    'attachment; filename="LegalEase_Document.pdf"'
                )
            },
        )

    except Exception as error:
        print(f"PDF generation error: {error}")
        raise HTTPException(
            status_code=502,
            detail="PDF generation failed. Please try again later.",
        )