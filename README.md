
# Low Expectations League – Keeper Eligibility Checker (Clean Build)

This build includes fixes for earlier issues:
- robust ESPN headers to avoid 403/HTML,
- no lru_cache on Flask Config,
- modular structure,
- helper script to list ESPN team IDs.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in LEAGUE_ID, ESPN_SWID, ESPN_S2 (fresh!), LAST_SEASON
```

## Map ESPN Team IDs
Run:
```bash
python list_teams.py
```
Then edit `app/config/team_map.py`:
```python
TEAM_ID_MAP = {
  1: "seahawks",
  2: "mahoms",
  # ...
}
```

Internal keys you can use: `seahawks, mahoms, devonta, cmb3dan, bumcrumbs, stamford, metzler, numbnuts, kenney, mitchell`.

## Run
```bash
gunicorn wsgi:app --bind 127.0.0.1:5000 --workers 1 --threads 4 --timeout 60
```

If you get 403 in `list_teams.py`, refresh your ESPN_S2 from the browser.
