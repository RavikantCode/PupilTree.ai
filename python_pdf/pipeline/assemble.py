from schema.models import Question, Option, Answer, Table, TableCell
from .parser import parse_question
from .images import place_images
# from .extract import extract_question
import pymupdf

def assemble_question(q_group: dict, doc: pymupdf.Document,output_dir: str, uploader) -> Question:
    q_num = q_group["q_num"]
    blocks = q_group["blocks"]

    raw_text = "\n".join(b.content for b in blocks if b.type == "text")

    extracted = parse_question(raw_text)

    stem_imgs, option_imgs = place_images(
        q_group,
        doc,
        output_dir,
        uploader
    )

    options = []
    for opt_data in extracted.get("options", []):
        key = opt_data.get("key", "")
        img = option_imgs.get(key)
        opt_type = opt_data.get("optionType", "text")
        if img and opt_data.get("text"):
            opt_type = "text_and_image"
        elif img:
            opt_type = "image"

        options.append(Option(
            key=key,
            optionType=opt_type,
            text=opt_data.get("text"),
            imageDetails=img
        ))

    table_blocks = [b for b in blocks if b.type == "table"]
    tables = []
    for tb in table_blocks:
        if not tb.table_data:
            continue
        raw = tb.table_data
        headers = [str(c) if c else "" for c in raw[0]] if raw else []
        rows = []
        for r_idx, row in enumerate(raw[1:], 1):
            cells = []
            for c_idx, cell in enumerate(row):
                cells.append(TableCell(
                    row=r_idx, col=c_idx,
                    text=str(cell) if cell else None
                ))
            rows.append(cells)
        tables.append(Table(headers=headers, rows=rows))

    ans = extracted.get("answer", {})
    return Question(
        questionText=extracted.get("questionText", raw_text),
        questionType=extracted.get("questionType", "MCQ_SINGLE"),
        options=options,
        answer=Answer(
            key=ans.get("key"),
            explanation=ans.get("explanation")
        ),
        hasImage=len(stem_imgs) > 0,
        imageDetails=stem_imgs,
        tables=tables,
    )