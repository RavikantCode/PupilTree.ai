import pymupdf
from pathlib import Path
import json

base_dir = Path(__file__).parent
pdf_path = base_dir / "neet_2026.pdf"

result = {
    "pages": []
}

def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)

    for page in doc: 
        text = page.get_text().encode("utf8") 
        image_list = page.get_images()
        tabs = page.find_tables()
        for image in image_list:
            xref = image[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            with open(f"image_{xref}.{ext}", "wb") as img_file:
                img_file.write(image_bytes)

        if tabs.tables:  # at least one table found?
            table_data = tabs[0].extract()  # print content of first table
            table_json = json.dumps(tabs[0].extract(),ensure_ascii=False)
        out.write(text) 
        out.write(bytes((12,))) 
        out.write(table_json.encode("utf8"))
    out.close() 

extract_text_from_pdf(pdf_path)


# def extract_image_from_pdf(pdf_path):
#     doc = pymupdf.open(pdf_path)

#     for page in doc:
#         image_list = page.get_images()
#         for image in image_list:
#             xref = image[0]
#             base_image = doc.extract_image(xref)
#             image_bytes = base_image["image"]
#             # Save the image bytes to a file
#             with open(f"image_{xref}.png", "wb") as img_file:
#                 img_file.write(image_bytes)

# def extract_tables_from_pdf(pdf_path):
#     doc = pymupdf.open(pdf_path)
#     page = doc[0] 
#     tabs = page.find_tables() 
#     print(f"{len(tabs.tables)} found on {page}")

#     if tabs.tables:  # at least one table found?
#         pprint(tabs[0].extract())  

# extract_image_from_pdf(pdf_path)
# extract_tables_from_pdf(pdf_path)