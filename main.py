import os
import re
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

# Use local folders
INPUT_DIR = "input"
OUTPUT_DIR = "output"

def extract_pdf_structure(pdf_path):
    headings = []
    font_sizes = []
    pages_detected = set()

    for page_layout in extract_pages(pdf_path):
        page_number = page_layout.pageid
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if hasattr(text_line, "get_text"):
                        text = text_line.get_text().strip()
                        if text:
                            sizes = [char.size for char in text_line if isinstance(char, LTChar)]
                            if sizes:
                                avg_size = sum(sizes) / len(sizes)
                                font_sizes.append((avg_size, text, page_number))
                                if re.match(r'^\d+\.|^\([a-zA-Z]\)', text) or text.endswith(':'):
                                    continue
                                if avg_size > 15:
                                    level = "H1"
                                elif 13 < avg_size <= 15:
                                    level = "H2"
                                else:
                                    level = "H3"
                                headings.append({
                                    "level": level,
                                    "text": text,
                                    "page": page_number
                                })
                                pages_detected.add(page_number)

    title = sorted(font_sizes, key=lambda x: -x[0])[0][1].strip() if font_sizes else os.path.basename(pdf_path)
    structured = len(headings) >= 3 and len(pages_detected) > 1

    return {
        "title": title,
        "outline": headings if structured else []
    }

def process_all_pdfs():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            result = extract_pdf_structure(pdf_path)
            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            print(f"✅ Processed: {filename}")

if __name__ == "__main__":
    process_all_pdfs()
