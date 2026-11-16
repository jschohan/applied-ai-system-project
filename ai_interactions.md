# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code to add an agentic Gemini workflow (plan -> act -> check -> explain) plus a reliability/testing harness to the music recommender, fully integrated into `main.py`, keeping the deterministic scorer unchanged. I had it enter plan mode first to check my plan against the repo.

**Prompts used:**

- "Add an agentic Gemini workflow + reliability harness to my music recommender" (full spec: loop design, validation, fallback, `--query/--eval/--verbose`, mocked-LLM tests, free-tier key from `.env`).
- "Start by entering plan mode: read the code, confirm this plan against what's actually in the repo, and flag anything that conflicts before writing code."

**What did the agent generate or change?**

New: `src/agent.py`, `src/llm_client.py`, `src/evaluate.py`, `tests/test_agent.py`. Edited: `src/recommender.py` (`validate_profile`, `check_invariants`, `vocabulary`, `quiet` flag on `load_songs`, stale comment removed), `src/main.py` (argparse, `--query/--eval/--verbose`, profiles validated), `tests/test_recommender.py` (rewritten), `requirements.txt`, `.gitignore`, `model_card.md`. Commands run: pip install, pytest, live `--query` and `--eval` runs against Gemini.

**What did you verify or fix manually?**

- Plan review caught conflicts before coding: `main.py` flag parsing couldn't take `--query` text, `.env` wasn't git-ignored, and the "country / depressing" profile uses a mood not in the catalog.
- The agent first got model names from a subagent's web fetch that looked odd (e.g. `gemini-3.8-flash`, a different SDK API). It did not trust it and checked the installed SDK, listed models with the real key, and made a live structured-output call before choosing a default.
- One agent test was wrong, not the code (a scripted critic reply rated the last iteration 5). Fixed the test.
- Found while running: the critic can't fix a request the catalog can't satisfy ("not too acoustic"). Documented rather than hidden.
- Not verified by me: free-tier rate limits (docs fetched did not list them).

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
