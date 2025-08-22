from crewai.messaging import InMemoryMessageBus, CommunicationLogger


def test_in_memory_message_bus_and_logger(tmp_path):
    bus = InMemoryMessageBus()
    db_path = tmp_path / "comm.db"
    logger = CommunicationLogger(db_path)

    bus.publish("queue", "hello")

    def consumer(msg: str) -> None:
        logger.log("queue", msg)

    bus.consume("queue", consumer)

    rows = logger.fetch_all()
    assert rows[0][1] == "queue"
    assert rows[0][2] == "hello"
    logger.close()
