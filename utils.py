import os
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def ensure_directory_exists(directory):
    """
    Ensures the specified directory exists, creating it if necessary.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def setup_logging():
    """
    Sets up logging with both console and file handlers.
    """
    log_dir = os.getenv("LOG_DIR")
    if not log_dir:
        raise ValueError("LOG_DIR is not set in the environment variables.")
    ensure_directory_exists(log_dir)

    # Read LOG_LEVEL from environment variables
    log_level_str = os.getenv("LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, log_level_str.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid LOG_LEVEL: {log_level_str}")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"processing_{timestamp}.log")

    # Check if handlers are already set to prevent duplicate logs
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ],
        )
    else:
        # If handlers already exist, set the logging level
        logging.getLogger().setLevel(numeric_level)