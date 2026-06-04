import math
from dataclasses import dataclass
from typing import Dict, List

from data import ATTRIBUTE_BASES, BASE_SCORES, STAR_PLAYERS


@dataclass
class PlayerProfile:
    attack: int
    midfield: int
    defense: int
    overall: int


def name_hash(text: str) -> int:
    h = 0
    for ch in text:
        h = (h * 31 + ord(ch)) % 100000
    return h


def player_profile(player: Dict[str, str], team_id: str) -> PlayerProfile:
    base = BASE_SCORES.get(player["position"], 72)
    anchors = ATTRIBUTE_BASES.get(player["position"], {"attack": 60, "midfield": 60, "defense": 60})
    h = name_hash(f"{team_id}:{player['name']}")

    variance = ((h % 13) - 6) * 2
    star_boost = 6 if any(token.lower() in player["name"].lower() for token in STAR_PLAYERS) else 0
    team_boost = ((h % 7) - 3) * 1.5

    attack = max(20, min(99, anchors["attack"] + variance + star_boost + team_boost))
    midfield = max(20, min(99, anchors["midfield"] + variance * 0.8 + star_boost * 0.6 + team_boost))
    defense = max(20, min(99, anchors["defense"] + variance * 0.6 + star_boost * 0.35 + team_boost))
    overall = max(20, min(99, base + variance + star_boost + team_boost))

    return PlayerProfile(
        attack=round(attack),
        midfield=round(midfield),
        defense=round(defense),
        overall=round(overall),
    )


def calculate_results(picks: List[Dict]) -> Dict:
    attack_pool = [p for p in picks if p["position"] in {"RW", "LW", "ST", "CF", "SS", "CAM"}]
    midfield_pool = [p for p in picks if p["position"] in {"CM", "CDM", "CAM"}]
    defense_pool = [p for p in picks if p["position"] in {"GK", "RB", "CB", "LB", "CDM"}]

    attack_ratings = [p["profile"].attack for p in attack_pool]
    midfield_ratings = [p["profile"].midfield for p in midfield_pool]
    defense_ratings = [p["profile"].defense for p in defense_pool]
    all_ratings = [p["profile"].overall for p in picks]

    attack = sum(attack_ratings) / len(attack_ratings) if attack_ratings else 0
    midfield = sum(midfield_ratings) / len(midfield_ratings) if midfield_ratings else 0
    defense = sum(defense_ratings) / len(defense_ratings) if defense_ratings else 0

    avg = sum(all_ratings) / len(all_ratings)
    spread = math.sqrt(sum((x - avg) ** 2 for x in all_ratings) / len(all_ratings))
    chemistry = max(45, min(99, 100 - spread))

    overall = attack * 0.38 + midfield * 0.27 + defense * 0.25 + chemistry * 0.10

    return {
        "attack": round(attack),
        "midfield": round(midfield),
        "defense": round(defense),
        "chemistry": round(chemistry),
        "overall": round(overall, 1),
        "avg_rating": avg,
    }


def score_tier(score: float) -> str:
    if score >= 95:
        return "GOAT TIER"
    if score >= 90:
        return "LEGENDARY"
    if score >= 85:
        return "ELITE"
    if score >= 80:
        return "WORLD CLASS"
    if score >= 75:
        return "VERY GOOD"
    return "MID TABLE FC"


def compute_achievements(stats: Dict, picks: List[Dict]) -> List[str]:
    achievements = []

    if stats["overall"] >= 95:
        achievements.append("Invincible Potential")
    if stats["attack"] >= 90:
        achievements.append("Firepower")
    if stats["midfield"] >= 90:
        achievements.append("Midfield Kings")
    if stats["defense"] >= 90:
        achievements.append("Iron Wall")
    if stats["chemistry"] >= 92:
        achievements.append("Well Drilled")
    if sum(1 for p in picks if p["profile"].overall >= 92) >= 3:
        achievements.append("Galacticos")

    return achievements


def build_insights(picks: List[Dict], stats: Dict) -> Dict:
    metric_rows = [
        {"key": "attack", "label": "Attack", "value": stats["attack"]},
        {"key": "midfield", "label": "Midfield", "value": stats["midfield"]},
        {"key": "defense", "label": "Defense", "value": stats["defense"]},
        {"key": "chemistry", "label": "Chemistry", "value": stats["chemistry"]},
    ]

    strongest = max(metric_rows, key=lambda x: x["value"])
    weakest = min(metric_rows, key=lambda x: x["value"])
    draft_mvp = max(picks, key=lambda p: p["profile"].overall)
    achievements = compute_achievements(stats, picks)

    return {
        "strongest": strongest,
        "weakest": weakest,
        "draft_mvp": draft_mvp,
        "achievements": achievements,
    }