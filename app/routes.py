# app/routes.py
from __future__ import annotations
from flask import Blueprint, current_app, jsonify, render_template, request
from rapidfuzz import process, fuzz
from .services.espn import (
    player_index_by_name,
    dropdown_teams,
    fetch_league_blob,
)  # <-- added fetch_league_blob
from .keeper import check_final_roster, keeper_verdict, TEAMS, can_add_to_keepers, calculate_keeper_cost, KeeperSelection
import email
from email import parser

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    # Build dropdown from ESPN live names; fallback to static if ESPN hiccups
    try:
        teams = dropdown_teams(current_app.config)
        if not teams:
            teams = TEAMS
    except Exception:
        teams = TEAMS
    return render_template(
        "index.html", 
        teams=teams, 
        last_season=current_app.config["LAST_SEASON"],
        commissioner_email=current_app.config.get("COMMISSIONER_EMAIL", "")
    )


@bp.get("/api/team_roster")
def api_team_roster():
    """
    Returns final EOY roster for a given internal team key.
    Response: { team_key, final_scoring_period, players: [{id,name,draft_round,undrafted}] }
    """
    team_key = (request.args.get("team") or "").strip()
    if not team_key:
        return jsonify({"error": "Missing ?team=<team_key>"}), 400

    try:
        blob = fetch_league_blob(current_app.config)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch ESPN data: {e}"}), 500

    # Build draft round lookup
    picks = (blob.get("draft", {}) or {}).get("draftDetail", {}).get("picks", []) or []
    draft_round_by_player = {}
    for p in picks:
        pid, rnd = p.get("playerId"), p.get("roundId")  # Use roundId instead of round
        if isinstance(pid, int) and isinstance(rnd, int):
            draft_round_by_player[pid] = rnd

    # Map ESPN team id -> our internal key
    from .config.team_map import TEAM_ID_MAP

    final_sp = blob.get("final_scoring_period")
    out = []
    for t in (blob.get("roster") or {}).get("teams", []) or []:
        espn_tid = t.get("id")
        mapped = TEAM_ID_MAP.get(espn_tid)
        if mapped != team_key:
            continue
        for e in (t.get("roster") or {}).get("entries", []) or []:
            p = (e.get("playerPoolEntry") or {}).get("player") or {}
            pid, full = p.get("id"), p.get("fullName")
            if not isinstance(pid, int) or not full:
                continue
            rd = draft_round_by_player.get(pid)
            out.append(
                {
                    "id": pid,
                    "name": full,
                    "draft_round": rd,
                    "undrafted": rd is None,
                }
            )

    return jsonify(
        {
            "team_key": team_key,
            "final_scoring_period": final_sp,
            "players": sorted(
                out, key=lambda x: (x["undrafted"], x["draft_round"] or 99, x["name"])
            ),
        }
    )


@bp.post("/api/check")
def api_check():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip().lower()
    team_key = (data.get("team_id") or "").strip()

    if not name or not team_key:
        return jsonify({"error": "Missing player name or team selection."}), 400

    try:
        idx = player_index_by_name(current_app.config)
    except Exception as e:
        return jsonify({"error": f"Failed to load ESPN data: {e}"}), 500

    rec = idx.get(name)
    if not rec:
        choices = list(idx.keys())
        suggestions = process.extract(name, choices, scorer=fuzz.WRatio, limit=3)
        hint = ", ".join([c[0] for c in suggestions if c[1] >= 75]) or "no close match"
        return jsonify(
            {
                "final_on_roster": False,
                "final_message": f"Player not found on any final roster for {current_app.config['LAST_SEASON']}. Suggestions: {hint}.",
                "keeper_eligible": False,
                "keeper_message": "No eligibility check performed because player was not found.",
                "keeper_bucket": None,
            }
        )

    final_ok, final_msg = check_final_roster(rec, team_key)
    if not final_ok:
        return jsonify(
            {
                "final_on_roster": False,
                "final_message": final_msg,
                "keeper_eligible": False,
                "keeper_message": "Ineligible because the player was not on your final roster last season.",
                "keeper_bucket": None,
                "draft_round": rec.draft_round,
                "undrafted": rec.originally_undrafted,
            }
        )

    elig, msg, bucket = keeper_verdict(rec)
    return jsonify(
        {
            "final_on_roster": True,
            "final_message": "Player was on your final roster last season.",
            "keeper_eligible": bool(elig),
            "keeper_message": msg,
            "keeper_bucket": bucket,
            "draft_round": rec.draft_round,
            "undrafted": rec.originally_undrafted,
        }
    )


@bp.post("/api/check_keeper_selection")
def api_check_keeper_selection():
    """
    Check if a player can be added to keeper selection based on current limits.
    """
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip().lower()
    team_key = (data.get("team_id") or "").strip()
    current_keepers = data.get("current_keepers", [])

    if not name or not team_key:
        return jsonify({"error": "Missing player name or team selection."}), 400

    try:
        idx = player_index_by_name(current_app.config)
    except Exception as e:
        return jsonify({"error": f"Failed to load ESPN data: {e}"}), 500

    rec = idx.get(name)
    if not rec:
        return jsonify({"error": "Player not found."}), 404

    # Create KeeperSelection object from current keepers
    selection = KeeperSelection(team_key=team_key, keepers=current_keepers)
    
    # Check if can be added
    can_add, message, bucket = can_add_to_keepers(rec, selection)
    
    if can_add:
        cost_round = calculate_keeper_cost(rec, selection)
        return jsonify({
            "can_add": True,
            "message": message,
            "bucket": bucket,
            "cost_round": cost_round,
            "player_info": {
                "id": rec.player_id,
                "name": rec.name,
                "draft_round": rec.draft_round,
                "undrafted": rec.originally_undrafted
            }
        })
    else:
        return jsonify({
            "can_add": False,
            "message": message,
            "bucket": None
        })


@bp.get("/api/keeper_limits")
def api_keeper_limits():
    """
    Get current keeper selection limits and rules.
    """
    return jsonify({
        "max_keepers": 3,
        "limits": {
            "1-10": 1,
            "11-16": 1,
            "waiver": 1
        },
        "rules": [
            "Maximum 3 keepers total",
            "1 keeper from rounds 1-10",
            "1 keeper from rounds 11-16", 
            "1 waiver wire keeper (undrafted players)",
            "Players kept last year cannot be kept again"
        ]
    })
