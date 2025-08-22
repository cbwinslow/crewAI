"""Abstract message bus interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable


class MessageBus(ABC):
    """Simple interface for message bus implementations."""

    @abstractmethod
    def publish(self, queue: str, message: str) -> None:
        """Publish a message to a queue."""

    @abstractmethod
    def consume(self, queue: str, callback: Callable[[str], None]) -> None:
        """Consume all pending messages from a queue and process with callback."""

    @abstractmethod
    def close(self) -> None:
        """Release any resources held by the bus."""
