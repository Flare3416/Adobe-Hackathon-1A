import os
import re
import json
from collections import Counter
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

# Define folders where PDFs go in and where JSON comes out
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Get average font size and font name for a line of text
def get_font_properties(text_line):
    sizes = [char.size for char in text_line if isinstance(char, LTChar)]
    fonts = [char.fontname for char in text_line if isinstance(char, LTChar)]

    if not sizes:
        return 0, ""

    avg_size = sum(sizes) / len(sizes)
    font_name = Counter(fonts).most_common(1)[0][0] if fonts else ""

    return avg_size, font_name

# This function reads through the PDF layout and tries to figure out what the title is,
# and what parts look like headings (H1, H2, H3) based on font size and boldness.
def extract_structure_with_layout_analysis(pdf_path):
    font_counts = Counter()
    all_text_lines = []

    # Try to find the title from the first page, usually it's the biggest text
    title_info = {"text": "", "page": 0, "size": 0}

    # First pass: go through every page, collect text info and fonts
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    text = text_line.get_text().strip()
                    if not text:
                        continue

                    avg_size, font_name = get_font_properties(text_line)
                    all_text_lines.append((page_layout.pageid, avg_size, font_name, text))
                    font_counts[round(avg_size)] += 1

                    # Check if this line might be the title
                    if page_layout.pageid == 1 and avg_size > title_info["size"]:
                        title_info["size"] = avg_size
                        title_info["text"] = text
                        title_info["page"] = page_layout.pageid

    # Fallback title if nothing was found on first page
    title = title_info["text"]
    if not title:
        all_text_lines_sorted = sorted(all_text_lines, key=lambda x: -x[1])
        title = all_text_lines_sorted[0][3] if all_text_lines_sorted else os.path.basename(pdf_path)

    # Most common size is assumed to be normal body text
    body_size = font_counts.most_common(1)[0][0] if font_counts else 12

    # Figure out font sizes that stand out enough to be headings
    headings = []
    unique_sizes = sorted(font_counts.keys(), reverse=True)
    heading_thresholds = [s for s in unique_sizes if s > body_size + 1]

    h1_size = heading_thresholds[0] if len(heading_thresholds) > 0 else body_size + 4
    h2_size = heading_thresholds[1] if len(heading_thresholds) > 1 else body_size + 2

    # Second pass: decide heading levels
    for page_num, size, font, text in all_text_lines:
        # Don't include the title again as a heading
        if text == title_info["text"] and page_num == title_info["page"]:
            continue

        is_bold = 'bold' in font.lower()

        if size >= h1_size or (size > body_size and is_bold):
            level = "H1"
        elif size >= h2_size or (size > body_size and is_bold):
            level = "H2"
        elif size > body_size + 0.5:
            level = "H3"
        else:
            continue  # probably normal paragraph text

        # Skip lines that are too short or just numbered bullets
        if len(text) < 4 or re.match(r'^\d+\.', text):
            continue

        headings.append({"level": level, "text": text, "page": page_num})

    return {
        "title": title.strip(),
        "outline": headings
    }

# Wrapper function to extract structure from a single PDF
def extract_pdf_structure(pdf_path):
    return extract_structure_with_layout_analysis(pdf_path)

# Moves any PDF from the root to /input folder (so people can be lazy)
def move_root_pdfs_to_input():
    for file in os.listdir('.'):
        if file.lower().endswith(".pdf"):
            os.rename(file, os.path.join(INPUT_DIR, file))
            print(f"📥 Moved {file} to {INPUT_DIR}/")

# Loop through all PDFs in the input folder and process them
def process_all_pdfs():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)

    move_root_pdfs_to_input()  # this makes the dev life easier

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"🧩 Processing: {filename}...")
            result = extract_pdf_structure(pdf_path)

            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

            print(f"✅ Done: {output_filename}")

# Entry point
if __name__ == "__main__":
    process_all_pdfs()
