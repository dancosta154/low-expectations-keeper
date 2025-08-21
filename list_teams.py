from app.services.espn import fetch_league_blob
from app import create_app

app = create_app()
with app.app_context():
    blob = fetch_league_blob(app.config)

    # team metadata lives under teams_meta["teams"]
    tlist = []
    for t in blob["teams_meta"].get("teams", []):
        tid = t.get("id")
        # Try location/nickname first; fall back to name/abbrev
        loc = t.get("location") or ""
        nick = t.get("nickname") or ""
        name = t.get("name") or (loc + " " + nick).strip()
        abbrev = t.get("abbrev") or ""
        owners = t.get("owners") or []
        tlist.append((tid, loc or None, nick or None, name, abbrev, owners))

    print(tlist)
