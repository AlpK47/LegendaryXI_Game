import random
from typing import Dict, List

from data import ROLE_ALIASES, SLOT_DEFS, TEAM_PLAYERS, TEAMS


def display_slot(slot_id: str) -> str:
    for slot in SLOT_DEFS:
        if slot["id"] == slot_id:
            return slot["label"]
    return slot_id


def slot_matches(position: str, slot_group: str) -> bool:
    return position in ROLE_ALIASES.get(slot_group, [slot_group])


def get_open_slot_ids_for_player(position: str, filled_slots: List[str]) -> List[str]:
    open_ids = []
    for slot in SLOT_DEFS:
        if slot["id"] in filled_slots:
            continue
        if slot_matches(position, slot["group"]):
            open_ids.append(slot["id"])
    return open_ids


def get_assignable_slot_index(position: str, filled_slots: List[str]) -> int:
    open_ids = get_open_slot_ids_for_player(position, filled_slots)
    if not open_ids:
        return -1

    first_open_id = open_ids[0]
    for idx, slot in enumerate(SLOT_DEFS):
        if slot["id"] == first_open_id:
            return idx
    return -1


def has_open_slot_for_player(position: str, filled_slots: List[str]) -> bool:
    return len(get_open_slot_ids_for_player(position, filled_slots)) > 0


def available_teams(picked: List[Dict]) -> List[Dict]:
    filled_slots = [p["slot_id"] for p in picked]
    used_names = [p["name"] for p in picked]

    valid_teams = []
    for team in TEAMS:
        roster = TEAM_PLAYERS.get(team["id"], [])
        if any(
            (player["name"] not in used_names)
            and has_open_slot_for_player(player["position"], filled_slots)
            for player in roster
        ):
            valid_teams.append(team)

    return valid_teams


def roll_random_team(picked: List[Dict]) -> Dict | None:
    teams = available_teams(picked)
    if not teams:
        return None
    return random.choice(teams)