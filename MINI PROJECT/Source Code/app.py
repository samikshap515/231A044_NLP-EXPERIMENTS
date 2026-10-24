import os
import time
import json

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from extractor import extract_action_items


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Meeting Action Item Extractor",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Main page ---------- */

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Hero ---------- */

    .hero {
        background: linear-gradient(135deg, #172554, #2563eb);
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 750;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #dbeafe;
        margin-bottom: 1rem;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.25);
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #e0f2fe;
    }

    /* ---------- Section headings ---------- */

    .section-number {
        color: #2563eb;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.15rem;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }

    .section-description {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    /* ---------- Input area ---------- */

    .input-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    /* ---------- Metrics ---------- */

    .metric-card {
        background: white;
        border: 1px solid #dbe3ef;
        border-radius: 14px;
        padding: 1.15rem 1.25rem;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
    }

    .metric-label {
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .metric-value {
        color: #0f172a;
        font-size: 1.9rem;
        font-weight: 750;
        margin-top: 0.4rem;
    }

    .metric-description {
        color: #94a3b8;
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }

    /* ---------- Summary ---------- */

    .summary-box {
        background: #f8fafc;
        border-left: 5px solid #2563eb;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        color: #334155;
        line-height: 1.7;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.75rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f0;
    }

    /* ---------- Buttons ---------- */

    div.stButton > button {
        border-radius: 9px;
        font-weight: 650;
        min-height: 2.7rem;
    }

    /* ---------- Dataframe ---------- */

    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">📝 Meeting Action Item Extractor</div>
        <div class="hero-subtitle">
            Automatically identify tasks, assignees, deadlines, and priorities
            from meeting notes using NLP-based information extraction.
        </div>
        <div class="hero-badge">
            NLP Mini Project • Deterministic Information Extraction
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-number">01</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Meeting Information</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Provide the meeting date, upload meeting files, or paste meeting notes.'
    '</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# Meeting date
# ------------------------------------------------------------

st.markdown("📅 **Meeting Date**")

meeting_date = st.date_input(
    "Meeting Date",
    label_visibility="collapsed"
)


# ------------------------------------------------------------
# File upload
# ------------------------------------------------------------

st.markdown("📁 **Upload Meeting Files**")

SUPPORTED_FILE_TYPES = [
    "pdf",
    "txt",
    "md",
    "csv",
    "json",
    "docx",
    "xlsx",
    "xls",
    "pptx"
]

uploaded_files = st.file_uploader(
    "Upload files",
    type=SUPPORTED_FILE_TYPES,
    accept_multiple_files=True,
    label_visibility="collapsed",
    help="PDF, TXT, MD, CSV, JSON, DOCX, XLSX, XLS and PPTX are supported."
)


# ------------------------------------------------------------
# Meeting notes
# ------------------------------------------------------------

st.markdown("💬 **Meeting Notes**")

meeting_text = st.text_area(
    "Meeting Notes",
    height=190,
    label_visibility="collapsed",
    placeholder=(
        "Example:\n\n"
        "Rahul will prepare the project report by Friday.\n"
        "Priya will complete the UI design by Monday.\n"
        "Amit must test the application tomorrow.\n"
        "Neha should update the project documentation next week.\n"
        "The security configuration should be reviewed before the final submission.\n"
        "Someone should investigate the server issue urgently."
    )
)


# ============================================================
# FILE TEXT EXTRACTION
# ============================================================

def extract_file_text(uploaded_file):
    """
    Extract readable text from supported file formats.
    """

    extension = os.path.splitext(uploaded_file.name)[1].lower()

    try:

        # ----------------------------------------------------
        # TXT / MD
        # ----------------------------------------------------

        if extension in [".txt", ".md"]:
            return uploaded_file.getvalue().decode(
                "utf-8",
                errors="ignore"
            )

        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------

        if extension == ".csv":
            df = pd.read_csv(uploaded_file)
            return df.to_string(index=False)

        # ----------------------------------------------------
        # JSON
        # ----------------------------------------------------

        if extension == ".json":
            raw = uploaded_file.getvalue().decode(
                "utf-8",
                errors="ignore"
            )

            data = json.loads(raw)

            return json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            )

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        if extension == ".pdf":

            from pypdf import PdfReader

            reader = PdfReader(uploaded_file)

            pages = []

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    pages.append(text)

            return "\n".join(pages)

        # ----------------------------------------------------
        # DOCX
        # ----------------------------------------------------

        if extension == ".docx":

            from docx import Document

            document = Document(uploaded_file)

            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            return "\n".join(paragraphs)

        # ----------------------------------------------------
        # XLSX / XLS
        # ----------------------------------------------------

        if extension in [".xlsx", ".xls"]:

            from openpyxl import load_workbook

            workbook = load_workbook(
                uploaded_file,
                data_only=True
            )

            output = []

            for sheet in workbook.worksheets:

                for row in sheet.iter_rows(
                    values_only=True
                ):

                    values = [
                        str(value)
                        for value in row
                        if value is not None
                    ]

                    if values:
                        output.append(" ".join(values))

            return "\n".join(output)

        # ----------------------------------------------------
        # PPTX
        # ----------------------------------------------------

        if extension == ".pptx":

            from pptx import Presentation

            presentation = Presentation(uploaded_file)

            output = []

            for slide in presentation.slides:

                for shape in slide.shapes:

                    if hasattr(shape, "text"):

                        text = shape.text.strip()

                        if text:
                            output.append(text)

            return "\n".join(output)

        return ""

    except Exception as error:

        st.warning(
            f"Could not read {uploaded_file.name}: {error}"
        )

        return ""


# ============================================================
# EXTRACTION BUTTON
# ============================================================

st.markdown("")

extract_clicked = st.button(
    "🔍  Extract Action Items",
    type="primary",
    use_container_width=True
)


# ============================================================
# EXTRACTION
# ============================================================

if extract_clicked:

    start_time = time.perf_counter()

    source_texts = []

    # --------------------------------------------------------
    # Pasted text
    # --------------------------------------------------------

    if meeting_text and meeting_text.strip():

        source_texts.append(
            meeting_text.strip()
        )

    # --------------------------------------------------------
    # Uploaded files
    # --------------------------------------------------------

    if uploaded_files:

        for uploaded_file in uploaded_files:

            file_text = extract_file_text(
                uploaded_file
            )

            if file_text and file_text.strip():

                source_texts.append(
                    file_text.strip()
                )

    # --------------------------------------------------------
    # No input
    # --------------------------------------------------------

    if not source_texts:

        st.error(
            "Please paste meeting notes or upload at least one meeting file."
        )

        st.stop()

    # --------------------------------------------------------
    # Combine sources
    # --------------------------------------------------------

    combined_text = "\n".join(source_texts)

    # --------------------------------------------------------
    # Run NLP extractor
    # --------------------------------------------------------

    items = extract_action_items(
        combined_text,
        meeting_date
    )

    processing_time = (
        time.perf_counter() - start_time
    )

    # --------------------------------------------------------
    # Store result
    # --------------------------------------------------------

    st.session_state["extraction_results"] = items
    st.session_state["processing_time"] = processing_time


# ============================================================
# DISPLAY RESULTS
# ============================================================

if "extraction_results" in st.session_state:

    items = st.session_state["extraction_results"]

    processing_time = st.session_state.get(
        "processing_time",
        0
    )

    if items is None or items.empty:

        st.warning(
            "No actionable tasks were detected in the provided meeting information."
        )

        st.stop()


    # ========================================================
    # RESULTS HEADER
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-number">02</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Extraction Results</div>',
        unsafe_allow_html=True
    )

    st.info(
        "⚡ Deterministic NLP extraction completed successfully. "
        "Each detected task has been separated into an individual action item."
    )


    # ========================================================
    # METRICS
    # ========================================================

    total_tasks = len(items)

    high_count = int(
        (items["Priority"] == "High").sum()
    )

    medium_count = int(
        (items["Priority"] == "Medium").sum()
    )

    low_count = int(
        (items["Priority"] == "Low").sum()
    )

    deadline_count = int(
        (
            items["Normalized Deadline"]
            .astype(str)
            .str.lower()
            .ne("no deadline")
        ).sum()
    )

    assigned_count = int(
        (
            items["Assigned To"]
            .astype(str)
            .str.lower()
            .ne("unassigned")
        ).sum()
    )


    metric_columns = st.columns(5)


    metrics = [
        (
            "TOTAL TASKS",
            total_tasks,
            "Action items detected"
        ),
        (
            "HIGH PRIORITY",
            high_count,
            "Requires attention"
        ),
        (
            "WITH DEADLINES",
            deadline_count,
            "Deadlines identified"
        ),
        (
            "ASSIGNED",
            assigned_count,
            "Named assignees"
        ),
        (
            "PROCESSING TIME",
            f"{processing_time:.2f}s",
            "Extraction speed"
        )
    ]


    for column, metric in zip(
        metric_columns,
        metrics
    ):

        label, value, description = metric

        with column:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # ACTION ITEMS
    # ========================================================

    st.markdown("")

    st.markdown(
        '<div class="section-number">03</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Action Items</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Individual tasks identified from the meeting information.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Display dataframe
    # --------------------------------------------------------

    display_df = items[
        [
            "Assigned To",
            "Action Item",
            "Deadline",
            "Normalized Deadline",
            "Priority"
        ]
    ].copy()


    def priority_style(row):

        styles = [
            "" for _ in row
        ]

        priority = row["Priority"]

        priority_index = row.index.get_loc(
            "Priority"
        )

        if priority == "High":

            styles[priority_index] = (
                "background-color: #fee2e2; "
                "color: #b91c1c; "
                "font-weight: 700;"
            )

        elif priority == "Medium":

            styles[priority_index] = (
                "background-color: #ffedd5; "
                "color: #c2410c; "
                "font-weight: 700;"
            )

        elif priority == "Low":

            styles[priority_index] = (
                "background-color: #dcfce7; "
                "color: #15803d; "
                "font-weight: 700;"
            )

        return styles


    styled_df = display_df.style.apply(
        priority_style,
        axis=1
    )


    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Assigned To": st.column_config.TextColumn(
                "👤 Assigned To"
            ),
            "Action Item": st.column_config.TextColumn(
                "✅ Action Item",
                width="large"
            ),
            "Deadline": st.column_config.TextColumn(
                "📅 Deadline"
            ),
            "Normalized Deadline": st.column_config.TextColumn(
                "🗓️ Normalized Deadline"
            ),
            "Priority": st.column_config.TextColumn(
                "⚡ Priority"
            )
        }
    )


    # ========================================================
    # CSV DOWNLOAD
    # ========================================================

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="📥 Download Action Items as CSV",
        data=csv_data,
        file_name="meeting_action_items.csv",
        mime="text/csv"
    )


    # ========================================================
    # PRIORITY OVERVIEW
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-number">04</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Priority Overview</div>',
        unsafe_allow_html=True
    )

    priority_labels = [
        "High",
        "Medium",
        "Low"
    ]

    priority_values = [
        high_count,
        medium_count,
        low_count
    ]

    priority_colors = [
        "#EF4444",
        "#F59E0B",
        "#22C55E"
    ]


    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=priority_labels,
            y=priority_values,
            marker_color=priority_colors,
            text=priority_values,
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Tasks: %{y}<extra></extra>"
            )
        )
    )


    fig.update_layout(
        title="Tasks by Priority",
        xaxis_title="Priority",
        yaxis_title="Number of Tasks",
        height=400,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(
            l=50,
            r=30,
            t=70,
            b=50
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # EXTRACTION SUMMARY
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-number">05</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Extraction Summary</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Build professional paragraph
    # --------------------------------------------------------

    priority_sentence_parts = []

    if high_count > 0:
        priority_sentence_parts.append(
            f"{high_count} high-priority "
            f"{'task' if high_count == 1 else 'tasks'}"
        )

    if medium_count > 0:
        priority_sentence_parts.append(
            f"{medium_count} medium-priority "
            f"{'task' if medium_count == 1 else 'tasks'}"
        )

    if low_count > 0:
        priority_sentence_parts.append(
            f"{low_count} low-priority "
            f"{'task' if low_count == 1 else 'tasks'}"
        )


    if len(priority_sentence_parts) == 1:

        priority_text = priority_sentence_parts[0]

    elif len(priority_sentence_parts) == 2:

        priority_text = (
            priority_sentence_parts[0]
            + " and "
            + priority_sentence_parts[1]
        )

    else:

        priority_text = (
            ", ".join(priority_sentence_parts[:-1])
            + ", and "
            + priority_sentence_parts[-1]
        )


    if assigned_count > 0:

        assignment_text = (
            f"{assigned_count} "
            f"{'task has' if assigned_count == 1 else 'tasks have'} "
            f"a named assignee"
        )

    else:

        assignment_text = (
            "no tasks have a named assignee"
        )


    if deadline_count > 0:

        deadline_text = (
            f"{deadline_count} "
            f"{'task contains' if deadline_count == 1 else 'tasks contain'} "
            f"a recognizable deadline"
        )

    else:

        deadline_text = (
            "no recognizable deadlines were identified"
        )


    summary = (
        f"The NLP system identified {total_tasks} actionable "
        f"{'task' if total_tasks == 1 else 'tasks'} from the provided "
        f"meeting information. The extracted items include "
        f"{priority_text}. In addition, {deadline_text}, while "
        f"{assignment_text}. Each action item has been separated into "
        f"an individual record with its assignee, original deadline, "
        f"normalized deadline, and priority."
    )


    st.markdown(
        f'<div class="summary-box">{summary}</div>',
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Meeting Action Item Extractor • NLP Mini Project<br>
        Deterministic NLP-based task, deadline and priority extraction
    </div>
    """,
    unsafe_allow_html=True
)