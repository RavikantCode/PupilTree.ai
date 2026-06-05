import re
from .ingest import Block
from typing import List, Dict, Any

Q_START = re.compile(r"^\s*(\d{1,3})\.\s+[A-Z]", re.IGNORECASE)


def segment(blocks: List[Block]) -> List[Dict[str, Any]]:
    questions = []
    current = None       

    for block in blocks:
        is_new_q = False
        q_num = None

        if block.type == "text":
            m = Q_START.match(block.content)
            if m:
                num = int(m.group(1))
                expected = (questions[-1]["q_num"] + 1) if questions else 1
                if abs(num - expected) <= 3:
                    is_new_q = True
                    q_num = num

        if is_new_q:
            if current is not None:
                questions.append(current)
            current = {
                "q_num":   q_num,
                "page":    block.page,
                "start_y": block.bbox[1],
                "end_y":   block.bbox[3],
                "blocks":  [block],
            }
        elif current is not None:
            current["blocks"].append(block)
            current["end_y"] = max(current["end_y"], block.bbox[3])

    if current is not None:
        questions.append(current)

    return questions