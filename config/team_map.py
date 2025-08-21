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

# Players who were kept in 2023 and cannot be kept again in 2024
# (they've already been kept for 1 season, max is 2 seasons total)
SEASONS_KEPT_OVERRIDES = {
    2976212: 1,  # Stefon Diggs
    3918298: 1,  # Josh Allen
    3116406: 1,  # Tyreek Hill
    4241389: 1,  # CeeDee Lamb
    4429795: 1,  # Jahmyr Gibbs
    4569618: 1,  # Garrett Wilson
    4239996: 1,  # Travis Etienne Jr.
    3054850: 1,  # Alvin Kamara
    4427366: 1,  # Breece Hall
    3045147: 1,  # James Conner
    4430737: 1,  # Kyren Williams
    4036378: 1,  # Jordan Love
    4426515: 1,  # Puka Nacua
    4430027: 1,  # Sam LaPorta
    4035676: 1,  # Zack Moss (found as "zack moss")
    4430878: 1,  # Jaxon Smith-Njigba
    4258173: 1,  # Nico Collins
    4428557: 1,  # Tyjae Spears
    4429084: 1,  # Anthony Richardson
    4429160: 1,  # De'Von Achane
    4428331: 1,  # Rashee Rice
    4569987: 1,  # Jaylen Warren
}
