# Multi-Step Reasoning Agent with Self-Checking

## 📌 Project Overview

This project implements a Multi-Step Reasoning Agent that solves questions using three stages:

1. **Planner** — Breaks the question into smaller, logical steps.
2. **Executor** — Solves the question by following the plan.
3. **Verifier** — Checks the answer and provides feedback if corrections are needed.

If the Verifier rejects an answer, the Executor gets another chance to improve it. The agent allows up to two retries after the initial attempt.

## 🛠️ Technologies Used

- Python
- Large Language Models (LLMs)
- Groq API
- OpenAI Python SDK
- JSON

## 📂 Project Structure

```text
multistep_reasoning_agent/
│
├── agent.py
├── prompts.py
├── requirements.txt
├── README.md
└── tests/
    └── test_agent.py
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/DEEPIKA-R-K/Multi-step-reasoning-agent.git
cd multistep_reasoning_agent
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the API Key

This project supports Groq and OpenAI API access.

For Groq, create an API key through the [Groq Console](https://console.groq.com/keys).

Set the key in PowerShell:

```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

Set the model:

```powershell
$env:LLM_MODEL="openai/gpt-oss-20b"
```

Keep your API key private. Never commit it to GitHub.

### 5. Run the Application

```bash
python agent.py
```

Enter a question when prompted. The application returns a JSON response containing the plan, answer, explanation, verification result, and number of attempts.

## 🧠 Prompt Design

All system prompts are defined in `prompts.py`.

### 1. Planner Prompt

The Planner converts the user's question into a sequence of actionable steps.

**Design decision:** It is instructed to plan without solving the question. This separates planning from execution.

### 2. Executor Prompt

The Executor follows the plan and generates an answer with a brief explanation.

**Design decision:** It receives structured instructions and returns JSON, making its output easier for Python to process.

### 3. Verifier Prompt

The Verifier independently checks the answer for correctness, relevance, and consistency.

**Design decision:** It can reject an answer and provide feedback for another attempt instead of automatically accepting the Executor's response.

### Why Use Separate Prompts?

Each prompt defines one component's responsibility and expected output format. This improves modularity, makes the workflow easier to maintain, and allows each stage to be tested separately.

## 🔄 Workflow

```text
User Question
     |
     v
   Planner
     |
     v
   Executor
     |
     v
   Verifier
     |
     v
Answer Passed?
   /       \
 Yes        No
  |          |
  v          v
Return     Retry Executor
Answer     with Feedback
              |
              v
       Retry Limit Reached?
```

The agent performs an initial execution and allows up to two retries if verification fails.

## 📝 Example Questions

The agent can be tested with questions such as:

- What is 18% of 250?
- Convert 2.5 hours to minutes.
- What is the average of 10, 20, and 30?
- Explain the difference between a Python list and a tuple.
- A notebook costs ₹40. What do three notebooks cost?

See `example_run_logs.md` for the example questions and output format. Replace illustrative outputs with actual results from your runs before submitting.

## ⚠️ Assumptions and Limitations

- The selected model must support JSON-object response mode.
- The Planner is expected to return a non-empty list of steps.
- The Verifier is expected to return a Boolean `passed` field and feedback.
- Verification relies on an LLM and does not guarantee correctness.
- The Verifier may overlook errors or reject a correct answer.
- Multiple LLM calls increase response time and API usage.
- The agent does not use external tools or a retrieval system.
- API availability, model access, and rate limits depend on the provider and account.

## 🔍 What Did Not Work Well?

- Prompt instructions alone cannot guarantee correct answers or valid JSON.
- The Executor and Verifier may share similar reasoning limitations.
- Multiple stages increase latency and API usage.
- Vague verification feedback may not help the Executor correct an error.
- Model support for structured JSON output can vary.

## 🚀 Future Improvements

With more development time, I would:

- Add automated evaluation using questions with known answers.
- Add task-specific validation for calculations and structured outputs.
- Improve error handling for API failures and rate limits.
- Record response time and token usage for each stage.
- Expand unit tests for retries, malformed JSON, and invalid responses.
- Add external tools or retrieval for questions requiring current information.
- Save real example runs for reproducible evaluation.

## 🧪 Testing

Run the unit tests with:

```bash
python -m unittest discover -s tests
```

These tests cover basic input validation and missing API-key handling.

## 📄 Example Run Logs

The `example_run_logs.md` file contains suggested test questions and illustrative output examples.

For the final submission, run the agent and include **5–10 actual question-and-answer logs**. Do not present mock outputs as real execution results.

## 👩‍💻 Author

Created as a project demonstrating multi-step LLM reasoning, prompt engineering, structured outputs, and self-checking.
