"""RabbitMQ-backed message bus implementation."""

from __future__ import annotations

from typing import Callable

import pika

from .base import MessageBus


class RabbitMQMessageBus(MessageBus):
    """A message bus that uses RabbitMQ for communication."""

    def __init__(self, url: str = "amqp://guest:guest@localhost//") -> None:
        parameters = pika.URLParameters(url)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    def publish(self, queue: str, message: str) -> None:
        self._channel.queue_declare(queue=queue)
        self._channel.basic_publish(exchange="", routing_key=queue, body=message)

    def consume(self, queue: str, callback: Callable[[str], None]) -> None:
        self._channel.queue_declare(queue=queue)
        for method_frame, properties, body in self._channel.consume(queue):
            callback(body.decode())
            self._channel.basic_ack(method_frame.delivery_tag)
        self._channel.cancel()

    def close(self) -> None:
        if not self._connection.is_closed:
            self._connection.close()
