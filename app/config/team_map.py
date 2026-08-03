# app/config/team_map.py

TEAM_ID_MAP = {
    1: "seahawks",  # Arizona Cardinals (Dan Costa)
    2: "numbnuts",  # Numbnutsss (Greg Costa)
    3: "stamford",  # Stamford Mackie (Scott Mackie)
    4: "cmb3dan",  # CMB 3-Dan (Dan S)
    5: "devonta",  # Chasing Joe (Joe Costa)  [was DeVonta Hurts You]
    6: "bumcrumbs",  # Bum Crumbs (Phat Johnson)
    7: "mitchell",  # Team Mitchell (Timothy Mitchell)
    8: "metzler",  # The Arm of the Armadillos (Andrew Flaherty) [was Paul Metzler...]
    9: "kenney",  # Team Kenney (Brian Kenney)
    10: "mahoms",  # Justin Time (Connor Flaherty) [was Me And My Mahomies]
}

# Players who were kept in 2025 and cannot be kept again in 2026
# (they've already been kept for 1 season, max is 2 seasons total)
SEASONS_KEPT_OVERRIDES = {
    4430807: 1,  # Bijan Robinson (rd 1)
    4362628: 1,  # Ja'Marr Chase (rd 1)
    4595348: 1,  # Malik Nabers (rd 4)
    4362238: 1,  # Chase Brown (rd 8)
    4683062: 1,  # Xavier Worthy (rd 8)
    4432773: 1,  # Brian Thomas Jr. (rd 10)
    4612826: 1,  # Ladd McConkey (rd 10)
    4596448: 1,  # Bucky Irving (rd 11)
    4426348: 1,  # Jayden Daniels (rd 11)
    4426388: 1,  # Jameson Williams (rd 11)
    4426385: 1,  # Zach Charbonnet (rd 11)
    4036133: 1,  # T.J. Hockenson (rd 12)
    4038941: 1,  # Justin Herbert (rd 13)
    4373678: 1,  # Khalil Shakir (rd 13)
    4032473: 1,  # Rashid Shaheed (rd 17)
}
