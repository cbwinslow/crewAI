"""Utilities to fetch agent definitions from the web."""

from __future__ import annotations

from typing import Optional

import httpx

from ..agent import Agent


def fetch_agent_definition(url: str, client: Optional[httpx.Client] = None) -> Agent:
    """Retrieve an agent definition from a remote URL."""
    close = False
    if client is None:
        client = httpx.Client()
        close = True
    response = client.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    agent = Agent(**data)
    if close:
        client.close()
    return agent
