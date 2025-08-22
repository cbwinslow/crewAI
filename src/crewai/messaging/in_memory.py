"""In-memory message bus for testing and simple scenarios."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict, List

from .base import MessageBus


class InMemoryMessageBus(MessageBus):
    """A message bus that stores messages in memory."""

    def __init__(self) -> None:
        self._queues: DefaultDict[str, List[str]] = defaultdict(list)

    def publish(self, queue: str, message: str) -> None:
        self._queues[queue].append(message)

    def consume(self, queue: str, callback: Callable[[str], None]) -> None:
        messages = list(self._queues.get(queue, []))
        self._queues[queue] = []
        for message in messages:
            callback(message)

    def close(self) -> None:
        self._queues.clear()
