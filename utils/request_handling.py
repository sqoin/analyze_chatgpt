import json
import requests
from utils.config import read_config


def escape_content(content):
    """Escapes the given content using json.dumps and returns it."""
    escaped_content = json.dumps(content)
    return escaped_content


def make_request(content):
    """Makes a POST request with the given content and returns the response."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": read_config()["authorization"],
    }
    data = {
        "model": read_config()["openai-model"],
        "messages": [{"role": "user", "content": content}]
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=data
    )
    return response


def extract_content(response):
    """Extracts the content from the response and replaces escaped newlines with actual line breaks."""
    content = response.json()["choices"][0]["message"]["content"]
    content = content.replace("\\n", "\n")
    return content
