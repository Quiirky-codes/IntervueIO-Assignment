# Interview Transcript Summarizer

An AI-powered interview transcript analysis tool built using Streamlit and Google Gemini.

The application takes raw interview transcripts as input and generates structured hiring summaries including:
- Topics covered
- Candidate profile
- Evidence and strengths
- Potential concerns
- Candidate summary

The goal of this project was to build a lightweight but reliable transcript analysis workflow while focusing on prompt engineering, grounding, and structured evaluation.

---

# Features

- Upload interview transcript files (`.txt`)
- Paste transcript manually
- AI-generated structured hiring assessments
- Transcript preview and statistics
- Download generated summaries
- Retry handling for Gemini API failures
- Grounded prompt design to reduce hallucinations
- Handles both technical and operational interviews

---

# Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| LLM Provider | Google Gemini |
| Model Used | `gemini-2.5-flash` |
| Language | Python |

---

# Project Structure

```text
interview-summarizer/
│
├── app.py
├── summarizer.py
├── prompts.py
├── prompt_iterations.md
├── README.md
├── requirements.txt
├── .env
├── .env.example
├── outputs/
└── assets/
```

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/Quiirky-codes/IntervueIO-Assignment.git
cd interview_summarizer
```

---

## 2. Create Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

You can obtain a Gemini API key from:

https://ai.google.dev/

---

# Run the Application

```bash
streamlit run app.py
```

The application will open in your browser automatically.

Default local URL:

```text
http://localhost:8501
```

---

# Usage

1. Upload a `.txt` interview transcript
   OR
2. Paste the transcript manually
3. Click **Generate Summary**
4. Review AI-generated structured assessment
5. Download summary or full report

---

# Example Output Structure

<img width="1364" height="805" alt="Screenshot 2026-05-09 at 9 28 40 AM" src="https://github.com/user-attachments/assets/389ea8c5-fcf5-400d-9229-43903c4f7797" />


---

# Prompt Engineering Approach

The prompts were iteratively refined to improve:
- hallucination reduction
- output consistency
- handling long transcripts
- recruiter-style evaluation tone
- evidence-based seniority inference
- transcript grounding

The evolution of the prompts and outputs is documented in:

```text
prompt_iterations.md
```

---

# Key Design Decisions

## Why Streamlit?

I chose Streamlit because the assignment did not require a full production frontend, and Streamlit allowed quick iteration while still providing a clean and usable interface.

---

## Why Structured Markdown Instead of JSON?

I initially experimented with JSON outputs for consistency, but Gemini occasionally produced malformed JSON on long transcripts.

I ultimately switched to structured markdown because:
- It was more reliable
- Easier to render
- Simpler for recruiters to read
- Reduced unnecessary parsing complexity

---

## Why Transcript Preprocessing?

Interview transcripts often contain:
- timestamps
- inconsistent spacing
- noisy formatting

Basic preprocessing improved:
- prompt readability
- output consistency
- transcript grounding

---

## Reflection

One thing that genuinely surprised me during this assignment was how sensitive the model was to small changes in the prompt. Even slight wording differences changed the tone, confidence level, and structure of the output quite a bit. In the earlier versions, the model tended to overestimate candidates and produce summaries that sounded too polished or generic. Adding grounding instructions such as “only use explicitly stated information” significantly reduced hallucinations and made the summaries feel more realistic and recruiter-friendly.

I also experimented with chunk-based summarization for longer transcripts because I initially thought larger transcripts would exceed context limitations. While it helped with scalability, I noticed that over-compressing transcripts sometimes removed important context and weakened the final evaluation quality. In the final version, I focused more on preserving transcript structure and improving prompt clarity instead of making the pipeline overly complex.

If I had another day, I would improve support for very long interviews using speaker-aware chunking and better context merging. I would also add confidence scoring for profile inference and improve export options like PDF or DOCX reports.

# Limitations

- The quality of summaries depends heavily on transcript clarity.
- Very long transcripts may still require transcript chunking in future versions.
- Candidate evaluation is inference-based and should not replace human review.
- Some technical depth may be difficult for the model to infer if answers are vague.

---

# Security Note

API keys are stored using environment variables and are excluded from version control using `.gitignore`.

No API keys should ever be committed to the repository.

---

# Author

Amith M Jain
