import streamlit as st
import os

from datetime import datetime
from summarizer import summarize_transcript

st.set_page_config(
    page_title="Interview Transcript Summarizer",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>

.main-title {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    color: #1f77b4;
    margin-bottom: 0.5rem;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 2rem;
}

.metric-card {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []


st.markdown(
    '<div class="main-title">🧠 Interview Transcript Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered interview evaluation using Google Gemini</div>',
    unsafe_allow_html=True
)


with st.sidebar:

    st.header("ℹ️ How It Works")

    st.markdown("""
1. Upload a transcript file or paste text
2. Preview transcript content
3. Generate AI-powered assessment
4. Download results

---

### 📊 Output Includes
- Topics Covered
- Candidate Profile
- Evidence & Strengths
- Potential Concerns
- Candidate Summary

---

### 🤖 Model
- Google Gemini
- gemini-2.5-flash
""")

    st.divider()

    st.subheader("⚙️ Settings")

    save_to_outputs = st.checkbox(
        "Auto-save summaries",
        value=True
    )

    show_stats = st.checkbox(
        "Show transcript statistics",
        value=True
    )

col1, col2 = st.columns([3, 2])


with col1:

    st.subheader("📤 Upload Transcript")

    uploaded_file = st.file_uploader(
        "Choose transcript file",
        type=["txt"],
        help="Upload interview transcript file"
    )

    st.markdown("### Or paste transcript manually")

    manual_input = st.text_area(
        "Transcript",
        height=220,
        placeholder="Paste interview transcript here...",
        label_visibility="collapsed"
    )

transcript_text = ""
filename = ""

if uploaded_file:

    transcript_text = uploaded_file.read().decode(
        "utf-8",
        errors="ignore"
    ).strip()

    filename = uploaded_file.name

elif manual_input.strip():

    transcript_text = manual_input.strip()

    filename = (
        f"manual_input_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

with col2:

    st.subheader("📋 Quick Stats")

    if transcript_text:

        word_count = len(transcript_text.split())

        char_count = len(transcript_text)

        line_count = len(
            transcript_text.split("\n")
        )

        estimated_time = max(
            10,
            min(45, word_count // 45)
        )

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:

            st.metric(
                "Words",
                f"{word_count:,}"
            )

            st.metric(
                "Lines",
                f"{line_count:,}"
            )

        with metric_col2:

            st.metric(
                "Characters",
                f"{char_count:,}"
            )

            st.metric(
                "Est. Analysis",
                f"~{estimated_time}s"
            )

    else:

        st.info(
            "Upload or paste a transcript to view statistics."
        )


if transcript_text:

    st.divider()

    with st.expander(
        "📄 Transcript Viewer",
        expanded=False
    ):

        tab1, tab2 = st.tabs([
            "Preview",
            "Full Transcript"
        ])

        with tab1:

            MAX_PREVIEW_LENGTH = 8000

            preview = transcript_text[
                :MAX_PREVIEW_LENGTH
            ]

            if len(transcript_text) > MAX_PREVIEW_LENGTH:

                preview += (
                    "\n\n... (preview truncated)"
                )

            st.text_area(
                "Preview",
                preview,
                height=350,
                disabled=True,
                label_visibility="collapsed"
            )

        with tab2:

            st.text_area(
                "Full Transcript",
                transcript_text,
                height=600,
                disabled=True,
                label_visibility="collapsed"
            )

    st.divider()

    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])

    with btn_col2:

        analyze_button = st.button(
            "🚀 Generate Summary",
            type="primary",
            use_container_width=True
        )

    if analyze_button:

        with st.spinner(
            "🔄 Analyzing transcript with Gemini AI..."
        ):

            try:

                result = summarize_transcript(
                    transcript_text
                )

                st.session_state.analysis_history.append({
                    "filename": filename,
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "summary": result
                })

                if save_to_outputs:

                    output_dir = "outputs"

                    os.makedirs(
                        output_dir,
                        exist_ok=True
                    )

                    output_filename = (
                        f"{os.path.splitext(filename)[0]}"
                        f"_summary_"
                        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    )

                    output_path = os.path.join(
                        output_dir,
                        output_filename
                    )

                    with open(
                        output_path,
                        "w",
                        encoding="utf-8"
                    ) as f:

                        f.write(result)

                st.success(
                    "✅ Analysis completed successfully!"
                )

                st.divider()

                st.subheader(
                    "📊 Structured Summary"
                )

                st.markdown(result)

                if show_stats:

                    st.divider()

                    stat_col1, stat_col2, stat_col3 = st.columns(3)

                    with stat_col1:

                        st.metric(
                            "Input Words",
                            f"{len(transcript_text.split()):,}"
                        )

                    with stat_col2:

                        st.metric(
                            "Output Words",
                            f"{len(result.split()):,}"
                        )

                    with stat_col3:

                        compression_ratio = (
                            (len(result) / len(transcript_text)) * 100
                            if len(transcript_text) > 0
                            else 0
                        )

                        st.metric(
                            "Compression",
                            f"{compression_ratio:.1f}%"
                        )

                if save_to_outputs:

                    st.info(
                        f"💾 Summary saved to: `{output_path}`"
                    )

                st.divider()

                dl_col1, dl_col2 = st.columns(2)

                # Download Summary

                with dl_col1:

                    st.download_button(
                        label="⬇️ Download Summary",
                        data=result,
                        file_name=(
                            f"summary_"
                            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        ),
                        mime="text/plain",
                        use_container_width=True
                    )

                # Download Full Report

                with dl_col2:

                    full_report = f"""
INTERVIEW TRANSCRIPT ANALYSIS REPORT

Generated:
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Source:
{filename}


{transcript_text}

{result}
"""

                    st.download_button(
                        label="📄 Download Full Report",
                        data=full_report,
                        file_name=(
                            f"full_report_"
                            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        ),
                        mime="text/plain",
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    f"❌ Analysis failed: {str(e)}"
                )

                with st.expander(
                    "🔍 Error Details"
                ):

                    st.code(str(e))


else:

    st.info(
        "👆 Upload or paste an interview transcript to begin analysis."
    )


st.divider()

st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;'>

<p>
<strong>Interview Transcript Summarizer</strong>
</p>

<p>
Powered by Google Gemini AI
</p>

<p>
💡 Always review AI-generated evaluations carefully.
</p>

</div>
""", unsafe_allow_html=True)