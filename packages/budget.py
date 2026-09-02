from dataclasses import dataclass


@dataclass
class Budget:
    max_iterations: int = 3
    max_tokens: int = 50_000
    max_cost_usd: float = 5.0
    max_runtime_seconds: int = 1_800

    def allow(self, iteration: int, tokens: int, cost_usd: float, runtime_seconds: int) -> bool:
        return (
            iteration <= self.max_iterations
            and tokens <= self.max_tokens
            and cost_usd <= self.max_cost_usd
            and runtime_seconds <= self.max_runtime_seconds
        )
