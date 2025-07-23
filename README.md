# 📄 PDF Outline Extractor – Adobe Hackathon 1A

PDF Outline Extractor is a clean, Dockerized Python tool that extracts a structured outline from PDF files, including the document title and all detected headings (H1, H2, H3) along with their page numbers. Built for Adobe GenAI Hackathon Round 1A, this solution runs completely offline, requires no external models or internet, and produces valid JSON for every PDF.

---

## ⚙️ Features

- 📌 Extracts the document **title** (from largest text on page 1)
- 🧠 Classifies headings as **H1**, **H2**, **H3** based on font size and boldness
- 📂 Supports **batch processing** of multiple PDFs
- 🧾 Outputs one structured `.json` file per input PDF
- 🐋 Fully **Dockerized**, offline-compatible
- 🚫 No ML models, no APIs, no external dependencies

---

## 📦 Tech Stack

- **Python 3.11**
- **pdfminer.six** for PDF parsing
- **Docker** for containerization

---

## 🧩 Folder Structure
```
Adobe-Hackathon-1A/
├── input/ # Drop PDF files here
├── output/ # JSON outputs saved here
├── main.py # Core extraction script
├── requirements.txt # Dependency list
├── Dockerfile # Docker config
└── README.md # This file
```

---

## 🛠️ Setup Instructions

1. **Place PDFs in the `input/` folder**

2. **Build the Docker image**

```bash
docker build -t pdf-outline-extractor .

# PowerShell
docker run -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" pdf-outline-extractor

# CMD (Windows)
docker run -v "%cd%\input:/app/input" -v "%cd%\output:/app/output" pdf-outline-extractor
```
---

## 🧪 Example Output
```
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "History of AI", "page": 2 },
    { "level": "H3", "text": "Symbolic AI", "page": 3 }
  ]
}
```
---
