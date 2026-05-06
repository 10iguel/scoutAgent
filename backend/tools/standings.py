from crewai.tools import tool


@tool("standings")
def standings(league_id: int) -> dict:
    """Fetch live league table standings from Sportmonks API."""
    raise NotImplementedError
