"""In-memory message bus for testing and simple scenarios."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict, List

from .base import MessageBus


class InMemoryMessageBus(MessageBus):
    """A message bus that stores messages in memory."""

    def __init__(self) -> None:
        """
        Initialize the in-memory message bus.
        
        Creates the internal queue storage as a defaultdict mapping queue names to lists of messages; new queues are created automatically on first access.
        """
        self._queues: DefaultDict[str, List[str]] = defaultdict(list)

    def publish(self, queue: str, message: str) -> None:
        """
        Publish a message to an in-memory queue.
        
        Appends `message` to the end of the list for `queue`. If the queue does not yet exist it is created automatically (using the bus's internal in-memory storage). This is synchronous and does not return a value.
        
        Parameters:
            queue (str): Name of the target queue.
            message (str): Message payload to append to the queue.
        """
        self._queues[queue].append(message)

    def consume(self, queue: str, callback: Callable[[str], None]) -> None:
        """
        Consume all messages currently queued for `queue` by invoking `callback` for each message.
        
        This method takes a snapshot of the messages present at call time, clears the queue, and then calls `callback(message)` for each message in FIFO order. Processing is synchronous; exceptions raised by `callback` propagate to the caller.
        """
        messages = list(self._queues.get(queue, []))
        self._queues[queue] = []
        for message in messages:
            callback(message)

    def close(self) -> None:
        """
        Clear all in-memory queues and discard any pending messages.
        
        This removes all stored queues and their messages from the bus. It is synchronous and irreversible — any messages not yet consumed will be lost.
        """
        self._queues.clear()
