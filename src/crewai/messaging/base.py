"""Abstract message bus interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable


class MessageBus(ABC):
    """Simple interface for message bus implementations."""

    @abstractmethod
    def publish(self, queue: str, message: str) -> None:
        """
        Publish a message to the specified queue.
        
        Parameters:
            queue (str): Name of the target queue.
            message (str): Message payload to publish.
        """

    @abstractmethod
    def consume(self, queue: str, callback: Callable[[str], None]) -> None:
        """
        Consume (drain) all pending messages from the named queue, invoking `callback` once for each message.
        
        This method should synchronously (from the caller's perspective) retrieve every pending message from `queue` and pass each message body as a single `str` argument to `callback`. Implementations are expected to call `callback` for every message in the queue; behavior for concurrent consumers, ordering guarantees, retry semantics, and blocking behavior depend on the concrete implementation.
        
        Parameters:
            queue (str): Name of the queue or topic to consume from.
            callback (Callable[[str], None]): Function called for each message; receives the message body as a `str`.
        """

    @abstractmethod
    def close(self) -> None:
        """Release any resources held by the bus."""
