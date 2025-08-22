import httpx
from crewai.utilities.agent_lookup import fetch_agent_definition


def test_fetch_agent_definition():
    payload = {
        "role": "Tester",
        "goal": "Verify components",
        "backstory": "Ensures code quality",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        """
        Mock HTTP request handler that always returns a 200 OK response with the predefined JSON payload.
        
        This function is intended for use with httpx.MockTransport in tests. It ignores the incoming request and responds with an httpx.Response containing the `payload` variable from the enclosing scope serialized as JSON.
        
        Parameters:
            request (httpx.Request): Incoming HTTP request (ignored).
        
        Returns:
            httpx.Response: HTTP 200 response with the JSON body set to `payload`.
        """
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as client:
        agent = fetch_agent_definition("https://example.com/agent.json", client=client)

    assert agent.role == "Tester"
    assert agent.goal == "Verify components"
