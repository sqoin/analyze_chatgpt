import os
from utils.config import read_config
from utils.file_handling import read_file_content, write_file_content, get_file_list
from utils.request_handling import escape_content, make_request, extract_content

# Load the configuration
config = read_config()

# Set the directory to analyze from the configuration
directory_to_analyze = config["project_dir"]

# Set the output directory for the analyzed files
output_dir = os.path.join(directory_to_analyze, f"{os.path.basename(directory_to_analyze)}_chatgpt_analyze")

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create filter for the files that ends with .chatgpt
def filter(name, root, config):
    if not name.endswith(".chatgpt"):
        file_path = os.path.join(root, name)
        if os.path.isfile(file_path):
            content = read_file_content(file_path)
            content = config["request"] + " {}".format(content)
            escaped_content = escape_content(content)
            return escaped_content, file_path
    return None, None

def process_filtered_file(escaped_content, file_path, output_dir):
    response = make_request(escaped_content)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    extracted_content = extract_content(response)
    write_file_content(file_path, extracted_content, output_dir=output_dir)
    print("Processed file: {}".format(file_path))

# Loop through all files in the directory to analyze
for root, dirs, files in get_file_list(directory_to_analyze):
    for name in files:
        escaped_content, file_path = filter(name, root, config)
        if escaped_content:
            try:
                process_filtered_file(escaped_content, file_path, output_dir)
            except Exception as e:
                print("An error occurred while processing {}:{}".format(file_path, e))
