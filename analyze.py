import os
import logging
from utils.config import read_config
from utils.file_handling import  get_file_list
from utils.filter import filter
from utils.process_filtered_file import process_filtered_file
from logger_config import configure_logger 



# Configure the logger
configure_logger()

# Load the configuration
config = read_config()

# Set the directory to analyze from the configuration
directory_to_analyze = config["project_dir"]

# Set the output directory for the analyzed files
output_dir = os.path.join(directory_to_analyze, f"{os.path.basename(directory_to_analyze)}_chatgpt_analyze")

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# Log the directory being analyzed and the output directory
logging.info(f"Analyzing directory: {directory_to_analyze}")
logging.info(f"Output directory: {output_dir}")

# Loop through all files in the directory to analyze
for root, dirs, files in get_file_list(directory_to_analyze):
    for name in files:
        escaped_content, file_path = filter(name, root, config)
        if escaped_content:
            try:
                process_filtered_file(escaped_content, file_path, output_dir)
            except Exception as e:
                logging.error(f"An error occurred while processing {file_path}: {e}")  # Log the error