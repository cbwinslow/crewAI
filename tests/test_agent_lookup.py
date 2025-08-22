import httpx
from crewai.utilities.agent_lookup import fetch_agent_definition


def test_fetch_agent_definition():
    payload = {
        "role": "Tester",
        "goal": "Verify components",
        "backstory": "Ensures code quality",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as client:
        agent = fetch_agent_definition("https://example.com/agent.json", client=client)

    assert agent.role == "Tester"
    assert agent.goal == "Verify components"
