"""Definitions for common prebuilt crews."""

from __future__ import annotations

from typing import Dict, Callable

from ..agent import Agent
from ..crew import Crew


def _research_crew() -> Crew:
    researcher = Agent(
        role="Researcher",
        goal="Gather up-to-date information from the web",
        backstory="Expert at finding and summarizing information",
    )
    writer = Agent(
        role="Writer",
        goal="Produce clear summaries of research",
        backstory="Turns raw data into digestible reports",
    )
    return Crew(agents=[researcher, writer])


def _coding_crew() -> Crew:
    planner = Agent(
        role="Planner",
        goal="Design software solutions",
        backstory="Breaks problems into modular tasks",
    )
    coder = Agent(
        role="Coder",
        goal="Implement software tasks",
        backstory="Writes clean and efficient code",
        allow_code_execution=True,
    )
    return Crew(agents=[planner, coder])


def _support_crew() -> Crew:
    helper = Agent(
        role="Helper",
        goal="Answer user questions",
        backstory="Friendly assistant ready to help",
    )
    triage = Agent(
        role="Triage",
        goal="Route complex issues to specialists",
        backstory="Understands when to escalate problems",
    )
    return Crew(agents=[helper, triage])


PREBUILT_CREWS: Dict[str, Callable[[], Crew]] = {
    "research": _research_crew,
    "coding": _coding_crew,
    "support": _support_crew,
}


def get_prebuilt_crew(name: str) -> Crew:
    """Return a preconfigured crew by name."""
    try:
        return PREBUILT_CREWS[name]()
    except KeyError as exc:
        raise ValueError(f"Unknown crew: {name}") from exc
