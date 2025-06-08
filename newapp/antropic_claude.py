import requests
import os

# Set your Claude API key here
#CLAUDE_API_KEY = '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'
#CLAUDE_API_KEY = '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'

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

