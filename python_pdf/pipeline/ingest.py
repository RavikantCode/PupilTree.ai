import pymupdf                  
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Block:
    page: int                      
    type: str            
    bbox: tuple                    
    content: str = ""               
    xref: Optional[int] = None    
    table_data: Optional[list] = None 
    font_size: float = 12.0
    is_bold: bool = False


def extract_blocks(pdf_path: str):
    doc = pymupdf.open(pdf_path)
    blocks: List[Block] = []

    for page_num, page in enumerate(doc):
        page_dict = page.get_text("dict")         

        for b in page_dict["blocks"]:
            if b["type"] == 0:                   
                spans = [
                    span
                    for line in b["lines"]
                    for span in line["spans"]
                ]
                if not spans:
                    continue

                text = " ".join(s["text"] for s in spans).strip()
                if not text:
                    continue

                avg_size = sum(s["size"] for s in spans) / len(spans)
                is_bold = any("Bold" in s.get("font", "") for s in spans)

                blocks.append(Block(
                    page=page_num,
                    type="text",
                    bbox=tuple(b["bbox"]),
                    content=text,
                    font_size=avg_size,
                    is_bold=is_bold,
                ))

            elif b["type"] == 1:               
                blocks.append(Block(
                    page=page_num,
                    type="image",
                    bbox=tuple(b["bbox"]),
                    xref=b.get("xref"),
                ))

        # tabs = page.find_tables()
        # for tab in tabs.tables:
        #     blocks.append(Block(
        #         page=page_num,
        #         type="table",
        #         bbox=tuple(tab.bbox),
        #         table_data=tab.extract(),
        #     ))
        tabs = page.find_tables()
        page_rect = page.rect 
        page_area = page_rect.width * page_rect.height

        for tab in tabs.tables:
            tab_rect = pymupdf.Rect(tab.bbox)
            tab_area = tab_rect.width * tab_rect.height

            if tab_area > (page_area * 0.40):
                continue 

            blocks.append(Block(
                page=page_num,
                type="table",
                bbox=tuple(tab.bbox),
                table_data=tab.extract(),
            ))

    blocks.sort(key=lambda b: (b.page, b.bbox[0] // 300, b.bbox[1]))
    return blocks, doc