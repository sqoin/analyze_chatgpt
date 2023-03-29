import os
import logging  # Import the logging module
from utils.file_handling import read_file_content
from utils.request_handling import escape_content

# Create filter for the files that ends with .chatgpt
def filter(name, root, config):
    if not name.endswith(".chatgpt"):
        file_path = os.path.join(root, name)
        if os.path.isfile(file_path):
            content = read_file_content(file_path)
            content = config["request"] + " {}".format(content)
            escaped_content = escape_content(content)
            logging.debug(f"Filtered file: {file_path}")  # Log the filtered file
            return escaped_content, file_path
    logging.debug(f"Skipped file: {os.path.join(root, name)}")  # Log the skipped file
    return None, None
