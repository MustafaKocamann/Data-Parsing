"""Professional Streamlit interface for the invoice parsing pipeline."""

import json
import pandas as pd
import streamlit as st

from invoice_pipeline import InvoiceConfig, InvoicePipeline
from invoice_pipeline.step_01_sources import PdfSource
from invoice_pipeline.step_02_storage import MemoryStorage


# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Invoice Intelligence · AI-Powered Parsing",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─── Premium Dark Theme CSS ───────────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary: #0a0e1a;
    --bg-card: rgba(15, 20, 40, 0.65);
    --bg-card-hover: rgba(20, 28, 58, 0.8);
    --border-subtle: rgba(99, 102, 241, 0.15);
    --border-glow: rgba(139, 92, 246, 0.4);
    --accent-violet: #8b5cf6;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --gradient-1: linear-gradient(135deg, #8b5cf6, #3b82f6);
    --gradient-2: linear-gradient(135deg, #06b6d4, #8b5cf6);
    --gradient-3: linear-gradient(135deg, #f43f5e, #f59e0b);
    --glass-bg: rgba(15, 23, 42, 0.6);
    --glass-border: rgba(148, 163, 184, 0.08);
}

/* ── Global ── */
.stApp, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: linear-gradient(180deg, #0a0e1a 0%, #0f172a 50%, #0a0e1a 100%) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1025 0%, #111830 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Sidebar Brand Logo ── */
.sidebar-brand {
    text-align: center;
    padding: 1.2rem 0 0.5rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--glass-border);
}

.sidebar-brand .brand-icon {
    font-size: 2.5rem;
    display: block;
    margin-bottom: 0.4rem;
    filter: drop-shadow(0 0 12px rgba(139, 92, 246, 0.5));
}

.sidebar-brand .brand-title {
    font-size: 1.15rem;
    font-weight: 700;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}

.sidebar-brand .brand-subtitle {
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

/* ── Sidebar Section ── */
.sidebar-section {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 1rem 1rem 0.8rem;
    margin-bottom: 0.8rem;
}

.sidebar-section-title {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-muted);
    margin-bottom: 0.6rem;
}

/* ── Pipeline Status Cards ── */
.pipeline-status {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 0.6rem;
}

.pipeline-step {
    flex: 1;
    min-width: 55px;
    text-align: center;
    padding: 6px 4px;
    border-radius: 8px;
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.02em;
    transition: all 0.3s ease;
}

.pipeline-step.waiting {
    background: rgba(100, 116, 139, 0.15);
    color: var(--text-muted);
    border: 1px solid rgba(100, 116, 139, 0.1);
}

.pipeline-step.active {
    background: rgba(139, 92, 246, 0.2);
    color: #c4b5fd;
    border: 1px solid rgba(139, 92, 246, 0.3);
    animation: pulse-glow 2s ease-in-out infinite;
}

.pipeline-step.done {
    background: rgba(16, 185, 129, 0.15);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.25);
}

.step-icon {
    font-size: 1rem;
    display: block;
    margin-bottom: 2px;
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
    50% { box-shadow: 0 0 12px 2px rgba(139, 92, 246, 0.3); }
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 1.5rem;
}

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(12px);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}

.metric-card.violet::before { background: var(--gradient-1); }
.metric-card.cyan::before { background: linear-gradient(90deg, #06b6d4, #3b82f6); }
.metric-card.emerald::before { background: linear-gradient(90deg, #10b981, #06b6d4); }
.metric-card.amber::before { background: linear-gradient(90deg, #f59e0b, #f43f5e); }

.metric-card:hover {
    border-color: var(--border-glow);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(139, 92, 246, 0.12);
}

.metric-label {
    font-size: 0.72rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 0.35rem;
}

.metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.metric-icon {
    position: absolute;
    top: 1rem;
    right: 1.2rem;
    font-size: 1.6rem;
    opacity: 0.15;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.5rem 0 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--glass-border);
}

.section-header .section-icon {
    font-size: 1.25rem;
}

.section-header .section-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}

/* ── Glass Panels ── */
.glass-panel {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(16px);
    margin-bottom: 1rem;
}

.glass-panel-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Detail Rows ── */
.detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(148, 163, 184, 0.06);
}

.detail-row:last-child {
    border-bottom: none;
}

.detail-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-weight: 400;
}

.detail-value {
    font-size: 0.85rem;
    color: var(--text-primary);
    font-weight: 500;
    text-align: right;
    max-width: 60%;
    word-break: break-word;
}

.detail-value.highlight {
    color: var(--accent-violet);
    font-weight: 600;
}

/* ── Status Badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}

.status-badge.success {
    background: rgba(16, 185, 129, 0.15);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.25);
}

.status-badge.info {
    background: rgba(59, 130, 246, 0.15);
    color: #93c5fd;
    border: 1px solid rgba(59, 130, 246, 0.25);
}

/* ── Hero Header ── */
.hero-header {
    padding: 1.5rem 0 1rem;
    margin-bottom: 0.5rem;
}

.hero-title {
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 0.88rem;
    color: var(--text-secondary);
    font-weight: 400;
    line-height: 1.5;
}

/* ── Streamlit Component Overrides ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--glass-bg) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--glass-border) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(139, 92, 246, 0.2) !important;
    color: #c4b5fd !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* Button overrides */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: var(--gradient-1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.7rem 1.5rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3) !important;
    width: 100% !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    box-shadow: 0 6px 28px rgba(139, 92, 246, 0.5) !important;
    transform: translateY(-1px) !important;
}

/* Secondary buttons */
.stButton > button[kind="secondary"],
.stDownloadButton > button {
    background: var(--glass-bg) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton > button:hover {
    border-color: var(--border-glow) !important;
    box-shadow: 0 4px 16px rgba(139, 92, 246, 0.15) !important;
}

/* Radio buttons */
[data-testid="stSidebar"] .stRadio label {
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 1px dashed var(--border-subtle) !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--border-glow) !important;
}

/* Text area */
.stTextArea textarea {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-size: 0.78rem !important;
    line-height: 1.6 !important;
}

/* Select box */
.stSelectbox [data-baseweb="select"] {
    background: var(--glass-bg) !important;
    border-radius: 10px !important;
}

/* JSON viewer */
[data-testid="stJson"] {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

/* DataFrame */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}

/* Alerts */
.stAlert [data-testid="stAlertContentInfo"],
[data-testid="stNotification"] {
    background: rgba(59, 130, 246, 0.1) !important;
    border: 1px solid rgba(59, 130, 246, 0.2) !important;
    border-radius: 12px !important;
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
}

div[data-testid="stNotificationContentSuccess"] {
    background: rgba(16, 185, 129, 0.1) !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
}

div[data-testid="stNotificationContentError"] {
    background: rgba(244, 63, 94, 0.1) !important;
    border: 1px solid rgba(244, 63, 94, 0.2) !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: var(--accent-violet) !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(139, 92, 246, 0.3);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(139, 92, 246, 0.5);
}

/* ── Responsive ── */
@media (max-width: 768px) {
    .metric-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .hero-title {
        font-size: 1.4rem;
    }
}

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: var(--text-muted);
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    border-top: 1px solid var(--glass-border);
    margin-top: 2rem;
}
</style>
""",
    unsafe_allow_html=True,
)


# ─── Constants ─────────────────────────────────────────────────────────────────
SHAREPOINT_S3_OPTION = "☁️ SharePoint + Amazon S3"
DEMO_OPTION = "📦 Demo Invoice"
UPLOAD_OPTION = "📤 Upload PDF"


# ─── Pipeline Logic ───────────────────────────────────────────────────────────
def run_pipeline(source_mode: str, uploaded_file) -> object:
    """Execute the invoice parsing pipeline based on the selected source."""

    if source_mode == SHAREPOINT_S3_OPTION:
        raise ValueError("SharePoint and Amazon S3 flow is coming soon.")

    config = InvoiceConfig()
    config.demo_mode = True

    if source_mode == UPLOAD_OPTION:
        if uploaded_file is None:
            raise ValueError("Please upload a PDF file first.")

        pdf_bytes = uploaded_file.getvalue()
        if not pdf_bytes.startswith(b"%PDF"):
            raise ValueError("The uploaded file is not a valid PDF.")

        source = PdfSource(
            filename=uploaded_file.name,
            pdf_bytes=pdf_bytes,
            source_name="Streamlit Upload",
        )
        storage = MemoryStorage(uploaded_file.name)
        return InvoicePipeline(config, source, storage).run()

    return InvoicePipeline(config).run()


# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown(
        """
        <div class="sidebar-brand">
            <span class="brand-icon">🔮</span>
            <div class="brand-title">Invoice Intelligence</div>
            <div class="brand-subtitle">AI-Powered Parsing Engine</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Document Source Section
    st.markdown(
        '<div class="sidebar-section">'
        '<div class="sidebar-section-title">📂 Document Source</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    source_mode = st.radio(
        "Select input source",
        [DEMO_OPTION, UPLOAD_OPTION, SHAREPOINT_S3_OPTION],
        label_visibility="collapsed",
    )

    uploaded_file = None
    if source_mode == UPLOAD_OPTION:
        uploaded_file = st.file_uploader(
            "Drop your invoice PDF here",
            type="pdf",
            help="Supports single-page and multi-page PDF invoices.",
        )
    elif source_mode == SHAREPOINT_S3_OPTION:
        st.info(
            "The SharePoint → S3 production flow is ready, "
            "but is not enabled in the UI yet."
        )
    else:
        st.markdown(
            '<span class="status-badge info">📄 Using sample invoice.pdf</span>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    run_clicked = st.button(
        "⚡  Process Invoice",
        type="primary",
        disabled=source_mode == SHAREPOINT_S3_OPTION,
        use_container_width=True,
    )

    # Pipeline steps indicator
    pipeline_done = st.session_state.get("result") is not None

    if pipeline_done:
        step_states = ["done"] * 5
    elif run_clicked:
        step_states = ["active"] * 5
    else:
        step_states = ["waiting"] * 5

    step_labels = ["Fetch", "Store", "Parse", "Extract", "Output"]
    step_icons = ["📥", "💾", "🔍", "📊", "📁"]

    steps_html = '<div class="sidebar-section"><div class="sidebar-section-title">⚙️ Pipeline Status</div><div class="pipeline-status">'
    for icon, label, state in zip(step_icons, step_labels, step_states):
        steps_html += (
            f'<div class="pipeline-step {state}">'
            f'<span class="step-icon">{icon}</span>{label}</div>'
        )
    steps_html += "</div></div>"
    st.markdown(steps_html, unsafe_allow_html=True)

    # Footer in sidebar
    st.markdown(
        """
        <div style="position: fixed; bottom: 12px; left: 16px; right: 16px;
                     text-align: center; font-size: 0.65rem; color: #475569;">
            Built with Streamlit · v1.0
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─── Main Content ─────────────────────────────────────────────────────────────

# Hero Header
st.markdown(
    """
    <div class="hero-header animate-in">
        <div class="hero-title">Invoice Intelligence Workspace</div>
        <div class="hero-subtitle">
            Upload an invoice PDF or use the demo file to extract, validate, and export structured data automatically.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Run pipeline
if run_clicked:
    try:
        with st.spinner("🔮 Processing invoice through the AI pipeline..."):
            st.session_state["result"] = run_pipeline(source_mode, uploaded_file)
        st.success("✅ Invoice processed successfully!")
        st.rerun()
    except Exception as error:
        st.session_state.pop("result", None)
        st.error(f"❌ {error}")


# ─── Results Display ───────────────────────────────────────────────────────────
result = st.session_state.get("result")

if not result:
    # Empty State
    st.markdown(
        """
        <div style="text-align: center; padding: 4rem 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.3;">📄</div>
            <div style="font-size: 1.1rem; color: #64748b; font-weight: 500; margin-bottom: 0.5rem;">
                No invoice processed yet
            </div>
            <div style="font-size: 0.82rem; color: #475569; max-width: 400px; margin: 0 auto; line-height: 1.6;">
                Select a document source from the sidebar and click
                <strong style="color: #8b5cf6;">Process Invoice</strong>
                to begin extracting structured data.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    result_dict = result.model_dump(mode="json")
    invoice = result_dict["invoice"]
    line_items = invoice.get("line_items", [])
    parsed_pages = result_dict.get("parsed_pages", [])
    parsed_tables = result_dict.get("parsed_tables", [])
    saved_output = result_dict.get("saved_output", {})

    # ── Metric Cards ──
    inv_num = invoice.get("invoice_number") or "—"
    total_amt = invoice.get("total_amount")
    total_display = f"₹{total_amt:,.0f}" if total_amt else "—"
    items_count = str(len(line_items))
    pages_count = str(len(parsed_pages))

    st.markdown(
        f"""
        <div class="metric-grid animate-in">
            <div class="metric-card violet">
                <div class="metric-icon">🧾</div>
                <div class="metric-label">Invoice Number</div>
                <div class="metric-value">{inv_num}</div>
            </div>
            <div class="metric-card cyan">
                <div class="metric-icon">💰</div>
                <div class="metric-label">Total Amount</div>
                <div class="metric-value">{total_display}</div>
            </div>
            <div class="metric-card emerald">
                <div class="metric-icon">📋</div>
                <div class="metric-label">Line Items</div>
                <div class="metric-value">{items_count}</div>
            </div>
            <div class="metric-card amber">
                <div class="metric-icon">📄</div>
                <div class="metric-label">Pages</div>
                <div class="metric-value">{pages_count}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Output path badge
    if saved_output.get("folder"):
        st.markdown(
            f'<span class="status-badge success">✅ Saved to: {saved_output["folder"]}</span>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ──
    overview_tab, text_tab, tables_tab, json_tab = st.tabs(
        ["📊 Overview", "📝 Document Text", "📋 Tables", "🔧 Metadata & JSON"]
    )

    # ── Overview Tab ──
    with overview_tab:
        col_left, col_right = st.columns([2, 3])

        with col_left:
            st.markdown(
                '<div class="section-header">'
                '<span class="section-icon">🧾</span>'
                '<span class="section-title">Invoice Details</span>'
                "</div>",
                unsafe_allow_html=True,
            )

            details = {
                "Invoice Number": invoice.get("invoice_number") or "—",
                "Invoice Date": invoice.get("invoice_date") or "—",
                "Vendor Name": invoice.get("vendor_name") or "—",
                "Customer Name": invoice.get("customer_name") or "—",
                "Total Amount": total_display,
                "Currency": invoice.get("currency", "INR"),
            }

            detail_html = '<div class="glass-panel">'
            for label, value in details.items():
                highlight = ' highlight' if label in ("Total Amount", "Invoice Number") else ''
                detail_html += (
                    f'<div class="detail-row">'
                    f'<span class="detail-label">{label}</span>'
                    f'<span class="detail-value{highlight}">{value}</span>'
                    f"</div>"
                )
            detail_html += "</div>"
            st.markdown(detail_html, unsafe_allow_html=True)

        with col_right:
            st.markdown(
                '<div class="section-header">'
                '<span class="section-icon">📋</span>'
                '<span class="section-title">Line Items</span>'
                "</div>",
                unsafe_allow_html=True,
            )

            if line_items:
                df = pd.DataFrame(line_items)
                display_columns = {
                    "item": "Description",
                    "quantity": "Qty",
                    "unit_price": "Unit Price",
                    "amount": "Amount",
                }
                optional_cols = {
                    "sku": "SKU",
                    "uom": "UOM",
                    "discount": "Discount",
                    "tax": "Tax",
                }

                for col_key, col_name in optional_cols.items():
                    if col_key in df.columns and df[col_key].notna().any():
                        display_columns[col_key] = col_name

                available = {
                    k: v for k, v in display_columns.items() if k in df.columns
                }
                df_display = df[list(available.keys())].rename(columns=available)

                st.dataframe(
                    df_display,
                    use_container_width=True,
                    hide_index=True,
                    height=min(400, 38 + len(df_display) * 35),
                )

                # Summary stats
                total_items_sum = df["amount"].sum() if "amount" in df.columns else 0
                total_qty = df["quantity"].sum() if "quantity" in df.columns else 0

                scol1, scol2, scol3 = st.columns(3)
                scol1.metric("Total Items", len(line_items))
                scol2.metric("Total Quantity", f"{total_qty:g}")
                scol3.metric("Items Total", f"₹{total_items_sum:,.0f}")
            else:
                st.info("No line items were extracted from this invoice.")

    # ── Document Text Tab ──
    with text_tab:
        st.markdown(
            '<div class="section-header">'
            '<span class="section-icon">📝</span>'
            '<span class="section-title">Extracted Document Text</span>'
            "</div>",
            unsafe_allow_html=True,
        )

        if parsed_pages:
            page_labels = [f"Page {p['page_number']}" for p in parsed_pages]
            selected_page = st.selectbox(
                "Select page",
                range(len(parsed_pages)),
                format_func=lambda i: page_labels[i],
            )

            page_text = parsed_pages[selected_page]["text"]
            word_count = len(page_text.split())
            line_count = len(page_text.splitlines())

            pcol1, pcol2, pcol3 = st.columns(3)
            pcol1.metric("Characters", f"{len(page_text):,}")
            pcol2.metric("Words", f"{word_count:,}")
            pcol3.metric("Lines", f"{line_count:,}")

            st.text_area(
                "Page content",
                page_text,
                height=450,
                label_visibility="collapsed",
            )
        else:
            st.info("No text was extracted from this document.")

    # ── Tables Tab ──
    with tables_tab:
        st.markdown(
            '<div class="section-header">'
            '<span class="section-icon">📋</span>'
            '<span class="section-title">Extracted Tables</span>'
            "</div>",
            unsafe_allow_html=True,
        )

        if parsed_tables:
            st.markdown(
                f'<span class="status-badge info">Found {len(parsed_tables)} table(s)</span>',
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)

            for idx, table in enumerate(parsed_tables, start=1):
                title = f"📊 Table {idx} — Page {table['page_number']}"
                with st.expander(title, expanded=(idx == 1)):
                    table_data = table["data"]
                    if table_data and len(table_data) > 1:
                        raw_headers = [
                            str(h or f"Col {i + 1}")
                            for i, h in enumerate(table_data[0])
                        ]
                        # Deduplicate column names
                        seen: dict[str, int] = {}
                        headers: list[str] = []
                        for h in raw_headers:
                            if h in seen:
                                seen[h] += 1
                                headers.append(f"{h}_{seen[h]}")
                            else:
                                seen[h] = 0
                                headers.append(h)
                        df_table = pd.DataFrame(table_data[1:], columns=headers)
                        st.dataframe(
                            df_table,
                            use_container_width=True,
                            hide_index=True,
                        )
                    else:
                        st.dataframe(
                            table_data,
                            use_container_width=True,
                        )
        else:
            st.info("No tables were detected in this document.")

    # ── Metadata & JSON Tab ──
    with json_tab:
        jcol1, jcol2 = st.columns(2)

        with jcol1:
            st.markdown(
                '<div class="section-header">'
                '<span class="section-icon">📁</span>'
                '<span class="section-title">Saved Files</span>'
                "</div>",
                unsafe_allow_html=True,
            )
            st.json(saved_output)

        with jcol2:
            st.markdown(
                '<div class="section-header">'
                '<span class="section-icon">🏷️</span>'
                '<span class="section-title">Document Metadata</span>'
                "</div>",
                unsafe_allow_html=True,
            )
            st.json(result_dict.get("metadata", {}))

        st.markdown("<br>", unsafe_allow_html=True)

        # Download buttons
        dcol1, dcol2 = st.columns(2)

        json_data = json.dumps(result_dict, indent=2, ensure_ascii=False)

        with dcol1:
            st.download_button(
                "⬇️  Download Full JSON",
                data=json_data,
                file_name="invoice_result.json",
                mime="application/json",
                use_container_width=True,
            )

        with dcol2:
            invoice_json = json.dumps(invoice, indent=2, ensure_ascii=False)
            st.download_button(
                "⬇️  Download Invoice Data",
                data=invoice_json,
                file_name="invoice_data.json",
                mime="application/json",
                use_container_width=True,
            )

        # Full JSON preview
        with st.expander("🔍 Preview Complete JSON Output"):
            st.json(result_dict)

    # Footer
    st.markdown(
        """
        <div class="footer">
            🔮 Invoice Intelligence · AI-Powered Parsing Engine · Built with Streamlit & Pydantic
        </div>
        """,
        unsafe_allow_html=True,
    )