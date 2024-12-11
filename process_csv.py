import os
import json
import logging
from dotenv import load_dotenv
from unstructured.partition.csv import partition_csv
from utils import ensure_directory_exists, setup_logging
from charset_normalizer import from_path


def process_csv_files(input_dir, output_dir):
    """
    Recursively processes all CSV files in the input directory
    and saves structured output in the output directory.
    """
    if not os.path.exists(input_dir):
        logging.error(f"Input directory does not exist: {input_dir}")
        return

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".csv"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_dir_full = os.path.join(output_dir, relative_path)
                ensure_directory_exists(output_dir_full)
                output_txt_path = os.path.join(output_dir_full, f"{file}.txt")
                output_json_path = os.path.join(output_dir_full, f"{file}.json")
                output_annotated_txt_path = os.path.join(
                    output_dir_full, f"{file}_annotated.txt"
                )

                logging.info(f"Processing CSV file: {input_path}")
                try:
                    # Detect file encoding
                    encoding = detect_file_encoding(input_path)
                    if not encoding:
                        logging.warning(
                            f"Could not detect encoding for {input_path}. Skipping file."
                        )
                        log_failed_file(input_path, "Unknown encoding")
                        continue

                    # Process the CSV file
                    elements = partition_csv(
                        filename=input_path,
                        encoding=encoding,
                        include_header=True,  # Set to True if you want to include headers
                        infer_table_structure=True,
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
    failed_log_path = os.path.join(os.getenv("LOG_DIR"), "failed_csv_files.log")
    with open(failed_log_path, "a", encoding="utf-8") as f:
        f.write(f"{input_path}: {error_message}\n")
    logging.warning(f"Logged failed CSV file for manual review: {input_path}")


def detect_file_encoding(file_path, min_confidence=0.5):
    """
    Detects the encoding of a CSV file using charset-normalizer.
    Returns the encoding if confidence is above min_confidence, else None.
    """
    try:
        result = from_path(file_path)
        if result:
            best_guess = result.best()
            if best_guess and best_guess.encoding and best_guess.encoding != "ascii":
                if best_guess.percent_chaos < (100 - min_confidence * 100):
                    logging.info(
                        f"Detected encoding '{best_guess.encoding}' for file {file_path}"
                    )
                    return best_guess.encoding
    except Exception as e:
        logging.error(f"Error detecting encoding for {file_path}: {e}")
    return None


if __name__ == "__main__":
    # Load environment variables and set up logging
    load_dotenv()
    input_dir = os.getenv("LOCAL_FILE_INPUT_DIR")
    output_dir = os.getenv("LOCAL_FILE_OUTPUT_DIR")
    log_dir = os.getenv("LOG_DIR")

    ensure_directory_exists(input_dir)
    ensure_directory_exists(output_dir)
    ensure_directory_exists(log_dir)

    setup_logging()

    # Process CSV files
    process_csv_files(input_dir, output_dir)