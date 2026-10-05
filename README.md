# Self-Improving Clinical Scheduling Agent

A production-grade, self-correcting clinical scheduling assistant framework built using a local LLM optimization pipeline. This repository demonstrates a closed-loop multi-turn agent evaluation harness that flags constraint violations, synthesizes structured prompts on the fly, and validates improvements without code regression.

## System Architecture
- **`storage.py`**: A mock clinical database with an integrated **Deterministic Validation State Machine** enforcing clinic hours and slot constraints.
- **`agent.py`**: The primary scheduler agent that reads dynamic rules out of persistent memory and dynamically handles customer intent.
- **`simulator.py`**: A synthetic patient harness that tests the scheduling agent over multiple turns with varying clinical personas.
- **`evaluation.py`**: An automated compliance judge executing strict rubric analysis and auditing database state changes.
- **`run_loop.py`**: The core runtime orchestrator closing the self-improvement loop across two sequential test runs.

## Setup and Running Instructions

1. **Install Python Libraries:**
   ```bash
   pip install ollama pydantic
   ```

2. **Register the Local LLM Wrapper Engine:**
   Ensure Ollama is running locally, then initialize the optimized agent blueprint:
   ```bash
   ollama create clinic-llama -f Modelfile
   ```

3. **Execute the E2E Self-Improving Loop Pipeline:**
   ```bash
   python run_loop.py
   ```
