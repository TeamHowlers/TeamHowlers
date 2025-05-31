"""
prompt_builder.py: Builds an LLM prompt from Jira ticket data
"""

def build_gpt_prompt(title, description, labels):
    prompt = f"""
You are a senior developer. Analyze the following Jira ticket and extract:
1. All code or implementation requirements.
2. Acceptance criteria for completion (including coverage, conventions, security, if mentioned).
3. Any assumptions or implied requirements.

---
Title: {title}
---
Description:
{description}
---
Labels: {', '.join(labels) if labels else 'None'}
---
Respond in this JSON format:
{{
  "requirements": ["..."],
  "acceptance_criteria": ["..."],
  "assumptions": ["..."]
}}
"""
    return prompt
