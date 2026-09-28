
import sys
from pathlib import Path

import streamlit as st

# Add the LegalEase project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai.legal_ai import generate_legal_document
from backend.services.document_export import create_docx, create_pdf


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #9CA3AF;
        margin-top: 5px;
        margin-bottom: 30px;
    }

    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }

    .stDownloadButton button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("⚖️ LegalEase")
    st.caption("AI-Powered Legal Document Platform")

    st.divider()

    st.subheader("Navigation")
    st.write("📄 Document Generator")
    st.write("📥 Document Downloads")

    st.divider()

    st.caption("Version 1.0.0")
    st.caption("Powered by Gemini AI")


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Generate professional legal document drafts with AI'
    '</div>',
    unsafe_allow_html=True,
)

st.info(
    "LegalEase creates editable legal document drafts. "
    "Review the generated document carefully and consult "
    "a qualified lawyer before official use."
)


# --------------------------------------------------
# DOCUMENT GENERATION FORM
# --------------------------------------------------

st.header("📄 Create a Legal Document")

document_types = [
    "Non-Disclosure Agreement (NDA)",
    "Rental Agreement",
    "Employment Agreement",
    "Service Agreement",
    "Affidavit",
    "Business Partnership Agreement",
    "Sale Agreement",
    "Loan Agreement",
    "Other",
]

with st.form("legal_document_form"):

    document_type = st.selectbox(
        "Select Document Type",
        document_types,
    )

    if document_type == "Other":
        custom_document_type = st.text_input(
            "Enter Your Document Type",
            placeholder="Example: Consultancy Agreement",
        )
    else:
        custom_document_type = document_type

    details = st.text_area(
        "Enter Document Details",
        placeholder=(
            "Enter party names, addresses, effective date, "
            "purpose, terms, conditions, jurisdiction, "
            "and any other relevant information."
        ),
        height=220,
    )

    submitted = st.form_submit_button(
        "✨ Generate Legal Document",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# GENERATE DOCUMENT
# --------------------------------------------------

if submitted:

    if not custom_document_type.strip():
        st.warning("Please enter a document type.")

    elif not details.strip():
        st.warning("Please enter the required document details.")

    else:
        try:
            with st.spinner(
                "Generating your legal document... Please wait."
            ):
                generated_document = generate_legal_document(
                    custom_document_type.strip(),
                    details.strip(),
                )

            if not generated_document or not generated_document.strip():
                st.error(
                    "The AI returned an empty document. Please try again."
                )
            else:
                st.session_state["generated_document"] = (
                    generated_document
                )
                st.session_state["generated_document_type"] = (
                    custom_document_type.strip()
                )

                st.success("Document generated successfully!")

        except Exception as error:
            print(f"Document generation error: {error}")

            error_message = str(error)

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                st.error(
                    "Gemini API quota has been exceeded. "
                    "Please wait until your quota resets or check "
                    "your Google AI Studio quota and billing settings."
                )
            else:
                st.error(
                    "Document generation failed. "
                    "Please check the PowerShell error message."
                )


# --------------------------------------------------
# DOCUMENT PREVIEW AND DOWNLOADS
# --------------------------------------------------

if "generated_document" in st.session_state:

    document = st.session_state["generated_document"]
    saved_document_type = st.session_state.get(
        "generated_document_type",
        "Legal Document",
    )

    st.divider()

    st.header("📑 Generated Document")

    st.caption(f"Document Type: {saved_document_type}")

    st.text_area(
        "Document Preview",
        value=document,
        height=450,
        disabled=True,
        key="document_preview",
    )

    st.download_button(
        label="⬇️ Download TXT",
        data=document,
        file_name="LegalEase_Document.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.subheader("Download Document Formats")

    col1, col2 = st.columns(2)

    try:
        docx_file = create_docx(document)
        pdf_file = create_pdf(document)

        with col1:
            st.download_button(
                label="📘 Download Word (DOCX)",
                data=docx_file.getvalue(),
                file_name="LegalEase_Document.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )

        with col2:
            st.download_button(
                label="📕 Download PDF",
                data=pdf_file.getvalue(),
                file_name="LegalEase_Document.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    except Exception as error:
        print(f"Document export error: {error}")

        st.error(
            "File export failed. Please check the PowerShell "
            "window for the exact error."
        )

    st.caption(
        "Disclaimer: This document is an AI-generated draft "
        "for informational purposes only. It does not constitute "
        "formal legal advice. Consult qualified legal counsel "
        "to verify its accuracy and suitability."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "© 2026 LegalEase | AI-Powered Legal Document Generation"
)