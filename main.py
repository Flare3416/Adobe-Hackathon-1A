import os
import re
import json
from collections import Counter
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

# Set your input and output folder paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Extract average font size and most common font name from a line
def get_font_properties(text_line):
    sizes = [char.size for char in text_line if isinstance(char, LTChar)]
    fonts = [char.fontname for char in text_line if isinstance(char, LTChar)]
    if not sizes:
        return 0, ""
    avg_size = sum(sizes) / len(sizes)
    font_name = Counter(fonts).most_common(1)[0][0] if fonts else ""
    return avg_size, font_name

# Analyze layout to extract headings and title based on font styles/sizes
def extract_structure_with_layout_analysis(pdf_path):
    font_counts = Counter()
    all_text_lines = []
    
    # Store the biggest font on page 1 as a potential title
    title_info = {"text": "", "page": 0, "size": 0}

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    text = text_line.get_text().strip()
                    if text:
                        avg_size, font_name = get_font_properties(text_line)
                        all_text_lines.append((page_layout.pageid, avg_size, font_name, text))
                        font_counts[round(avg_size)] += 1

                        # Store the largest text on first page as the title
                        if page_layout.pageid == 1 and avg_size > title_info["size"]:
                            title_info = {
                                "text": text,
                                "page": page_layout.pageid,
                                "size": avg_size
                            }

    # Fallback title if nothing detected
    title = title_info["text"] or (
        sorted(all_text_lines, key=lambda x: -x[1])[0][3] if all_text_lines else os.path.basename(pdf_path)
    )

    body_size = font_counts.most_common(1)[0][0] if font_counts else 12
    unique_sizes = sorted(font_counts.keys(), reverse=True)
    heading_thresholds = [s for s in unique_sizes if s > body_size + 1]

    h1_size = heading_thresholds[0] if len(heading_thresholds) > 0 else body_size + 4
    h2_size = heading_thresholds[1] if len(heading_thresholds) > 1 else body_size + 2

    headings = []
    for page_num, size, font, text in all_text_lines:
        # Skip the line if it's the title
        if text == title_info["text"] and page_num == title_info["page"]:
            continue

        is_bold = 'bold' in font.lower()

        # Classify headings based on size and boldness
        if size >= h1_size or (size > body_size and is_bold):
            level = "H1"
        elif size >= h2_size or (size > body_size and is_bold):
            level = "H2"
        elif size > body_size + 0.5:
            level = "H3"
        else:
            continue

        # Ignore short/bulleted junk
        if len(text) < 4 or re.match(r'^\d+\.', text):
            continue

        headings.append({"level": level, "text": text, "page": page_num})

    return {"title": title.strip(), "outline": headings}

# Wrapper function (in case of future fallback logic)
def extract_pdf_structure(pdf_path):
    return extract_structure_with_layout_analysis(pdf_path)

# Main batch processor for all PDFs in the input directory
def process_all_pdfs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"🔍 Processing: {filename}...")
            try:
                result = extract_pdf_structure(pdf_path)
                output_filename = os.path.splitext(filename)[0] + ".json"
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                print(f"✅ Saved: {output_filename}")
            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")

if __name__ == "__main__":
    process_all_pdfs()