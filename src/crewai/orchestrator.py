"""Simple orchestrator to supervise agent communications."""

from __future__ import annotations

from typing import Dict

from .messaging import MessageBus, CommunicationLogger


class AIOrchestrator:
    """Coordinates agents via a message bus and logs interactions."""

    def __init__(self, bus: MessageBus, logger: CommunicationLogger) -> None:
        self._bus = bus
        self._logger = logger
        self._registry: Dict[str, str] = {}

    def register_agent(self, name: str, queue: str) -> None:
        """Register an agent with the orchestrator."""
        self._registry[name] = queue

    def send(self, agent_name: str, message: str) -> None:
        queue = self._registry.get(agent_name)
        if queue is None:
            raise ValueError(f"Unknown agent: {agent_name}")
        self._bus.publish(queue, message)
        self._logger.log(queue, message)

    def monitor(self, agent_name: str) -> None:
        """Consume and log all pending messages for an agent."""
        queue = self._registry.get(agent_name)
        if queue is None:
            raise ValueError(f"Unknown agent: {agent_name}")

        def _callback(message: str) -> None:
            self._logger.log(queue, message)

        self._bus.consume(queue, _callback)

    def close(self) -> None:
        self._bus.close()
        self._logger.close()
