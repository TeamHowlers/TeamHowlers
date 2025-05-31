"""
main.py - Fully automated Jira-to-code workflow
"""
import sys
from jira_fetcher import get_jira_ticket
from prompt_builder import build_gpt_prompt
from llm_processor import ask_gpt
from code_writer import instruct_gpt
import os
import pathlib
from test_runner import run_pytest, run_jest_tests

import shutil

from dotenv import load_dotenv
load_dotenv()

def save_generated_files(files_dict):
    """Save all generated files to respective paths."""
    for filepath, content in files_dict.items():
        abs_path = os.path.abspath(filepath)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <JIRA-TICKET-ID>")
        sys.exit(1)
    ticket_id = sys.argv[1]
    print(f"Fetching Jira ticket {ticket_id}...")
    data = get_jira_ticket(ticket_id)
    print(f"Title: {data['title']}\nLabels: {data['labels']}\nDesc (first 100 chars): {str(data['description'])[:100]}...")

    # Build prompt for requirements and acceptance criteria
    prompt = build_gpt_prompt(data['title'], data['description'], data['labels'])
    print("\nExtracting requirements/criteria/assumptions from GPT-4...")
    analysis = ask_gpt(prompt)
    requirements = "\n".join(analysis.get('requirements', []))
    acceptance_criteria = "\n".join(analysis.get('acceptance_criteria', []))
    assumptions = "\n".join(analysis.get('assumptions', []))
    print("\nGPT-4 summaries:")
    print("REQUIREMENTS:\n", requirements)
    print("ACCEPTANCE CRITERIA:\n", acceptance_criteria)
    print("ASSUMPTIONS:\n", assumptions)

    # Generate production code + test files
    print("\nGenerating code and tests via GPT-4...")
    files_dict = instruct_gpt(requirements, acceptance_criteria, assumptions)
    if not files_dict:
        print("No code generated.")
        sys.exit(2)
    save_generated_files(files_dict)
    print(f"Saved {len(files_dict)} file(s): ", list(files_dict.keys()))

    # Run tests (priority: Python, fallback: JS/Jest)
    tested = False
    print("\nRunning Python tests (pytest+coverage) if any\u2026")
    testfiles = [f for f in files_dict.keys() if f.endswith(".py") and ("test" in f or "tests" in f)]
    if testfiles:
        ok, cov, output = run_pytest()
        print("Pytest output:\n", output)
        print(f"Coverage: {cov}%\nSuccess: {ok}")
        if ok and (cov is None or cov >= 80):
            tested = True
        else:
            print("Test failures or insufficient coverage. Please review and retry fixes.")
    if not tested:
        print("\nTrying to run Jest tests (JS/TS)\u2026")
        ok, cov, output = run_jest_tests()
        print(output)
        print(f"Jest Coverage: {cov}%\nSuccess: {ok}")
        ok, cov, output = run_pytest()
        if not ok or cov < 80:
            tested = True
        else:
            print("Test failures or insufficient coverage in JS/TS.")
    if tested:
        print("All tests passed and coverage ok! Workflow complete.")
    else:
        print("❌ Some tests failed or coverage was <80%. Review suggested fixes.")

if __name__ == "__main__":
    main()
