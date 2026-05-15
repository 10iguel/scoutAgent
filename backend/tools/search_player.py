import requests, os, json
from pathlib import Path
from crewai.tools import tool

CACHE = Path("backend/.cache/players")
CACHE.mkdir(parents=True, exist_ok=True)
HEADERS = {"x-apisports-key": os.getenv("API_SPORTS_KEY")}


@tool("search_player")
def search_player(player_name: str) -> str:
    """Resolves a player's name to their API ID and basic profile.
    Always call this first before transfer_market or comparison tools."""

    cache_file = CACHE / f"id_{player_name.lower().replace(' ', '_')}.json"
    if cache_file.exists():
        return cache_file.read_text()

    resp = requests.get(
        "https://v3.football.api-sports.io/players",
        headers=HEADERS,
        params={"search": player_name, "season": 2024}
    )
    players = resp.json().get("response", [])

    # Extract just what the agent needs — don't return the full blob
    results = [
        {
            "id": p["player"]["id"],
            "name": p["player"]["name"],
            "fullname": f"{p['player']['firstname']} {p['player']['lastname']}",
            "nationality": p["player"]["nationality"],
            "age": p["player"]["age"],
            "current_team": p["statistics"][0]["team"]["name"] if p.get("statistics") else None
        }
        for p in players
    ]

    output = json.dumps(results)
    cache_file.write_text(output)
    return output