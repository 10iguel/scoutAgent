import requests, os, json
from pathlib import Path
from crewai.tools import tool

CACHE = Path("backend/.cache/standings")
CACHE.mkdir(parents=True, exist_ok=True)
HEADERS = {"x-apisports-key": os.getenv("API_SPORTS_KEY")}

LEAGUE_IDS = {
    "la liga": 140, "premier league": 39,
    "serie a": 135, "bundesliga": 78,
    "ligue 1": 61, "mls": 253
}


@tool("standings")
def standings(league_name: str, season: int = 2024) -> str:
    """Fetches current league table standings. 
    league_name can be: 'la liga', 'premier league', 'serie a', 
    'bundesliga', 'ligue 1', 'mls'."""

    league_id = LEAGUE_IDS.get(league_name.lower())
    if not league_id:
        return json.dumps({"error": f"Unknown league: {league_name}. Choose from: {list(LEAGUE_IDS.keys())}"})

    cache_file = CACHE / f"{league_id}_{season}.json"
    if cache_file.exists():
        return cache_file.read_text()

    resp = requests.get(
        "https://v3.football.api-sports.io/standings",
        headers=HEADERS,
        params={"league": league_id, "season": season}
    )
    table = resp.json()["response"][0]["league"]["standings"][0]

    slim = [{"rank": t["rank"], "team": t["team"]["name"],
             "points": t["points"], "form": t["form"],
             "gd": t["goalsDiff"]} for t in table[:10]]  # top 10 only

    output = json.dumps(slim)
    cache_file.write_text(output)
    return output