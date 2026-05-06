from crewai.tools import tool


@tool("predictive")
def predictive(player_name: str) -> dict:
    """Predict a player's summer World Cup trajectory based on current form."""
    raise NotImplementedError
