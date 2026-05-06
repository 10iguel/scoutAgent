from crewai.tools import tool


@tool("player_stats")
def player_stats(player_name: str) -> dict:
    """Fetch current season stats for a player from Sportmonks API."""
    raise NotImplementedError
