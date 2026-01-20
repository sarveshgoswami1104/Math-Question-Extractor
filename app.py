import streamlit as st
import fitz  # PyMuPDF
import json

from extractor import extract_math_questions

# OCR imports
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes

# ------------------------------------------------------
# HARD-WIRED SYSTEM PATHS (Windows-safe)
# ------------------------------------------------------

# Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Poppler binary path (from your system)
POPPLER_PATH = r"C:\poppler-25.12.0\Library\bin"


# ------------------------------------------------------
# Streamlit page config
# ------------------------------------------------------
st.set_page_config(
    page_title="Math Question Extractor",
    layout="centered"
)

st.title("📘 Math Question Extractor")
st.write(
    "Extract math word problems using a **local LLM**. "
    "Supports text, PDFs, and scanned documents via OCR."
)


# ------------------------------------------------------
# File uploader & text input
# ------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload a PDF, image, or TXT file",
    type=["pdf", "txt", "png", "jpg", "jpeg"]
)

text_input = st.text_area(
    "Or paste text directly here",
    height=200
)


# ------------------------------------------------------
# PDF text extraction with OCR fallback (IMPROVED)
# ------------------------------------------------------
def extract_text_from_pdf(file):
    """
    Extract text from PDF.
    Uses OCR if PDF is scanned/image-based.
    """
    pdf_bytes = file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    # 1️⃣ Try native text extraction
    for page in doc:
        text += page.get_text().strip()

    # 2️⃣ OCR fallback for scanned PDFs
    if not text.strip():
        st.info("Scanned PDF detected. Running OCR (high quality)...")

        images = convert_from_bytes(
            pdf_bytes,
            dpi=300,  # High DPI for better OCR
            poppler_path=POPPLER_PATH
        )

        custom_config = r"--oem 3 --psm 6"

        for img in images:
            text += pytesseract.image_to_string(
                img,
                config=custom_config
            )

    return text


# ------------------------------------------------------
# Main action
# ------------------------------------------------------
if st.button("Extract Math Questions"):

    raw_text = ""

    if uploaded_file is not None:

        if uploaded_file.type == "application/pdf":
            raw_text = extract_text_from_pdf(uploaded_file)

        elif uploaded_file.type.startswith("image"):
            image = Image.open(uploaded_file)
            raw_text = pytesseract.image_to_string(
                image,
                config=r"--oem 3 --psm 6"
            )

        else:
            raw_text = uploaded_file.read().decode("utf-8", errors="ignore")

    elif text_input.strip():
        raw_text = text_input

    else:
        st.warning("Please upload a file or paste some text.")
        st.stop()

    if not raw_text.strip():
        st.warning("No readable text found in the input.")
        st.stop()

    # --------------------------------------------------
    # OCR / Extracted text preview (DEBUG + TRANSPARENCY)
    # --------------------------------------------------
    st.subheader("🔍 OCR / Extracted Text Preview")
    st.text(raw_text[:3000])

    with st.spinner("Running local AI model..."):
        results = extract_math_questions(raw_text)

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------
    if not results:
        st.info("No math questions found.")
    else:
        st.success(f"Found {len(results)} math question(s).")

        for i, q in enumerate(results, start=1):
            st.subheader(f"Question {i}")
            st.write(q.get("question_text", ""))

            latex = q.get("latex", "")
            if latex:
                # Normalize LaTeX to single line for clean rendering
                latex = " ".join(latex.split())
                st.latex(latex)

            st.caption(
                f"Difficulty: {q.get('difficulty')} | "
                f"Tags: {', '.join(q.get('tags', []))}"
            )

        # Download JSON output
        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(results, indent=2),
            file_name="math_questions.json",
            mime="application/json"
        )
