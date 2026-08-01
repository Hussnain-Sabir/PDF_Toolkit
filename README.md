# 🛠️ Python PDF Toolkit

A lightweight, terminal-based CLI application built with Python to convert, merge, and compress PDFs and images seamlessly.

Wrote all of the code on my own, but used AI help for image compression in PDFs and for CLI input.

---

## 🌟 Features

* **🖼️ Image-to-PDF Conversion:** Convert all `.jpg`, `.jpeg`, `.png`, and `.webp` files inside a directory into a single combined PDF.
* **📄 PDF Merger:** Combine multiple PDF documents in strict numerical/alphabetical order.
* **🔀 Unified Media Merger:** Merge both images and PDF files together into a single master document without losing text vector crispness.
* **🗜️ PDF Compressor:** Reduces PDF file sizes using iterative image resizing (`LANCZOS`), quality degradation, stream compression, and object deduplication toward a user-defined target megabyte size.
* **🖥️ Interactive CLI:** Menu-driven terminal interface with path sanitization (supports drag-and-drop paths with single/double quotes).

---

## 📁 Folder Structure & File Creation

The toolkit automatically manages output directories based on the action selected:

| Tool / Action | Target Directory Created |
| :--- | :--- |
| **Image to PDF** | `<folder_path>/IMG_to_PDF/` |
| **PDF Merger** | `<folder_path>/Merged_PDFs/` |
| **Unified Media Merger** | `<folder_path>/Merged_All/` |
| **PDF Compressor** | `<file_parent_folder>/Compressed_PDFs/` |

> 🔒 **Collision Safety:** All functions use non-overwriting filename logic (`_1.pdf`, `_2.pdf`) so existing files are never overwritten.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3.8+** installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/pdf-toolkit.git](https://github.com/your-username/pdf-toolkit.git)
   cd pdf-toolkit

Install dependencies:
  pip install pypdf pillow


  🖥️ Usage
Run the main script to launch the interactive menu:
  python pdf_toolkit.py



Options Overview:

==============================
      PDF TOOLKIT CLI         
==============================
1. Convert Images to PDF
2. Merge PDFs
3. Merge Images & PDFs Together
4. Compress a PDF
5. Exit
