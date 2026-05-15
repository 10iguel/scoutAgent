import requests, os, json
from pathlib import Path
from crewai.tools import tool

CACHE = Path("backend/.cache/comparison")
CACHE.mkdir(parents=True, exist_ok=True)
HEADERS = {"x-apisports-key": os.getenv("API_SPORTS_KEY")}


@tool("comparison")
def comparison(player_id: int, season: int) -> str:
    """Fetches a player's stats for a specific historical season for comparison.
    Use this to compare a player's past performance against another player.
    Requires a numeric player ID — use search_player tool first."""

    cache_file = CACHE / f"{player_id}_{season}.json"
    if cache_file.exists():
        return cache_file.read_text()

    resp = requests.get(
        "https://v3.football.api-sports.io/players",
        headers=HEADERS,
        params={"id": player_id, "season": season}
    )
    data = resp.json().get("response", [{}])[0]
    stats = data.get("statistics", [])

    # Aggregate across all competitions that season
    totals = {
        "goals": sum(s["goals"]["total"] or 0 for s in stats),
        "assists": sum(s["goals"]["assists"] or 0 for s in stats),
        "appearances": sum(s["games"]["appearences"] or 0 for s in stats),
        "dribbles_success": sum(s["dribbles"]["success"] or 0 for s in stats),
        "avg_rating": round(
            sum(float(s["games"]["rating"]) for s in stats if s["games"]["rating"])
            / max(len([s for s in stats if s["games"]["rating"]]), 1), 2
        ),
        "competitions": [s["league"]["name"] for s in stats]
    }

    output = json.dumps({"player": data.get("player", {}).get("name"), "season": season, **totals})
    cache_file.write_text(output)
    return output