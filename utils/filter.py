
import os
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
            return escaped_content, file_path
    return None, None

