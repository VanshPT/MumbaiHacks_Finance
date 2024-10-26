# qa.py
import os
from langchain_community.document_loaders import SeleniumURLLoader
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

# Function to summarize URL content
def urlSummarizer(input_urls):
    urls = [input_urls]

    loader = SeleniumURLLoader(urls=urls)
    # Implement your loading logic here (if needed)

    # Placeholder for actual summary logic
    return "Summary of the URL content."

# Function to generate responses using the local Llama model
def generate_with_llama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama2",
        "prompt": prompt
    }
    
    response_content = ""
    
    with requests.post(url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")
                try:
                    line_json = json.loads(line_str)
                    response_content += line_json.get("response", "")
                    if line_json.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue
    return response_content

