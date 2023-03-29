# ChatGPT File Analyzer
This script analyzes a directory of code files and uses the OpenAI model to generate analysis based on the content of the files. The responses are written to new files with a .chatgpt extension.

# How to use

    1.Clone this repository to your local machine.
    2.Install the necessary dependencies by running pip3 install -r requirements.txt
    3.Modify the config.json file.
    4.Run the script with the command  python3 -B analyze.py
    5.The generated .chatgpt files will be written to a new directory named after the original directory.

# configuration

You need to make changes on your 'config.json'.

```

{
    "project_dir": ".",
    "authorization": "Your open ai key", /* check https://platform.openai.com/account/api-keys */
    "request": "a simple request like (Find all problems here)",
    "openai-model":"gpt-3.5-turbo", /* or GPT-4 */
    "files_to_be_included": "*", /* could be *.js, *.ts */
    "files_to_be_excluded": "*.chatgpt" /* this pattern will be added to .gitignore pattern if it exists */
}

```
# Error handling

    The script has detailed logging to help identify any errors that may occur during the analysis process. Here are some examples of how the script handles errors:

     _ If the script encounters a directory or file that it cannot access, it will log a warning message and skip that file or directory.

     _ If a file does not contain any code that needs to be processed, the script will log a warning message and skip that file.

     _ If the script encounters an error while making a request to the OpenAI API, it will log an error message with a stack trace and skip processing that file.

     _ If the script encounters an error while extracting content from the response, it will log a warning message and skip processing that file.

     _ If the script encounters an error while writing to a file, it will log an error message with a stack trace and skip processing that file.

    By checking the logs, you can identify any issues that occurred during the analysis process and take appropriate action to resolve them.


