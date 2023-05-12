import os
import glob
import json
from utils.config import read_config
import logging
import re
from docx import Document
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml



# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the configuration
config = read_config()

project_dir = config['project_dir']
authorization = config['authorization']
openai_model = config['openai-model']
requests = config['requests']


def add_border(cell):
    # this is the xml for a basic thin border
    border_xml = """
    <w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
    </w:tcBorders>
    """
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_pr.append(parse_xml(border_xml))


def extract_json(file_content):
    # Search for JSON data within file content
    json_pattern = re.compile(r'{.*?}', re.DOTALL)
    json_matches = json_pattern.findall(file_content)
    if not json_matches:
        # JSON data not found or is invalid, return None
        return None
    else:
        # Parse JSON data and return as list of objects
        json_data = []
        for match in json_matches:
            try:
                json_data.append(json.loads(match))
            except json.JSONDecodeError:
                logging.warning(f"Unable to parse JSON data from string: {match}")
        return json_data



def collecting_data_word(project_dir, req, data, file_names):
    # Write output to Word file
    output_dir = os.path.join(project_dir, req['dist_dir'])
    output_extension = '.docx'
    output_file = os.path.join(output_dir, req['collecting_data_output'] + output_extension)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Create a new Document
    doc = Document()

    # Create an empty table
    table = doc.add_table(rows=1, cols=len(data[0][0]) + 2)

    # Add header row
    header_cells = table.rows[0].cells
    header_cells[0].text = 'FileName'
    add_border(header_cells[0])

    for i, key in enumerate(data[0][0].keys()):
        header_cells[i + 1].text = str(key)
        add_border(header_cells[i + 1])

    # Add data rows
    for file_name, file_data in zip(file_names, data):
        for item in file_data:
            cells = table.add_row().cells
            cells[0].text = file_name  # add filename to the first cell
            add_border(cells[0])  # add border to the first cell

            for i, key in enumerate(item.keys()):
                cells[i + 1].text = str(item[key])
                add_border(cells[i + 1])  # add border to the rest of the cells

    # Save the document
    doc.save(output_file)
    logging.info(f"Wrote output data to file: {output_file}")


# Loop through each request in the config
for req in requests:
    # Get files to be analyzed
    input_dir = os.path.join(project_dir, req['dist_dir'])
    files = glob.glob(os.path.join(input_dir, '**', '*' + req['output_extension']), recursive=True)
    logging.info(f"Found {len(files)} files to analyze in {input_dir}")

    # Loop through each file and analyze data
    data = []
    file_names = []
    for file in files:
        with open(file) as f:
            logging.info(f"Analyzing data in file: {file}")
            file_content = f.read()

            # Extract JSON data from file content
            json_obj = extract_json(file_content)
            if json_obj is None:
                # JSON data not found or is invalid, add error to data list
                logging.warning(f"JSON data not found or is invalid in file: {file}")
            else:
                # Add to data list
                data.append(json_obj)
                # Remove the extension from the filename
                base_name = os.path.basename(file)
                file_name, _ = os.path.splitext(base_name)
                file_names.append(file_name)
                logging.info(f"Successfully analyzed JSON data in file: {file}")

    # Call the function with file names
    collecting_data_word(project_dir, req, data, file_names)
