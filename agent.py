import json
import os
from typing import Any

from openai import OpenAI
from prompts import PLANNER_PROMPT, EXECUTOR_PROMPT, VERIFIER_PROMPT

MODEL = os.getenv("MODEL","openai/gpt-oss-20b")
MAX_RETRIES = 2


def call_json(client: OpenAI, system_prompt: str, user_prompt: str) -> dict[str, Any]:
    """Call the LLM and parse its JSON response."""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("The model returned an empty response.")
    return json.loads(content)


def make_plan(client: OpenAI, question: str) -> dict[str, Any]:
    return call_json(client, PLANNER_PROMPT, json.dumps({"question": question}))


def execute_plan(client: OpenAI, question: str, plan: dict[str, Any]) -> dict[str, Any]:
    payload = {"question": question, "plan": plan}
    return call_json(client, EXECUTOR_PROMPT, json.dumps(payload))


def verify_solution(
    client: OpenAI, question: str, plan: dict[str, Any], solution: dict[str, Any]
) -> dict[str, Any]:
    payload = {"question": question, "plan": plan, "proposed_solution": solution}
    return call_json(client, VERIFIER_PROMPT, json.dumps(payload))


def solve(question: str, client: OpenAI | None = None) -> dict[str, Any]:
    """Run planner -> executor -> verifier, retrying when verification fails."""
    question = question.strip()
    if not question:
        return {
            "answer": "",
            "status": "failed",
            "reasoning_visible_to_user": "Please provide a question to solve.",
            "metadata": {
                "plan": "",
                "checks": [],
                "retries": 0,
            },
        }

    client = client or OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
    last_plan: dict[str, Any] = {}
    checks: list[dict[str, Any]] = []

    for attempt in range(MAX_RETRIES + 1):
        try:
            last_plan = make_plan(client, question)
            solution = execute_plan(client, question, last_plan)
            verification = verify_solution(client, question, last_plan, solution)

            passed = verification.get("passed") is True
            check = {
                "check_name": "llm_independent_verification",
                "passed": passed,
                "details": str(verification.get("details", "No details provided.")),
            }
            checks.append(check)

            if passed:
                return {
                    "answer": str(solution.get("answer", "")),
                    "status": "success",
                    "reasoning_visible_to_user": str(
                        solution.get(
                            "short_explanation",
                            "The answer was checked before it was returned.",
                        )
                    ),
                    "metadata": {
                        "plan": last_plan,
                        "checks": checks,
                        "retries": attempt,
                    },
                }

            # The next loop reruns planning and execution. Feedback helps the model
            # correct the previous attempt without exposing hidden reasoning to users.
            question = (
                f"{question}\n\nPrevious attempt failed verification. "
                f"Verifier feedback: {verification.get('details', 'Re-check the solution.')}"
            )

        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            checks.append({
                "check_name": "valid_json",
                "passed": False,
                "details": f"Could not parse a valid model response: {exc}",
            })
        except Exception as exc:
            checks.append({
                "check_name": "agent_execution",
                "passed": False,
                "details": f"Agent call failed: {type(exc).__name__}: {exc}",
            })
            break

    return {
        "answer": "I couldn't verify a reliable answer.",
        "status": "failed",
        "reasoning_visible_to_user": (
            "The proposed solution did not pass verification after the allowed attempts."
        ),
        "metadata": {
            "plan": last_plan,
            "checks": checks,
            "retries": min(len(checks), MAX_RETRIES),
        },
    }


def main() -> None:
    print("Multi-Step Reasoning Agent (type 'exit' to quit)")
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        result = solve(question)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
