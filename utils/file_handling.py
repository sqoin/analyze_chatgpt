import os
import fnmatch


def read_file_content(file_path):
    """Reads the content of a file and returns it."""
    with open(file_path, "r") as f:
        content = f.read()
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


def get_file_list(dir_path):
    """Yields (root, dirs, files) tuples for all files in the directory that are not ignored by .gitignore. get all the files that finish with .js and .ts"""
    gitignore_path = os.path.join(dir_path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            ignore_patterns = f.read().splitlines()
        for root, dirs, files in os.walk(dir_path):
            files = [f for f in files if all(not fnmatch.fnmatch(f, pattern) for pattern in ignore_patterns) and (f.endswith('.js') or f.endswith('.ts'))]
            dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]
            yield root, dirs, files
    else:
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and (f.endswith('.js') or f.endswith('.ts'))]
        yield dir_path, [], files
