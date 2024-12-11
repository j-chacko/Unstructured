import os
import json
import logging
from dotenv import load_dotenv
from unstructured.partition.xlsx import partition_xlsx
from utils import ensure_directory_exists, setup_logging

def process_xlsx_files(
    input_dir,
    output_dir,
    find_subtable=True,
    include_header=False,
    infer_table_structure=True,
    starting_page_number=1,
):
    """
    Recursively processes all .xlsx files in the input directory
    and saves structured output in the output directory.
    Allows configuring partition_xlsx options.
    """
    if not os.path.exists(input_dir):
        logging.error(f"Input directory does not exist: {input_dir}")
        return

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".xlsx"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_dir_full = os.path.join(output_dir, relative_path)
                ensure_directory_exists(output_dir_full)
                output_txt_path = os.path.join(output_dir_full, f"{file}.txt")
                output_json_path = os.path.join(output_dir_full, f"{file}.json")
                output_annotated_txt_path = os.path.join(
                    output_dir_full, f"{file}_annotated.txt"
                )

                logging.info(f"Processing XLSX file: {input_path}")

                try:
                    # Process the XLSX file
                    elements = partition_xlsx(
                        filename=input_path,
                        find_subtable=find_subtable,
                        include_header=include_header,
                        infer_table_structure=infer_table_structure,
                        starting_page_number=starting_page_number,
                    )

                    if not elements:
                        logging.warning(f"No content extracted from {input_path}")
                        log_failed_file(input_path, "No content extracted")
                        continue

                    # Write outputs
                    write_output(output_txt_path, elements)
                    write_json_output(output_json_path, elements)
                    write_annotated_output(output_annotated_txt_path, elements)
                    logging.info(f"Processed successfully: {input_path}")

                except Exception as e:
                    logging.error(f"Error processing {input_path}: {e}")
                    log_failed_file(input_path, e)

def write_output(output_path, elements):
    """
    Writes the extracted content to the output TXT file.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            for element in elements:
                f.write(f"{element.text}\n\n")
    except Exception as e:
        logging.error(f"Failed to write TXT output to {output_path}: {e}")

def write_json_output(output_path, elements):
    """
    Writes the elements to a JSON file.
    """
    try:
        data = {"elements": [element.to_dict() for element in elements]}
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to write JSON output to {output_path}: {e}")

def write_annotated_output(output_path, elements):
    """
    Writes annotated text output to the specified file.
    """
    try:
        annotated_text = elements_to_annotated_text(elements)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(annotated_text)
    except Exception as e:
        logging.error(f"Failed to write annotated TXT output to {output_path}: {e}")

def elements_to_annotated_text(elements):
    annotated_text = ""
    for element in elements:
        element_type = type(element).__name__
        text = element.text or ""
        annotated_text += f"[{element_type}] {text}\n"
    return annotated_text

def log_failed_file(input_path, error_message):
    """
    Logs the path of the failed file for manual review.
    """
    failed_log_path = os.path.join(os.getenv("LOG_DIR"), "failed_xlsx_files.log")
    with open(failed_log_path, "a", encoding="utf-8") as f:
        f.write(f"{input_path}: {error_message}\n")
    logging.warning(f"Logged failed XLSX file for manual review: {input_path}")

if __name__ == "__main__":
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

    # Process XLSX files
    process_xlsx_files(
        input_dir,
        output_dir,
        find_subtable=True,
        include_header=False,
        infer_table_structure=True,
        starting_page_number=1,
    ) 