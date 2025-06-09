import requests
import os

# Set your Claude API key here

# Claude API endpoint
CLAUDE_API_URL = "https://api.anthropic.com/v1/complete"

def ask_claude(prompt):
    headers = {
        "Authorization": f"Bearer {CLAUDE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "Claude-v1",  # Claude's model
        "max_tokens_to_sample": 300  # Limit for Claude's response length
    }
    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["completion"]
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    prompt = "What is the future of AI in healthcare?"
    response = ask_claude(prompt)
    print("Claude's Response: ", response)

