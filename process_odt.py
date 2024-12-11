import os
import json
import logging
from dotenv import load_dotenv
from unstructured.partition.odt import partition_odt
from utils import ensure_directory_exists, setup_logging


def process_odt_files(input_dir, output_dir):
    """
    Processes all .odt files in the input directory and saves extracted content to the output directory.
    """
    if not os.path.exists(input_dir):
        logging.error(f"Input directory does not exist: {input_dir}")
        return

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".odt"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_dir_full = os.path.join(output_dir, relative_path)
                ensure_directory_exists(output_dir_full)
                output_txt_path = os.path.join(output_dir_full, f"{file}.txt")
                output_json_path = os.path.join(output_dir_full, f"{file}.json")
                output_annotated_txt_path = os.path.join(output_dir_full, f"{file}_annotated.txt")

                logging.info(f"Processing ODT file: {input_path}")
                try:
                    elements = partition_odt(
                        filename=input_path,
                        include_metadata=True,
                    )

                    if not elements:
                        logging.warning(f"No content extracted from {input_path}")
                        continue

                    # Write outputs
                    write_output(output_txt_path, elements)
                    write_json_output(output_json_path, elements)
                    write_annotated_output(output_annotated_txt_path, elements)
                    logging.info(f"Processed successfully: {input_path}")

                except Exception as e:
                    logging.error(f"Error processing {input_path}: {e}")
                    log_failed_file(input_path)


def write_output(output_path, elements):
    """
    Writes the extracted content to the output TXT file.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            # Write elements
            for element in elements:
                f.write(f"{element.text}\n\n")  # Add a newline between elements

        logging.info(f"TXT output written to {output_path}")
    except Exception as e:
        logging.error(f"Failed to write TXT output to {output_path}: {e}")


def write_json_output(output_path, elements):
    """
    Writes the elements to a JSON file.
    """
    try:
        data = {
            "elements": [element.to_dict() for element in elements],
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"JSON output written to {output_path}")
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
        logging.info(f"Annotated TXT output written to {output_path}")
    except Exception as e:
        logging.error(f"Failed to write annotated TXT output to {output_path}: {e}")


def elements_to_annotated_text(elements):
    """
    Converts elements to annotated text format.
    """
    annotated_text = ""
    for element in elements:
        element_type = type(element).__name__
        text = element.text or ""
        annotated_text += f"[{element_type}] {text}\n"
    return annotated_text


def log_failed_file(input_path):
    """
    Logs the path of the failed file for manual review.
    """
    failed_log_path = os.path.join(os.getenv("LOG_DIR"), "failed_odt_files.log")
    with open(failed_log_path, "a", encoding="utf-8") as f:
        f.write(f"{input_path}\n")
    logging.warning(f"Logged failed ODT file for manual review: {input_path}")


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

    # Process ODT files
    process_odt_files(input_dir, output_dir)