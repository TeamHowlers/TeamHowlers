"""
code_writer.py - Converts requirements and acceptance criteria to code and test files via LLM or templates.
"""

import os
import openai


def instruct_gpt(requirements, acceptance_criteria, assumptions=None, file_context=None, model="gpt-4"):
    """
    Calls GPT-4 to generate production-quality code based on requirements.
    Optionally passes related file context to help LLM generate correct code.
    Returns: {filename: content} dict for all suggested files (including test files)
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    prompt = f"""
        You are an expert software engineer. Generate production-quality code for the following requirements:

        Requirements:
        {requirements}
        
        Acceptance criteria:
        {acceptance_criteria}
        
        Assumptions:
        {assumptions or ''}
        
        Provide each file as a markdown code block, like:
        ```python
        # path/to/filename.py\n<file contents>
        ```
        or
        ```javascript
        // path/to/file.js\n<file contents>
        ```
        Ensure that test code is provided for each relevant function or component, using appropriate conventions (pytest, unittest in Python; Jest in JS; etc). Make sure generated code passes linting tools or formatters (Black/Prettier/ESLint).
        Respond with only code blocks.
    """
    if file_context:
        prompt += f"\n\nContext from existing files:\n{file_context}\n\n---"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1500
    )
    # Extract code blocks + filenames
    import re
    blocks = re.findall(r'```([a-zA-Z0-9]+)\n([^`]+)```', response['choices'][0]['message']['content'])
    files = {}
    for lang, block in blocks:
        lines = block.split('\n')
        if lines and lines[0].startswith(('#', '//')) and lines[0].strip():
            path = lines[0].lstrip('#/ ').strip()
            content = '\n'.join(lines[1:]).strip()
            files[path] = content
    return files
