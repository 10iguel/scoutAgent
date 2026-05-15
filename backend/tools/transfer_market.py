import requests, os, json
from pathlib import Path
from crewai.tools import tool

CACHE = Path("backend/.cache/transfers")
CACHE.mkdir(parents=True, exist_ok=True)
HEADERS = {"x-apisports-key": os.getenv("API_SPORTS_KEY")}


@tool("transfer_market")
def transfer_market(player_id: int) -> str:
    """Fetches transfer history and fee values for a player.
    Requires a numeric player ID — use search_player tool first."""

    cache_file = CACHE / f"{player_id}.json"
    if cache_file.exists():
        return cache_file.read_text()

    resp = requests.get(
        "https://v3.football.api-sports.io/transfers",
        headers=HEADERS,
        params={"player": player_id}
    )
    data = resp.json().get("response", [{}])[0]

    # Clean it up for the agent
    transfers = [
        {
            "date": t["date"],
            "fee": t["type"],  # e.g. "€ 80M" or "Free Transfer"
            "from": t["teams"]["out"]["name"],
            "to": t["teams"]["in"]["name"],
        }
        for t in data.get("transfers", [])
    ]

    result = {
        "player": data.get("player", {}).get("name"),
        "transfer_history": transfers,
        "most_recent_fee": transfers[0]["fee"] if transfers else "Unknown"
    }

    output = json.dumps(result)
    cache_file.write_text(output)
    return output