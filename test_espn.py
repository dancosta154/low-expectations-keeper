import os, requests
import email
from email import parser

LEAGUE_ID = os.getenv("LEAGUE_ID")
SWID = os.getenv("ESPN_SWID")
S2 = os.getenv("ESPN_S2")

url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leagues/{LEAGUE_ID}"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": f"https://fantasy.espn.com/football/league?leagueId={LEAGUE_ID}",
    "Origin": "https://fantasy.espn.com",
    "x-fantasy-platform": "kona",
}
cookies = {"SWID": SWID, "espn_s2": S2}

r = requests.get(url, headers=headers, cookies=cookies, timeout=25, allow_redirects=False)
print("status:", r.status_code)
print("ct:", r.headers.get("Content-Type"))
print("location:", r.headers.get("Location"))
print("first 200:", (r.text or "")[:200])