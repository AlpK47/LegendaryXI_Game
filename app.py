import streamlit as st

from data import SLOT_DEFS, TEAM_PLAYERS, TEAMS
from logic import (
    available_teams,
    display_slot,
    get_assignable_slot_index,
    has_open_slot_for_player,
    roll_random_team,
)
from scoring import build_insights, calculate_results, player_profile, score_tier

st.set_page_config(page_title="Football Draft MVP", page_icon="⚽", layout="wide")


def start_state():
    if "picked" not in st.session_state:
        st.session_state.picked = []
    if "rolled_team_id" not in st.session_state:
        st.session_state.rolled_team_id = None
    if "status" not in st.session_state:
        st.session_state.status = "Click Roll Team to begin."
    if "results" not in st.session_state:
        st.session_state.results = None


def reset_game():
    st.session_state.picked = []
    st.session_state.rolled_team_id = None
    st.session_state.status = "Click Roll Team to begin."
    st.session_state.results = None


def roll_team():
    team = roll_random_team(st.session_state.picked)
    if team is None:
        st.session_state.status = "No teams left with any usable players. Reset and try again."
        st.session_state.rolled_team_id = None
        return

    st.session_state.rolled_team_id = team["id"]
    st.session_state.status = f"Rolled {team['name']} ({team['era']}). Pick any player from that roster."


def pick_player(player: dict):
    team_id = st.session_state.rolled_team_id
    if not team_id:
        return

    picked = st.session_state.picked
    used_names = [p["name"] for p in picked]
    filled_slots = [p["slot_id"] for p in picked]

    if player["name"] in used_names:
        st.session_state.status = "That player has already been picked."
        return

    if not has_open_slot_for_player(player["position"], filled_slots):
        st.session_state.status = f"You already filled every {player['position']} / compatible slot."
        return

    slot_index = get_assignable_slot_index(player["position"], filled_slots)
    if slot_index == -1:
        st.session_state.status = f"No open slot fits {player['name']}."
        return

    profile = player_profile(player, team_id)
    next_picks = picked + [
        {
            **player,
            "team_id": team_id,
            "slot_id": SLOT_DEFS[slot_index]["id"],
            "profile": profile,
        }
    ]

    st.session_state.picked = next_picks
    st.session_state.rolled_team_id = None
    st.session_state.status = "Click Roll Team for the next pick." if len(next_picks) < len(SLOT_DEFS) else "Team complete."

    if len(next_picks) == len(SLOT_DEFS):
        stats = calculate_results(next_picks)
        insights = build_insights(next_picks, stats)
        st.session_state.results = {"stats": stats, **insights}


start_state()

st.markdown(
    """
    <style>
        .block-container { padding-top: 1.5rem; }
        .stButton > button { border-radius: 14px; padding: 0.75rem 1.1rem; font-weight: 700; }
        .metric-card { background: #0f172a; padding: 1rem; border-radius: 16px; border: 1px solid #1f2937; }
        .pill { display: inline-block; padding: 0.35rem 0.75rem; border-radius: 999px; border: 1px solid #334155; margin: 0.2rem 0.25rem 0 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Football Draft MVP")
st.caption("Roll a team, then pick any player from that roster. A player can only be selected if an open compatible slot still exists.")

col_left, col_right = st.columns([0.30, 0.70], gap="large")

with col_left:
    st.markdown("### Controls")
    st.write(st.session_state.status)

    if st.button("Roll Team", use_container_width=True, disabled=len(st.session_state.picked) >= len(SLOT_DEFS)):
        roll_team()
        st.rerun()

    if st.button("Reset", use_container_width=True):
        reset_game()
        st.rerun()

    st.markdown("### Progress")
    picked_count = len(st.session_state.picked)
    st.write(f"**{picked_count} / {len(SLOT_DEFS)} picks**")
    st.progress(picked_count / len(SLOT_DEFS))
    st.write(f"**Open slots:** {len(SLOT_DEFS) - picked_count}")

    st.markdown("### Locked lineup")
    picks_by_slot = {p["slot_id"]: p for p in st.session_state.picked}
    for slot in SLOT_DEFS:
        player_name = picks_by_slot.get(slot["id"], {}).get("name", "—")
        st.markdown(f"**{slot['label']}**: {player_name}")

with col_right:
    current_team = next((t for t in TEAMS if t["id"] == st.session_state.rolled_team_id), None)

    if not st.session_state.results:
        st.markdown("### Current round")
        if current_team:
            st.subheader(f"Rolled: {current_team['name']}")
            st.write(f"{current_team['era']} • {current_team['league']}")
            st.write("Full roster is shown below. Green buttons are currently usable.")

            roster = TEAM_PLAYERS.get(current_team["id"], [])
            filled_slots = [p["slot_id"] for p in st.session_state.picked]
            used_names = [p["name"] for p in st.session_state.picked]

            cols = st.columns(3)
            for i, player in enumerate(roster):
                is_used = player["name"] in used_names
                eligible = (not is_used) and has_open_slot_for_player(player["position"], filled_slots)
                slot_index = get_assignable_slot_index(player["position"], filled_slots)
                slot_label = "No open slot" if slot_index == -1 else SLOT_DEFS[slot_index]["label"]

                with cols[i % 3]:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    st.markdown(f"**{player['name']}**")
                    st.caption(f"{player['position']} • {('Already picked' if is_used else slot_label)}")
                    if st.button("Pick", key=f"pick_{current_team['id']}_{player['name']}", disabled=not eligible, use_container_width=True):
                        pick_player(player)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Click **Roll Team** to reveal the club for this pick.")
    else:
        stats = st.session_state.results["stats"]
        insights = st.session_state.results

        st.markdown("### Final result")
        st.markdown(
            f"""
            <div class='metric-card'>
                <h1 style='margin:0;'>Draft complete</h1>
                <h2 style='color:#10b981; margin:0.5rem 0 0;'>Greatness score: {stats['overall']}</h2>
                <p style='margin:0.25rem 0 0; font-weight:700;'>{score_tier(stats['overall'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        a1, a2, a3, a4 = st.columns(4)
        with a1:
            st.metric("Attack", stats["attack"])
        with a2:
            st.metric("Midfield", stats["midfield"])
        with a3:
            st.metric("Defense", stats["defense"])
        with a4:
            st.metric("Chemistry", stats["chemistry"])

        b1, b2 = st.columns(2)
        with b1:
            st.markdown("### Biggest strength")
            st.write(f"**{insights['strongest']['label']}** — {insights['strongest']['value']}/100")
            st.markdown("### Draft MVP")
            mvp = insights["draft_mvp"]
            st.write(f"**{mvp['name']}**")
            st.caption(f"{mvp['position']} • Rating {mvp['profile'].overall}")
        with b2:
            st.markdown("### Biggest weakness")
            st.write(f"**{insights['weakest']['label']}** — {insights['weakest']['value']}/100")

        st.markdown("### Achievements")
        if insights["achievements"]:
            for achievement in insights["achievements"]:
                st.markdown(f"<span class='pill'>{achievement}</span>", unsafe_allow_html=True)
        else:
            st.write("No achievements this run.")

        st.markdown("### Your XI")
        picks_by_slot = {p["slot_id"]: p for p in st.session_state.picked}
        for slot in SLOT_DEFS:
            st.write(f"**{slot['label']}**: {picks_by_slot.get(slot['id'], {}).get('name', '—')}")

        st.markdown("### Stat breakdown")
        st.write(f"Attack: {stats['attack']}")
        st.write(f"Midfield: {stats['midfield']}")
        st.write(f"Defense: {stats['defense']}")
        st.write(f"Chemistry: {stats['chemistry']}")

        if st.button("Play again"):
            reset_game()
            st.rerun()

st.markdown("---")
st.caption("This is a single-file Streamlit version you can open in PyCharm and run locally.")