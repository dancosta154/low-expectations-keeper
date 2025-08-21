
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

# League teams shown in the dropdown
TEAMS = [
    {"id": "mahoms",   "name": "Me And My Mahomies (Connor Flaherty)"},
    {"id": "mitchell", "name": "Team Mitchell (Timothy Mitchell)"},
    {"id": "devonta",  "name": "DeVonta Hurts You (Joe Costa)"},
    {"id": "cmb3dan",  "name": "CMB 3-Dan (Dan S)"},
    {"id": "bumcrumbs","name": "Bum Crumbs (Phat Johnson)"},
    {"id": "stamford", "name": "Stamford Mackie (Scott Mackie)"},
    {"id": "seahawks", "name": "Seattle Seahawks (Dan Costa)"},
    {"id": "metzler",  "name": "The Arm of the Armadillos (Andrew Flaherty)"},
    {"id": "numbnuts", "name": "Numbnutsss (Greg Costa)"},
    {"id": "kenney",   "name": "Team Kenney (Brian Kenney)"},
]
TEAM_INDEX: Dict[str, str] = {t["id"]: t["name"] for t in TEAMS}

class PlayerRec:
    def __init__(self, player_id: int, name: str):
        self.player_id = player_id
        self.name = name
        self.final_team_id: Optional[str] = None  # your league key, e.g. "seahawks"
        self.espn_team_id: Optional[int] = None
        self.draft_round: Optional[int] = None
        self.originally_undrafted: bool = False
        self.seasons_kept: int = 0

@dataclass
class Verdict:
    final_on_roster: bool
    final_message: str
    keeper_eligible: bool
    keeper_message: str
    keeper_bucket: Optional[str]

def check_final_roster(rec: PlayerRec, selected_team_key: str) -> Tuple[bool, str]:
    if rec.final_team_id is None:
        return False, "Final roster team mapping unknown for this league. Please map ESPN team IDs to your team keys in config/team_map.py."
    if rec.final_team_id != selected_team_key:
        return False, "Not on your final roster last season for this team."
    return True, "Player was on your final roster last season."

def keeper_verdict(rec: PlayerRec) -> Tuple[bool, str, Optional[str]]:
    # Rule: players who were kept last year cannot be kept this year
    if rec.seasons_kept >= 1:
        return False, "Ineligible: this player was kept last year and cannot be kept again this year.", None

    # Waiver path (truly undrafted)
    if rec.originally_undrafted:
        return True, (
            "Eligible as a Waiver Wire keeper. Default cost = 9th; becomes 10th if your other keeper uses a 9th."
        ), "waiver"

    # Drafted path
    if rec.draft_round is None:
        return False, "Insufficient data: original draft round unknown.", None
    rd = rec.draft_round
    if 1 <= rd <= 10:
        return True, f"Eligible as a Rounds 1–10 keeper (original round {rd}).", "1-10"
    if 11 <= rd <= 16:
        return True, f"Eligible as a Rounds 11–16 keeper (original round {rd}).", "11-16"
    return False, f"Ineligible: draft round {rd} is outside keeper window (1–16).", None
