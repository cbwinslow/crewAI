from crewai.crews.prebuilt import get_prebuilt_crew


def test_research_crew_structure():
    crew = get_prebuilt_crew("research")
    assert len(crew.agents) == 2
    roles = {agent.role for agent in crew.agents}
    assert "Researcher" in roles and "Writer" in roles
