# Multi-Step Reasoning Agent with Self-Checking

A small Python project implementing the Planner → Executor → Verifier loop described in the interview assignment.

## Requirements
- Python 3.10+
- An OpenAI API key for live LLM calls

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:OPENAI_API_KEY="your_api_key_here"
python agent.py
```

## Run
Type a word problem at `Question:`. Type `exit` to quit.

Example:
```text
Question: Alice has 3 red apples and twice as many green apples. How many total?
```

The program prints a JSON object with `answer`, `status`, `reasoning_visible_to_user`, and `metadata`.

## Project structure
- `agent.py`: orchestration, API calls, retries, output formatting, CLI
- `prompts.py`: separate Planner, Executor, and Verifier prompts
- `tests/test_agent.py`: offline orchestration tests using a fake client
- `requirements.txt`: Python dependency

## Run tests
```powershell
python -m unittest discover -s tests -v
```
Tests do not call the API. They check successful verification, retry behavior, and empty input.

## Design choices
- Prompts are separated from orchestration to make them easy to inspect and tune.
- Temperature is set to 0 for more consistent structured responses.
- JSON mode is requested to reduce malformed output.
- The verifier receives the original question and proposed solution and checks it independently.
- The agent retries at most twice after the first attempt.
- The full private chain-of-thought is not returned; users receive a concise explanation. Metadata is intended for debugging/evaluation.

## Assumptions and limitations
- This baseline uses an LLM verifier, so verification is not a mathematical guarantee.
- For stronger reliability, add deterministic Python validators for arithmetic, time arithmetic, non-negative counts, and slot boundaries.
- The retry loop appends verifier feedback to the question for the next attempt.
- Keep your API key in an environment variable; never commit it to Git.
- The three example sets are embedded in `prompts.py`; the test suite adds executable examples.
