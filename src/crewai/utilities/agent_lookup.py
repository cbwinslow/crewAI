"""Utilities to fetch agent definitions from the web."""

from __future__ import annotations

from typing import Optional

import httpx

from ..agent import Agent


def fetch_agent_definition(url: str, client: Optional[httpx.Client] = None) -> Agent:
    """
    Fetch an Agent definition from the given URL and return an Agent instance.
    
    Performs an HTTP GET on the provided URL, validates the response status (calls
    response.raise_for_status()), parses the response body as JSON, and constructs
    an Agent by unpacking the JSON object into Agent(**data). If no httpx.Client
    is supplied, a temporary client is created and closed before returning.
    
    Returns:
    	Agent: An Agent instance built from the JSON response.
    
    Raises:
    	httpx.HTTPStatusError: If the HTTP response status is not successful (raised by response.raise_for_status()).
    """
    close = False
    if client is None:
        client = httpx.Client()
        close = True
    response = client.get(url)
    response.raise_for_status()
    data = response.json()
    agent = Agent(**data)
    if close:
        client.close()
    return agent
