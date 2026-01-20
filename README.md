# Math Question Extractor (Local LLM + Streamlit)

This project is a **Math Question Extractor** built using **Streamlit** and a **local Large Language Model (LLM)**.  
It extracts mathematical questions from text, PDFs, images, and scanned documents, and presents them in a structured format.

The system runs **entirely locally** and does not rely on any cloud APIs.

---

## Features

- Extracts math questions from:
  - Plain text
  - Text-based PDFs
  - Scanned PDFs (OCR fallback)
  - Images (PNG/JPG)
- Supports algebra and calculus-style questions
- Uses a **local LLM (GPT4All)** for inference
- Does **not solve** questions (symbolic extraction only)
- Clean Streamlit-based UI
- Works offline after initial setup

---

## Tech Stack

- Python 3.11
- Streamlit
- GPT4All (local LLM)
- PyMuPDF (PDF text extraction)
- Tesseract OCR (for scanned documents)
- pdf2image + Poppler (PDF to image conversion)

---

## Project Structure

math-question-extractor/
├── app.py
├── extractor.py
├── requirements.txt
├── README.md
└── samples/ (optional)


---

## Setup Instructions

### 1. Create and activate virtual environment

```bat
py -3.11 -m venv venv
venv\Scripts\activate

2. Install Python dependencies
python -m pip install -r requirements.txt

3. Run the application
streamlit run app.py


The app will be available at:

http://localhost:8501

Usage

Paste math-related text directly into the text box, or

Upload a PDF or image file

Click Extract Math Questions

View extracted questions with symbolic expressions and metadata

OCR Support

For scanned PDFs and images, the application automatically falls back to OCR using Tesseract.

Note: OCR accuracy depends on scan quality and resolution.

Limitations

Low-quality scans, screenshots of emails, or heavily compressed images may not contain enough visual information for OCR to extract mathematical text.

Complex mathematical notation may not always be perfectly recognized by OCR systems.

These limitations are inherent to OCR-based pipelines.

Notes

This project focuses on question extraction, not solving.

Numerical answers are intentionally not computed.

Symbolic relationships are extracted where applicable.

Author

Sarvesh Pravin Goswami


