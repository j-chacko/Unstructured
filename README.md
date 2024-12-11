# Unstructured File Processor

## Overview

The **Unstructured File Processor** is a Python project designed to process a variety of file types, extract their content, and convert them into structured formats. It handles multiple file formats, including:

- Text files (`.txt`)
- CSV and TSV files (`.csv`, `.tsv`)
- Microsoft Office documents (`.doc`, `.docx`, `.ppt`, `.pptx`, `.xlsx`)
- PDF files (`.pdf`)
- Image files (`.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`, `.heic`)
- HTML files (`.html`)
- Markdown files (`.md`)
- Rich Text Format files (`.rtf`)
- And many others

The extracted content can be saved in plain text, JSON, and annotated text formats, providing flexibility for downstream processing and analysis.

## Table of Contents

- [Prerequisites](#prerequisites)
  - [System Requirements](#system-requirements)
  - [Required Packages](#required-packages)
  - [Homebrew Packages](#homebrew-packages)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create Virtual Environment](#2-create-virtual-environment)
  - [3. Install Python Packages](#3-install-python-packages)
  - [4. Install Homebrew Packages](#4-install-homebrew-packages)
  - [5. Set Up Environment Variables](#5-set-up-environment-variables)
  - [6. Create Required Directories](#6-create-required-directories)
- [Usage](#usage)
  - [Running the Main Script](#running-the-main-script)
  - [Running Individual Processing Scripts](#running-individual-processing-scripts)
- [Project Structure](#project-structure)
- [Detailed Description](#detailed-description)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Prerequisites

### System Requirements

- **Operating System:** macOS, Linux, or Windows
- **Python Version:** Python 3.8 or higher

### Required Packages

All the required Python packages are listed in `requirements.txt`. These can be installed using `pip`.

### Homebrew Packages

Some file types require additional system dependencies, which can be installed using [Homebrew](https://brew.sh/) (for macOS and Linux):

- **Tesseract OCR:** Used for optical character recognition (OCR) on images and PDFs.
- **Poppler:** Provides `pdftotext`, `pdftohtml`, and other utilities for PDF processing.
- **libmagic:** Used by `python-magic` for file type detection.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/j-chacko/Unstructured.git
cd Unstructured
```

### 2. Create Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
```

Activate the virtual environment:

- **macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

- **Windows:**

  ```cmd
  venv\Scripts\activate
  ```

### 3. Install Python Packages

Upgrade `pip` and install the required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Homebrew Packages

#### Install Homebrew (if not already installed)

**macOS/Linux:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install Required Packages

```bash
brew install tesseract poppler libmagic
```

**Note for Windows Users:**

- Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) for Windows.
- Install [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/) and add it to your `PATH`.

### 5. Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
touch .env
```

#### Contents of `.env`:

```dotenv
LOCAL_FILE_INPUT_DIR=/path/to/input
LOCAL_FILE_OUTPUT_DIR=/path/to/output
LOG_DIR=/path/to/logs
LOG_LEVEL=INFO
```

- **LOCAL_FILE_INPUT_DIR:** Absolute path to the input directory containing files to process.
- **LOCAL_FILE_OUTPUT_DIR:** Absolute path to the output directory where processed files will be saved.
- **LOG_DIR:** Absolute path to the directory where logs will be stored.
- **LOG_LEVEL:** Logging level (e.g., INFO, DEBUG, WARNING).

**Example:**

```dotenv
LOCAL_FILE_INPUT_DIR=/Users/username/Documents/unstructured/input
LOCAL_FILE_OUTPUT_DIR=/Users/username/Documents/unstructured/output
LOG_DIR=/Users/username/Documents/unstructured/logs
LOG_LEVEL=INFO
```

### 6. Create Required Directories

Ensure that the Input, Output, and Log directories specified in your `.env` file exist:

```bash
mkdir -p /path/to/input
mkdir -p /path/to/output
mkdir -p /path/to/logs
```

---

## Usage

### Running the Main Script

The `main.py` script processes all supported file types in the input directory.

**Command:**

```bash
python main.py
```

**What It Does:**

- Scans the input directory recursively.
- Identifies supported file types.
- Processes each file using the appropriate processing script.
- Saves outputs in the specified output directory.
- Logs processing details and errors.

### Running Individual Processing Scripts

Each file type has a dedicated processing script in the project directory (e.g., `process_pdf.py`, `process_image.py`).

**Example: Processing PDFs**

```bash
python process_pdf.py
```

**Note:**

- Ensure the environment variables are set, either via the `.env` file or exporting them in your shell.
- Individual scripts can be useful for debugging or processing specific file types.

---

## Project Structure

```
Unstructured/
├── main.py
├── .env
├── .gitignore
├── requirements.txt
├── utils.py
├── process_csv.py
├── process_doc_and_docx.py
├── process_email.py
├── process_epub.py
├── process_html.py
├── process_image.py
├── process_md.py
├── process_msg.py
├── process_odt.py
├── process_org.py
├── process_pdf.py
├── process_ppt_and_pptx.py
├── process_rst.py
├── process_rtf.py
├── process_text.py
├── process_tsv.py
├── process_xlsx.py
├── process_xml.py
├── input/
├── output/
└── logs/
    └── ...
```

- **main.py:** Entry point script to process all supported file types.
- **utils.py:** Contains utility functions for logging and directory management.
- **process_*.py:** Scripts dedicated to processing specific file types.
- **logs/:** Directory where log files are stored.

---

## Detailed Description

### Aim of the Project

The goal of the Unstructured File Processor is to automate the extraction and conversion of unstructured data from various file formats into structured formats suitable for data analysis, machine learning, or archival purposes.

**Features:**

- **Multi-format Support:** Handles a wide range of file types.
- **Recursive Processing:** Processes files in subdirectories.
- **Error Handling:** Logs errors and unsupported files for review.
- **Customizable Logging:** Configurable logging levels and outputs.
- **Modular Scripts:** Individual processing scripts for flexibility.

### How It Works

1. **Initialization:**
   - Loads environment variables.
   - Sets up logging configuration.
   - Ensures the input, output, and log directories exist.

2. **Processing Workflow:**
   - Scans the input directory for files.
   - Filters files by supported extensions.
   - For each file:
     - Calls the appropriate processing function.
     - Extracts content using specialized libraries (e.g., `unstructured`, `pytesseract`).
     - Saves output in multiple formats.

3. **Output Formats:**
   - **Plain Text (.txt):** Extracted text content.
   - **JSON (.json):** Structured data including metadata.
   - **Annotated Text (_annotated.txt):** Text with annotations indicating element types.

4. **Logging and Error Handling:**
   - Logs processing steps and any errors encountered.
   - Creates log files in the logs directory.
   - Logs unsupported or failed files for manual review.

---

## Troubleshooting

- **No Content Extracted:**
  - Check if the file is corrupt or contains unsupported content.
  - Review the logs for warnings.

- **Errors During Processing:**
  - Ensure all dependencies are installed.
  - Verify that environment variables are correctly set.
  - Check that required system packages (e.g., Tesseract, Poppler) are installed.

- **Logging Issues:**
  - Confirm that the `LOG_DIR` exists and is writable.
  - Adjust `LOG_LEVEL` in the `.env` file for more detailed logs.

- **Permission Errors:**
  - Ensure you have read permissions for input files and write permissions for output directories.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m "Description of your feature"
   ```

4. Push to your forked repository:

   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a pull request detailing your changes.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

**Note:** Replace any placeholder paths (e.g., `/path/to/input`) with actual paths relevant to your environment.
