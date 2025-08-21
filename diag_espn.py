# diag_espn.py
import os, re, requests, textwrap
import email
from email import parser

L = os.getenv("LEAGUE_ID")
SWID = os.getenv("ESPN_SWID") or ""
S2 = os.getenv("ESPN_S2") or ""


def show(name, val):
    print(f"{name}: {repr(val)}")
    print(
        f"  len={len(val)}  startswith-space={val[:1]==' '}  endswith-space={val[-1:]==' '}"
    )
    print(
        f"  printable? {val.isprintable()}  trailing-bytes={[ord(c) for c in val[-3:]]}"
    )
    print()


print("=== ENV CHECK ===")
show("LEAGUE_ID", L or "")
show("ESPN_SWID", SWID)
show("ESPN_S2", S2)

print("=== SHAPE CHECK ===")
swid_ok = bool(re.fullmatch(r"\{[0-9A-Fa-f-]{36}\}", SWID))
s2_ok = len(S2) > 60 and "%" in S2  # usually URL-encoded and long
print("SWID shape OK?", swid_ok)
print("S2 length/encoded OK?", s2_ok)
print()

print("=== REQUEST TESTS (no redirects) ===")
url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leagues/{L}"
common_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": f"https://fantasy.espn.com/football/league?leagueId={L}",
    "Origin": "https://fantasy.espn.com",
    "x-fantasy-platform": "kona",
    "x-fantasy-source": "kona",
}

variants = [
    ("SWID+espn_s2", {"SWID": SWID, "espn_s2": S2}),
    ("swid+espn_s2", {"swid": SWID, "espn_s2": S2}),
    ("SWID+ESPN_S2", {"SWID": SWID, "ESPN_S2": S2}),
    ("Cookie header (manual)", None),
]

for name, ck in variants:
    print(f"\n--- Variant: {name} ---")
    if ck is None:
        headers = {**common_headers, "Cookie": f"SWID={SWID}; espn_s2={S2}"}
        r = requests.get(url, headers=headers, timeout=25, allow_redirects=False)
    else:
        r = requests.get(
            url, headers=common_headers, cookies=ck, timeout=25, allow_redirects=False
        )

    print("status:", r.status_code)
    print("ct:", r.headers.get("Content-Type"))
    print("location:", r.headers.get("Location"))
    body = r.text or ""
    print("body-start:", repr(body[:200]))
