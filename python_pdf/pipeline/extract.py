import os
import json
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client

SYSTEM_PROMPT = """You parse one exam question into JSON. Return ONLY raw JSON — no markdown fences, no explanation.

Output this exact shape:
{
  "questionText": "full stem text, LaTeX preserved inside $...$",
  "questionType": "MCQ_SINGLE",
  "options": [
    {"key": "A", "optionType": "text", "text": "option text"}
  ],
  "answer": {"key": null, "explanation": null}
}

questionType rules (apply in this order):
- Has (A)(B)(C)(D) + "one or more correct" → MCQ_MULTIPLE
- Has (A)(B)(C)(D) → MCQ_SINGLE
- Has "Assertion" AND "Reason" → ASSERTION_REASON
- Has (i)(ii) matched to (p)(q) columns → MATRIX_MATCH
- Answer is an integer → NUMERICAL_INTEGER
- Answer is decimal → NUMERICAL_DECIMAL
- Under a passage → PARAGRAPH_BASED
- True/False → TRUE_FALSE
- Default → MCQ_SINGLE

LaTeX rules:
- Preserve ALL math inside $...$
- Do NOT strip or alter dollar signs"""


def extract_question(raw_text: str) -> dict:
    client = _get_client()

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=raw_text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0,    
        ),
    )

    text = resp.text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()

    return json.loads(text)