\# DESIGN NOTE: Self-Improving Scheduling Agent



\## Key Design Choices \& System Architecture

To maximize clinical safety and deterministic behavior, this system completely decouples state tracking and constraint verification from the open-ended LLM logic. The architecture consists of:

1\. \*\*Deterministic State Machine (DSM)\*\* inside `storage.py`. The LLM agent can propose state mutations via structured keywords, but the DSM validates boundary parameters (e.g., clinic operating hours) before altering records.

2\. \*\*Dynamic System Prompts via Isolated Injections\*\*. Instead of allowing an untrusted AI to rewrite its own source files, the meta-optimizer loop compiles structured directives into a local `dynamic\_rules.json` file. The agent reads this file during startup and appends the guidelines into its system instructions context safely.



\## The Self-Improvement Loop \& Scores

\- \*\*Run 1 (Baseline Agent):\*\* Assessed with an out-of-bounds patient slot profile request. The baseline agent failed to firmly deny the booking, leading to a failing audit score of \*\*40/100\*\*.

\- \*\*Meta-Optimization Action:\*\* The pipeline intercepted the failure anomaly and automatically compiled a new runtime behavioral instruction: \*"Check and deny requests before 9:00 AM without tool calls or lookups."\*

\- \*\*Run 2 (Self-Improved Agent):\*\* The agent automatically loaded the injected directive. On re-evaluation, it immediately blocked the out-of-bounds time frame requests, moving the final audit score to a perfect \*\*100/100 | Passed: True\*\*.



\## Production Hardening: What I Would Change

For a live clinic deployment, I would swap the open-ended text string optimization mechanism for a formal \*\*Configurable Policy Guardrail Engine\*\* (such as NeMo Guardrails or AWS Bedrock Guardrails) matched with a hard schema validation layer. Allowing an AI model to dynamically compile text that directly reshapes system guidance payloads introduces long-term non-deterministic behavior and vulnerabilities to prompt injection.



\## AI Co-Pilot vs. Human Judgment

\- \*\*Where AI Helped:\*\* Boilerplate script generation for multi-turn conversational data tracking structures, synthetic patient data generation, and rapid local framework troubleshooting.

\- \*\*Human Judgment Overrides:\*\* I rejected the use of fully autonomous multi-agent orchestration stacks (like CrewAI or AutoGen) recommended by standard AI prompts. In a real healthcare scenario, autonomous multi-agent loops introduce state volatility that is inherently unsafe. I restricted the core loop to a single agent verified by a hard-coded database constraint layer.



