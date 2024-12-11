import os
import logging
from dotenv import load_dotenv
# Import all processing functions
from process_csv import process_csv_files
from process_doc_and_docx import process_doc_and_docx_files
from process_email import process_email_files
from process_epub import process_epub_files
from process_image import process_image_files
from process_md import process_md_files
from process_msg import process_msg_files
from process_odt import process_odt_files
from process_org import process_org_files
from process_pdf import process_pdf_files
from process_html import process_html_files
from process_ppt_and_pptx import process_ppt_and_pptx_files
from process_rst import process_rst_files
from process_rtf import process_rtf_files
from process_text import process_text_files
from process_tsv import process_tsv_files
from process_xlsx import process_xlsx_files
from process_xml import process_xml_files
from utils import ensure_directory_exists, setup_logging

def log_unsupported_files(input_dir, supported_extensions):
    """
    Scans the input directory for unsupported file types and logs their paths.
    """
    unsupported_files = []
    for root, dirs, files in os.walk(input_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            # Skip hidden files
            if file.startswith('.'):
                continue
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext not in supported_extensions:
                file_path = os.path.join(root, file)
                unsupported_files.append(file_path)
    
    if unsupported_files:
        log_dir = os.getenv("LOG_DIR")
        ensure_directory_exists(log_dir)
        log_file_path = os.path.join(log_dir, "unsupported_files.log")
        with open(log_file_path, "w", encoding="utf-8") as f:
            for file_path in unsupported_files:
                f.write(f"{file_path}\n")
        logging.warning(f"Logged unsupported files for manual review in {log_file_path}")
    else:
        logging.info("No unsupported files found in the input directory.")

def main():
    # Load environment variables
    load_dotenv()
    input_dir = os.getenv("LOCAL_FILE_INPUT_DIR")
    output_dir = os.getenv("LOCAL_FILE_OUTPUT_DIR")
    log_dir = os.getenv("LOG_DIR")

    # Ensure directories exist
    ensure_directory_exists(input_dir)
    ensure_directory_exists(output_dir)
    ensure_directory_exists(log_dir)

    # Set up logging
    setup_logging()
    logging.info("Logging initialized.")

    # List of supported file extensions
    supported_extensions = {
        ".txt", ".csv", ".tsv", ".xlsx", ".xml", ".doc", ".docx", ".ppt",
        ".pptx", ".rst", ".rtf", ".eml", ".msg", ".epub", ".png", ".jpg",
        ".jpeg", ".tiff", ".bmp", ".heic", ".md", ".odt", ".org", ".html",
        ".pdf"
    }

    # Log unsupported files
    logging.info("Scanning for unsupported files...")
    log_unsupported_files(input_dir, supported_extensions)

    # List of processing functions and their descriptions
    processing_tasks = [
        (process_csv_files, "CSV file processing"),
        (process_tsv_files, "TSV file processing"),
        (process_xlsx_files, "XLSX file processing"),
        (process_xml_files, "XML file processing"),
        (process_doc_and_docx_files, "DOC and DOCX file processing"),
        (process_ppt_and_pptx_files, "PPT and PPTX file processing"),
        (process_rst_files, "RST file processing"),
        (process_rtf_files, "RTF file processing"),
        (process_text_files, "Text file processing"),
        (process_email_files, "Email file processing"),
        (process_epub_files, "EPUB file processing"),
        (process_image_files, "Image file processing"),
        (process_md_files, "Markdown file processing"),
        (process_msg_files, "Outlook (.msg) file processing"),
        (process_odt_files, "ODT file processing"),
        (process_org_files, "Org Mode file processing"),
        (process_html_files, "HTML file processing"),
        (process_pdf_files, "PDF file processing"),
    ]

    # Execute each processing task
    for process_function, description in processing_tasks:
        try:
            logging.info(f"Starting {description}...")
            process_function(input_dir, output_dir)
            logging.info(f"{description} completed successfully.")
        except Exception as e:
            logging.error(f"Error during {description}: {e}")

if __name__ == "__main__":
    main()