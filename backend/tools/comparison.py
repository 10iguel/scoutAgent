from crewai.tools import tool


@tool("comparison")
def comparison(player_name: str, legend_name: str) -> dict:
    """Compare a current player's stats against a World Cup legend."""
    raise NotImplementedError
