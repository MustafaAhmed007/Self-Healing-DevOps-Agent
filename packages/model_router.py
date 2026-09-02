from __future__ import annotations

import os


class ModelRouter:
    """Task-aware model selection facade.

    LiteLLM/Ollama adapters are intentionally optional so the core remains runnable offline.
    """

    def __init__(self) -> None:
        self.default = os.getenv("MODEL_DEFAULT", "ollama/llama3.2")
        self.reasoning = os.getenv("MODEL_REASONING", self.default)
        self.coding = os.getenv("MODEL_CODING", self.default)

    def model_for(self, task: str) -> str:
        if task in {"diagnosis", "reflection", "verification"}:
            return self.reasoning
        if task in {"patch", "code_analysis"}:
            return self.coding
        return self.default
