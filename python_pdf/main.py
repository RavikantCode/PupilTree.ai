import sys, json, os, time
from pipeline.ingest import extract_blocks
from pipeline.segment import segment
from pipeline.assemble import assemble_question
from storage.uploader import get_uploader

def run(pdf_path: str, output_dir: str = "output"):
    os.makedirs(output_dir, exist_ok=True)
    img_dir = os.path.join(output_dir, "images")
    uploader = get_uploader()

    t0 = time.time()

    blocks, doc = extract_blocks(pdf_path)
    questions_groups = segment(blocks)

    results = []
    for q_group in questions_groups:
        q = assemble_question(q_group, doc, img_dir, uploader)
        results.append(q.model_dump())

    doc.close()

    out_path = os.path.join(output_dir, "questions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    elapsed = time.time() - t0
    return results

if __name__ == "__main__":
    print(sys.argv)
    run(sys.argv[1])