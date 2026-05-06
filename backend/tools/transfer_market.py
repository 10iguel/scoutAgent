from crewai.tools import tool


@tool("transfer_market")
def transfer_market(player_name: str) -> dict:
    """Fetch transfer market value and current rumours for a player."""
    raise NotImplementedError
