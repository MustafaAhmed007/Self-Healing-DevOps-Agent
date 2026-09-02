from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    github_token: str | None = None
    database_url: str = "postgresql://repair:repair@localhost:5432/repair"
    redis_url: str = "redis://localhost:6379/0"
    ollama_base_url: str = "http://localhost:11434"
    max_iterations: int = 3
    max_tokens: int = 50_000
    max_cost_usd: float = 5.0
    sandbox_network: bool = False
    model_default: str = "ollama/llama3.2"
    model_reasoning: str | None = None
    model_coding: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")


settings = Settings()
