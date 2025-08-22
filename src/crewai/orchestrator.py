"""Simple orchestrator to supervise agent communications."""

from __future__ import annotations

from typing import Dict

from .messaging import MessageBus, CommunicationLogger


class AIOrchestrator:
    """Coordinates agents via a message bus and logs interactions."""

    def __init__(self, bus: MessageBus, logger: CommunicationLogger) -> None:
        """
        Initialize the orchestrator with a message bus and a communication logger.
        
        Sets internal references to the provided MessageBus and CommunicationLogger and initializes an empty registry mapping agent names (str) to queue names (str).
        """
        self._bus = bus
        self._logger = logger
        self._registry: Dict[str, str] = {}

    def register_agent(self, name: str, queue: str) -> None:
        """
        Register or update an agent's queue mapping in the orchestrator.
        
        Adds a mapping from agent `name` to the message bus `queue`. If the agent
        was previously registered, its queue is overwritten.
        
        Parameters:
            name (str): Agent identifier.
            queue (str): Message bus queue name that the agent listens on.
        """
        self._registry[name] = queue

    def send(self, agent_name: str, message: str) -> None:
        """
        Send a text message to a registered agent's queue and record the transmission.
        
        Lookup the agent's queue by name, publish `message` to that queue via the message bus, and log the delivered message. Raises ValueError if `agent_name` is not registered.
        
        Parameters:
            agent_name (str): Name of the target agent; must be registered with register_agent.
            message (str): The text payload to publish and log.
        
        Raises:
            ValueError: If the agent name is unknown.
        """
        queue = self._registry.get(agent_name)
        if queue is None:
            raise ValueError(f"Unknown agent: {agent_name}")
        self._bus.publish(queue, message)
        self._logger.log(queue, message)

    def monitor(self, agent_name: str) -> None:
        """
        Start consuming messages from the registered agent's queue and log each received message.
        
        Looks up the agent's queue by name, subscribes a callback with the message bus that forwards every consumed message to the communication logger.
        
        Raises:
            ValueError: If `agent_name` is not registered.
        """
        queue = self._registry.get(agent_name)
        if queue is None:
            raise ValueError(f"Unknown agent: {agent_name}")

        def _callback(message: str) -> None:
            """
            Log a consumed message to the orchestrator's communication logger for the associated queue.
            
            Parameters:
                message (str): The consumed message payload to record under the bound queue name.
            """
            self._logger.log(queue, message)

        self._bus.consume(queue, _callback)

    def close(self) -> None:
        """
        Close the orchestrator and release its resources.
        
        Closes the underlying message bus and the communication logger. After calling this method the orchestrator should not be used to send or monitor agents.
        """
        self._bus.close()
        self._logger.close()
