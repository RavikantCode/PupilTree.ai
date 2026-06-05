import re
from typing import Dict, Any

OPTION_RE = re.compile(r"(?:^|\s)\(?([1-4])\)\s*(.*?)(?=(?:^|\s)\(?[1-4]\)|$)", re.DOTALL)


def detect_question_type(text: str) -> str:
    low = text.lower()

    if "assertion" in low and "reason" in low:
        return "ASSERTION_REASON"

    if re.search(r"\([ivx]+\)", text) and re.search(r"\([pqrs]\)", text):
        return "MATRIX_MATCH"

    if re.search(r"\([A-D]\)", text):
        if "one or more" in low or "one or more correct" in low:
            return "MCQ_MULTIPLE"
        return "MCQ_SINGLE"

    if "true" in low and "false" in low:
        return "TRUE_FALSE"

    return "MCQ_SINGLE"


def parse_question(raw_text: str) -> Dict[str, Any]:
    options = []

    matches = OPTION_RE.findall(raw_text)
    for key, value in matches:
        options.append({
            "key": key,
            "optionType": "text",
            "text": value.strip(),
        })

    stem = OPTION_RE.split(raw_text)[0].strip()

    return {
        "questionText": stem,
        "questionType": detect_question_type(raw_text),
        "options": options,
        "answer": {"key": None, "explanation": None},
    }