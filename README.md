# Invoice Intelligence – AI‑Powered Invoice Parsing

> A premium, dark‑theme Streamlit UI that extracts structured data from PDF invoices using **pdfplumber**, **PyMuPDF**, and a clean Pydantic data model.

---

## 📖 Overview

This repository implements a complete end‑to‑end invoice‑processing pipeline:

1. **Source** – Load a PDF from a local demo file, a Streamlit upload, or (future) SharePoint.
2. **Storage** – Keep the PDF in‑memory for demos or upload it to Amazon S3 for production.
3. **Parsing** – Extract page text, PDF metadata, and tables.
4. **Cleaning & Extraction** – Normalise text, pull out invoice fields (number, date, vendor, total, etc.) and line‑item details.
5. **Output** – Persist structured JSON and CSV files for downstream systems.

The UI presents the results in a sleek, glass‑morphism dashboard with animated metric cards, status badges, and tabbed views for overview, raw text, tables, and metadata.

---

## ✨ Features

- **Premium dark UI** – gradient accents, glass cards, subtle micro‑animations.
- **Fully typed pipeline** – Pydantic models enforce data integrity.
- **Table handling** – Duplicate column names are automatically deduplicated.
- **Export options** – Download the full JSON result or just the invoice data.
- **Extensible** – The `step_XX_*.py` modules can be swapped out for custom sources/storage.

---

## 📁 Project Structure

```
Data Parsing/
├─ invoice_pipeline/               # Core pipeline package
│   ├─ __init__.py                # Exposes InvoiceConfig & InvoicePipeline
│   ├─ config.py                  # Reads environment variables (.env)
│   ├─ models.py                  # Pydantic data models
│   ├─ pipeline.py                # Orchestrates the steps
│   ├─ step_01_sources.py         # PDF source (demo / upload / SharePoint)
│   ├─ step_02_storage.py         # Memory or S3 storage
│   ├─ step_03_parsing.py         # PDF parsing, cleaning, extraction
│   └─ step_04_output.py          # JSON/CSV output writer
├─ app.py                         # Streamlit UI (premium redesign)
├─ pyproject.toml                 # Project metadata & dependencies
├─ .env                           # Environment configuration (demo mode, S3 keys, …)
└─ README.md                     # <‑‑ you are reading this!
```

**Note:** The original files were renamed from `1_sources.py`, `2_storage.py`, etc., to the more Pythonic `step_01_sources.py` … to match the imports in `pipeline.py`.

---

## 🛠️ Prerequisites

- **Python** ≥ 3.13 (the project uses the latest language features).
- **Git** (to clone the repo if you start from scratch).
- **Virtual environment** – recommended to isolate dependencies.

---

## 🚀 Installation

```bash
# Clone the repo (if you haven't already)
git clone https://github.com/your-username/invoice-intelligence.git
cd "Data Parsing"

# Create a virtual environment
python -m venv .venv
source .venv/Scripts/activate   # PowerShell: .\.venv\Scripts\Activate.ps1

# Install the package (editable) and its dependencies
pip install -e .
```

The `pyproject.toml` already lists the required libraries:
```
# core dependencies
boto3, ipykernel, msal, pdfplumber, pydantic, pymupdf, python-dotenv, requests, streamlit
```
If you prefer a `requirements.txt` you can generate it with `pip freeze > requirements.txt`.

---

## ⚙️ Configuration

Create a `.env` file at the project root (or copy the example from the repo) and set the variables you need:

```dotenv
DEMO_MODE=true                # Use the bundled demo invoice
SAMPLE_PDF=invoice.pdf        # Path to the demo PDF
# Production settings (optional)
TENANT_ID=...
CLIENT_ID=...
CLIENT_SECRET=...
DRIVE_ID=...
SHAREPOINT_FILE_PATH=...
S3_BUCKET_NAME=...
S3_OBJECT_KEY=...
```

---

## ▶️ Running the App

```bash
# From the project root
streamlit run app.py
```

Open the displayed URL (typically `http://localhost:8501`) in your browser. The sidebar lets you:
- Use the **Demo Invoice** (default).
- **Upload** your own PDF.
- (Future) select **SharePoint + Amazon S3**.

Press **⚡ Process Invoice** and watch the pipeline execute. Results appear as:
- Metric cards (invoice number, total amount, line‑item count, page count).
- Tabs for an overview, raw document text, extracted tables, and full JSON metadata.
- Download buttons for the full result and just the invoice data.

---

## 📊 UI Highlights (Mockup)

![Invoice Intelligence UI Mockup](C:/Users/musta/.gemini/antigravity-ide/brain/c5582337-c45b-4572-bf69-260ed84ce256/invoice_ui_mockup_1792227797282.jpg)

The mockup illustrates the dark glass‑morphism layout, gradient‑accented header, and the four KPI cards.

---

## 🧑‍💻 Development

- **Run tests** (if you add any): `pytest`
- **Add new steps** – create a `step_XX_<name>.py` module and import it in `pipeline.py`.
- **Customize styling** – edit the CSS block at the top of `app.py`.

---

## 📜 License

This project is licensed under the **MIT License** – feel free to fork, modify, and use it in commercial applications.

---

## 🙌 Contributing

Contributions are welcome! Please open an issue or submit a pull request.
