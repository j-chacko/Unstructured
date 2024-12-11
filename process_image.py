import os
import logging
import json
from unstructured.partition.image import partition_image
from utils import ensure_directory_exists, setup_logging

def process_image_files(
    input_dir,
    output_dir,
    strategy='hi_res',
    languages=None,
    infer_table_structure=False,
):
    """
    Processes all supported image files in the input directory and saves extracted content to the output directory.
    Allows specifying OCR strategy and languages.
    """
    if not os.path.exists(input_dir):
        logging.error(f"Input directory does not exist: {input_dir}")
        return

    supported_extensions = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".heic")

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(supported_extensions):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_dir_full = os.path.join(output_dir, relative_path)
                ensure_directory_exists(output_dir_full)

                # Process the image file
                process_image_file(
                    input_file=input_path,
                    output_dir=output_dir_full,
                    strategy=strategy,
                    languages=languages,
                    infer_table_structure=infer_table_structure,
                )

def process_image_file(
    input_file,
    output_dir,
    strategy='hi_res',
    languages=None,
    infer_table_structure=False,
):
    """
    Processes a single image file and saves the output in the specified output directory.
    """
    try:
        # Partition the image file
        elements = partition_image(
            filename=input_file,
            strategy=strategy,
            languages=languages,
            infer_table_structure=infer_table_structure,
        )

        if not elements:
            logging.warning(f"No content extracted from {input_file}")
            # Optionally log failed file or handle as desired
            return

        # Generate output file paths
        base_filename = os.path.basename(input_file)
        output_txt_path = os.path.join(output_dir, f"{base_filename}.txt")
        output_json_path = os.path.join(output_dir, f"{base_filename}.json")
        output_annotated_txt_path = os.path.join(output_dir, f"{base_filename}_annotated.txt")

        # Write outputs
        write_output(output_txt_path, elements)
        write_json_output(output_json_path, elements)
        write_annotated_output(output_annotated_txt_path, elements)

        logging.info(f"Processed image file: {input_file}")
    except Exception as e:
        logging.error(f"Error processing image file {input_file}: {e}")
        # Optionally log failed file or handle as desired

def write_output(output_path, elements):
    """
    Writes partitioned elements to the output TXT file.
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
    """
    Converts elements to annotated text format.
    """
    annotated_text = ""
    for element in elements:
        element_type = type(element).__name__
        text = element.text or ""
        annotated_text += f"[{element_type}] {text}\n"
    return annotated_text