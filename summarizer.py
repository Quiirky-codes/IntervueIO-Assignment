import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

from prompts import FINAL_PROMPT

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables."
    )

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def preprocess_transcript(text):
    """
    Cleans transcript while preserving structure.
    """

    if not text:
        return ""

    # Remove timestamps like [12:37]
    text = re.sub(r"\[\d{1,2}:\d{2}\]", "", text)

    # Normalize spaces while preserving paragraphs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def chunk_transcript(text, chunk_size=4000):
    """
    Splits long transcripts into smaller chunks.
    """

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def summarize_transcript(transcript_text):
    """
    Generates structured interview summary using Gemini.
    """

    if not transcript_text or len(transcript_text.strip()) < 20:
        return (
            "⚠️ Transcript is too short or empty for meaningful analysis."
        )

    cleaned_text = preprocess_transcript(
        transcript_text
    )

    # Use full transcript directly
    # unless extremely large
    MAX_DIRECT_LENGTH = 25000

    if len(cleaned_text) > MAX_DIRECT_LENGTH:

        chunks = chunk_transcript(
            cleaned_text,
            chunk_size=8000
        )

        # Keep only first few chunks
        # to avoid losing structure
        cleaned_text = "\n\n".join(chunks[:3])

    prompt = FINAL_PROMPT.replace(
        "{transcript}",
        cleaned_text
    )

    last_error = None

    for attempt in range(3):

        try:

            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,
                    "top_p": 0.8,
                    "max_output_tokens": 2200,
                }
            )

            if not response.text:
                raise ValueError(
                    "Empty response received from Gemini."
                )

            result = response.text.strip()

            result = result.replace(
                "```markdown",
                ""
            )

            result = result.replace(
                "```",
                ""
            )

            return result.strip()

        except Exception as e:
            last_error = str(e)

    return f"❌ Failed after retries: {last_error}"