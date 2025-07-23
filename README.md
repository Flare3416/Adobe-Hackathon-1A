PDF Outline Extractor - Adobe Hackathon Round 1A

This tool extracts the title and heading structure (H1, H2, H3) from PDF files based on font size and boldness using pdfminer.six. It outputs a JSON file per PDF with the document title and structured outline of headings and their page numbers. The tool is designed to be lightweight, offline-compatible, and fully Dockerized as per the Round 1A constraints.

How it works:
- The largest text on the first page is assumed to be the title.
- Font size and boldness are analyzed to classify headings into H1, H2, or H3.
- Short lines and numbered list items are ignored to avoid junk headings.
- No models, no internet, no hardcoded assumptions. Pure layout analysis.
- Works within 10 seconds for PDFs up to 50 pages.

Dependencies (in requirements.txt):
pdfminer.six==20221105
charset-normalizer>=2.0.0
cryptography>=2.5

Docker Instructions:
1. Place all your PDF files into the input/ folder.
2. Build the Docker image:
   docker build -t pdf-outline-extractor .
3. Run the container:
   On PowerShell:
     docker run -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" pdf-outline-extractor
   On CMD (Windows):
     docker run -v "%cd%\\input:/app/input" -v "%cd%\\output:/app/output" pdf-outline-extractor

Output:
- Each PDF processed creates a corresponding .json file in the output/ folder with the extracted title and outline.
- Example output:
  {
    "title": "Understanding AI",
    "outline": [
      { "level": "H1", "text": "Introduction", "page": 1 },
      { "level": "H2", "text": "Background", "page": 2 }
    ]
  }

Notes:
- Fully offline and Docker-compliant.
- Compatible with linux/amd64 base image (python:3.11-slim).
- Tested successfully on multiple documents.
- Ready for evaluation in Round 1A.

Author: Ujjwal Kumar