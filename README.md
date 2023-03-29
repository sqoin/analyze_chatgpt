# ChatGPT File Analyzer
This script allows you to analyze a directory of .js and .ts files using OpenAI's GPT-3.5-Turbo model. The output is a .chatgpt file for each input file.

# Getting Started
Clone this repository.
Install the required dependencies on the requirements.txt using

```
pip3 install -r requirements.txt

```
# configuration

Before start runing the script you need to configure your 'config.json'.

```

{
    "project_dir": "Where your project is located",
    "authorization": "Your open ai key",
    "request": "a simple request like (Find all problems here)",
    "openai-model":"Your open ai model"
}

```

# Usage
To run the script, simply run the following command in the terminal. 

```
python3 -B analyze.py

```

The output files will be created in the project directory with a _chatgpt_analyse suffix.

