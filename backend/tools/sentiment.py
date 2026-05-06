from crewai.tools import tool


@tool("sentiment")
def sentiment(player_name: str) -> dict:
    """Analyse news and social media sentiment for a player."""
    raise NotImplementedError
