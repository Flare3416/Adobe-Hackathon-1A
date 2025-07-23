# 📄 PDF Outline Extractor – Adobe Hackathon 1A

A smart, Dockerized Python tool that extracts a clean, structured outline from PDF files — including title, and all headings (H1, H2, H3) with their page numbers. Designed for Round 1A of the Adobe GenAI Hackathon, this app runs fully offline inside a Docker container and returns JSON output for each PDF.

---

## ⚙️ Features

- 📌 Extracts document **title** and headings
- 🧠 Classifies **H1**, **H2**, **H3** using font size + style
- 🧾 Outputs per-document structured **JSON**
- 🐋 Fully **Dockerized** for clean offline runs
- ⚡ **Batch processes** multiple PDFs in one go
- 🔒 No internet, no AI models, no fluff — pure logic

---

## 📦 Dependencies

Inside `requirements.txt`:

```txt
pdfminer.six==20221105
charset-normalizer>=2.0.0
cryptography>=2.5

---

## 📁 Folder Structure

```
Adobe-Hackathon-1A/
├── input/            # Place PDFs here
├── output/           # Extracted JSONs appear here
├── main.py           # Core script
├── requirements.txt  # Dependencies
├── Dockerfile        # For building image
└── README.md
```

---

##🐳 Docker Setup Instructions

1. **📥 Add PDFs to input/ folder**
2. **🔨 Build Docker image**
```bash
docker build -t pdf-outline-extractor .