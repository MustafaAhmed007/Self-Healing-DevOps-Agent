from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable


class InProcessQueue:
    def __init__(self, workers: int = 2):
        self.queue: asyncio.Queue[str] = asyncio.Queue()
        self.workers = workers

    async def submit(self, run_id: str) -> None:
        await self.queue.put(run_id)

    async def worker(self, handler: Callable[[str], Awaitable[None]]) -> None:
        while True:
            run_id = await self.queue.get()
            try:
                await handler(run_id)
            finally:
                self.queue.task_done()


class RedisQueue:
    def __init__(self, url: str, key: str = "shda:repairs"):
        try:
            import redis
        except ImportError as exc:
            raise RuntimeError("install the 'redis' extra to use RedisQueue") from exc
        self.redis = redis.Redis.from_url(url, decode_responses=True)
        self.key = key

    def submit(self, run_id: str) -> None:
        self.redis.rpush(self.key, json.dumps({"run_id": run_id}))

    def receive(self, timeout: int = 5) -> str | None:
        item = self.redis.blpop(self.key, timeout=timeout)
        return json.loads(item[1])["run_id"] if item else None
