import fnmatch
import os
import logging
from utils.config import read_config
from utils.file_handling import get_file_list
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

# Loop through all requests in the configuration file
for request in config["requests"]:
    # Log the security criteria and the request being analyzed
    logging.info(f"Security criteria: {request['security criteria']}")
    logging.info(f"Analyzing request: {request['request']}")

    # Loop through all files in the directory to analyze, including subdirectories
    for root, dirs, files in get_file_list(directory_to_analyze):
        if not files:
            logging.warning(f"No files found in directory: {root}")
        else:
            for name in files:
                full_path = os.path.join(root, name)
                # Check if the file is excluded by the config
                if any(fnmatch.fnmatch(name, pattern) for pattern in request["files_to_be_excluded"].split(",")):
                    continue

                # Check if the file is included by config
                if request["files_to_be_included"] == "*" or any(fnmatch.fnmatch(name, pattern) for pattern in request["files_to_be_included"].split(",")):
                    escaped_content, file_path = filter(name, root, request)
                    if escaped_content:
                        try:
                            process_filtered_file(escaped_content, file_path, output_dir)
                        except Exception as e:
                            logging.error(f"An error occurred while processing {file_path}: {e}")  # Log the error

if not os.listdir(output_dir):
    logging.warning(f"No files were analyzed.")
