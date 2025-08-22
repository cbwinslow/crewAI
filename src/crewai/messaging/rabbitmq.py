"""RabbitMQ-backed message bus implementation."""

from __future__ import annotations

from typing import Callable

import pika

from .base import MessageBus


class RabbitMQMessageBus(MessageBus):
    """A message bus that uses RabbitMQ for communication."""

    def __init__(self, url: str = "amqp://guest:guest@localhost//") -> None:
        """
        Initialize the RabbitMQMessageBus by opening a pika BlockingConnection and channel.
        
        Parameters:
            url (str): AMQP connection URL used to create pika.URLParameters. Defaults to "amqp://guest:guest@localhost//".
        """
        parameters = pika.URLParameters(url)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    def publish(self, queue: str, message: str) -> None:
        """
        Publish a text message to a RabbitMQ queue.
        
        Declares the queue (idempotent) to ensure it exists, then publishes the given message to the default exchange with the queue name as the routing key.
        
        Parameters:
            queue (str): Destination queue name.
            message (str): Message payload sent as the AMQP message body.
        """
        self._channel.queue_declare(queue=queue)
        self._channel.basic_publish(exchange="", routing_key=queue, body=message)

    def consume(self, queue: str, callback: Callable[[str], None]) -> None:
        """
        Consume messages from a RabbitMQ queue, invoking a callback for each message and acknowledging deliveries.
        
        This method declares the given queue (ensuring it exists), then iterates over messages yielded by the channel's consume generator. For each message, it decodes the body to a string, calls the provided callback with that string, and sends a basic ACK for the message. When the consume generator ends, the consumer is cancelled.
        
        Parameters:
            queue (str): Name of the RabbitMQ queue to consume from.
            callback (Callable[[str], None]): Function to call for each message body (decoded UTF-8 string).
        
        Returns:
            None
        """
        self._channel.queue_declare(queue=queue)
        for method_frame, properties, body in self._channel.consume(queue):
            callback(body.decode())
            self._channel.basic_ack(method_frame.delivery_tag)
        self._channel.cancel()

    def close(self) -> None:
        """
        Close the RabbitMQ connection if it is open.
        
        This method is idempotent: if the underlying pika connection is already closed, no action is taken.
        """
        if not self._connection.is_closed:
            self._connection.close()
