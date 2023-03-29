
from utils.file_handling import  write_file_content
from utils.request_handling import  make_request, extract_content


def process_filtered_file(escaped_content, file_path, output_dir):
    response = make_request(escaped_content)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    extracted_content = extract_content(response)
    write_file_content(file_path, extracted_content, output_dir=output_dir)
    print("Processed file: {}".format(file_path))