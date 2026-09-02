from __future__ import annotations

import os
from .engine import RepairEngine
from .persistence import MemoryRepository, PostgresRepository
from .queue import RedisQueue


def main() -> None:
    queue = RedisQueue(os.environ["REDIS_URL"])
    repository = PostgresRepository(os.environ["DATABASE_URL"]) if os.getenv("DATABASE_URL") else MemoryRepository()
    engine = RepairEngine(repository=repository)
    while True:
        run_id = queue.receive(timeout=30)
        if run_id:
            # Queue payloads are intentionally IDs; a production scheduler should persist the full job request.
            state = repository.get(run_id)
            if state:
                engine.start(state.issue)


if __name__ == "__main__":
    main()
