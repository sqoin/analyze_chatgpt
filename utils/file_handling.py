import os
import fnmatch
import logging  # Import the logging module
from utils.config import read_config

def read_file_content(file_path):
    """Reads the content of a file and returns it."""
    with open(file_path, "r") as f:
        content = f.read()
        logging.debug(f"Read content from file: {file_path}")  # Log the read operation
        return content


def write_file_content(file_path, content, output_dir=None):
    """Writes the given content to a .chatgpt file with the same name as the original file."""
    if not output_dir:
        output_dir = os.path.dirname(file_path)
    dir_path, filename = os.path.split(file_path)
    filename, extension = os.path.splitext(filename)
    chatgpt_file_path = os.path.join(output_dir, "{}.chatgpt".format(filename))

    with open(chatgpt_file_path, "w") as out:
        out.write(content)
        logging.debug(f"Wrote content to file: {chatgpt_file_path}")  # Log the write operation

 
def get_file_list(dir_path):
    """Yields (root, dirs, files) tuples for all files in the directory that are not ignored by .gitignore. 
    Get all the files with specific extensions defined in the 'files_to_be_included' config."""
    gitignore_path = os.path.join(dir_path, ".gitignore")

    config = read_config()
    requests = config["requests"]

    for request in requests:
        files_to_be_included = request.get("files_to_be_included", "*")
        if files_to_be_included != "*":
            patterns = files_to_be_included.split(",")
            extensions = [os.path.splitext(pattern.strip())[1] for pattern in patterns]
            logging.warning(f"Only {', '.join(extensions)} files will be analyzed")
        
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                ignore_patterns = f.read().splitlines()
            for root, dirs, files in os.walk(dir_path):
                if files_to_be_included != "*":
                    files = [f for f in files if all(not fnmatch.fnmatch(f, pattern) for pattern in ignore_patterns) and any(f.endswith(ext) for ext in extensions)]
                else:
                    files = [f for f in files if all(not fnmatch.fnmatch(f, pattern) for pattern in ignore_patterns)] 
                dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]
                logging.debug(f"Processing directory: {root}")  # Log the directory being processed
                yield root, dirs, files
        else:
            if files_to_be_included != "*":
                files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))  and any(f.endswith(ext) for ext in extensions)]
            else:
                files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) ]  
            logging.debug(f"Processing directory: {dir_path}")  # Log the directory being processed
            yield dir_path, [], files
