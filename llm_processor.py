"""
llm_processor.py - Invokes GPT-4 (or OpenAI API) with a prompt and returns the parsed result.
"""
import os
import openai
from dotenv import load_dotenv
load_dotenv()

# User must set OPENAI_API_KEY in env or config
# export OPENAI_API_KEY=... if using bash, or set in Env Variables on Windows

def ask_gpt(prompt, model="gpt-4"):    
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=800
    )
    # Try to extract valid JSON from the reply
    import json
    import re
    content = response['choices'][0]['message']['content']
    # Extract first {...} json block from content
    match = re.search(r'\{[\s\S]*?\}', content)
    if match:
        content_json = match.group(0)
        return json.loads(content_json)
    # fallback: try parsing whole content
    try:
        return json.loads(content)
    except Exception:
        return {"raw": content}
