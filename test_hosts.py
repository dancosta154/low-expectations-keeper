import os, requests
import email
from email import parser

L = os.getenv("LEAGUE_ID")
S2 = os.getenv("ESPN_S2")
SWID = os.getenv("ESPN_SWID")

hosts = [
    "https://lm-api-reads.fantasy.espn.com",
    "https://fantasy.espn.com",
]
path = f"/apis/v3/games/ffl/seasons/2024/segments/0/leagues/{L}"
hdrs = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": f"https://fantasy.espn.com/football/league?leagueId={L}",
    "Origin": "https://fantasy.espn.com",
    "x-fantasy-platform": "kona",
    "x-fantasy-source": "kona",
}
cks = {"SWID": SWID, "espn_s2": S2}

for h in hosts:
    url = h + path + "?view=mSettings"
    r = requests.get(url, headers=hdrs, cookies=cks, timeout=25, allow_redirects=False)
    print("\nHost:", h)
    print("status:", r.status_code)
    print("ct:", r.headers.get("Content-Type"))
    print("location:", r.headers.get("Location"))
    print("body:", (r.text or "")[:160].replace("\n", " "))
