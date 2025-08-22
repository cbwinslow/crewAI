from crewai.messaging import InMemoryMessageBus, CommunicationLogger
from crewai.orchestrator import AIOrchestrator


def test_orchestrator_send_and_monitor(tmp_path):
    bus = InMemoryMessageBus()
    logger = CommunicationLogger(tmp_path / "comm.db")
    orch = AIOrchestrator(bus, logger)
    orch.register_agent("agent1", "q1")
    orch.send("agent1", "hello")
    bus.publish("q1", "reply")
    orch.monitor("agent1")
    rows = logger.fetch_all()
    messages = [r[2] for r in rows]
    assert "hello" in messages
    assert "reply" in messages
    orch.close()
