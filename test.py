import requests
import json

# Define the URL for the Ollama API
url = "http://localhost:11434/api/generate"

# Define the payload with the model name and prompt
payload = {
    "model": "llama2",
    "prompt": "Why is the sky blue?"
}

# Make the POST request and check if response is streamed
with requests.post(url, json=payload, stream=True) as response:
    response_content = ""
    
    print("Raw response content:")

    # Stream and parse each line of the response
    for line in response.iter_lines():
        if line:
            line_str = line.decode("utf-8")

            try:
                # Try parsing the line as JSON
                line_json = json.loads(line_str)
                print(line_json.get("response",""))
                response_content += line_json.get("response", "")

                # Check if the "done" flag is set to true
                if line_json.get("done", False):
                    break
            except json.JSONDecodeError:
                print("Failed to parse line as JSON; skipping:", line_str)
                continue

# Final parsed response after all lines are processed
print("Parsed Response Content:")
print(response_content)