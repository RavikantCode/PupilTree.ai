import pymupdf
import os
from .ingest import Block
from schema.models import ImageDetails

def bbox_to_normalized(bbox: tuple, page_width: float, page_height: float) -> list:
    x0, y0, x1, y1 = bbox
    return [
        round(x0 / page_width * 1000),
        round(y0 / page_height * 1000),
        round(x1 / page_width * 1000),
        round(y1 / page_height * 1000),
    ]

def crop_image(doc: pymupdf.Document, block: Block,
               mapping_name: str, output_dir: str,
               scale: float = 2.0) -> str:
    page = doc[block.page]
    rect = pymupdf.Rect(block.bbox)
    mat = pymupdf.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat, clip=rect)

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{mapping_name}.png")
    pix.save(filepath)
    return filepath

def place_images(question: dict, doc: pymupdf.Document,
                 output_dir: str, uploader) -> tuple[list, dict]:
    import re
    q_num = question["q_num"]
    blocks = question["blocks"]

    option_ranges = {}
    for b in blocks:
        if b.type != "text":
            continue
        m = re.match(r"^\s*\(([A-D])\)", b.content)
        if m:
            key = m.group(1)
            if key in option_ranges:
                option_ranges[key] = (
                    option_ranges[key][0],
                    max(option_ranges[key][1], b.bbox[3])
                )
            else:
                option_ranges[key] = (b.bbox[1], b.bbox[3])

    stem_images = []
    option_images = {}
    img_counter = 0

    for b in blocks:
        if b.type != "image":
            continue

        mapping_name = f"img_q{q_num}_{img_counter}"
        img_counter += 1

        local_path = crop_image(doc, b, mapping_name, output_dir)
        url = uploader.upload(local_path, mapping_name)

        detail = ImageDetails(
            url=url,
            altText=None,
            imageType="question", 
            mappingImageName=f"{{{{IMAGE:{mapping_name}}}}}",
        )

        img_y_center = (b.bbox[1] + b.bbox[3]) / 2
        placed = False

        for key, (oy0, oy1) in option_ranges.items():
            tolerance = 30
            if oy0 - tolerance <= img_y_center <= oy1 + tolerance:
                detail.imageType = "option"
                option_images[key] = detail
                placed = True
                break

        if not placed:
            detail.imageType = "question"
            stem_images.append(detail)

    return stem_images, option_images