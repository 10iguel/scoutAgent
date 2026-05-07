import requests, os, json
from pathlib import Path
from crewai.tools import tool

CACHE = Path("backend/.cache/players")
CACHE.mkdir(parents=True, exist_ok=True)

HEADERS = {"x-apisports-key": os.getenv("API_SPORTS_KEY")}


@tool("player_stats")
def player_stats(player_name: str) -> str:
    """Fetches current season stats and ratings for a soccer player by name."""
    cache_file = CACHE / f"{player_name.lower().replace(' ', '_')}.json"

    if cache_file.exists():
        return cache_file.read_text()

    resp = requests.get(
        "https://v3.football.api-sports.io/players",
        headers=HEADERS,
        params={"search": player_name, "season": 2024}
    )
    data = resp.json()
    cache_file.write_text(json.dumps(data))
    return json.dumps(data)