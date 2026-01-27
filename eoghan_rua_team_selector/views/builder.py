# eoghan_rua_team_selector/views/builder.py
from pathlib import Path
import io
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from eoghan_rua_team_selector.team_logic import pick_teams
from eoghan_rua_team_selector.app import resource_path


def _parse_players(raw: str):
    """
    Accepts lines of either:
      - "Name,Skill"
      - "Name:Skill"
    Returns list[(name, int(skill))] ignoring blank lines.
    """
    players = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if "," in line:
            name, skill = line.split(",", 1)
        elif ":" in line:
            name, skill = line.split(":", 1)
        else:
            # default skill=2 if not provided
            name, skill = line, "2"
        name = name.strip()
        try:
            skill = int(skill.strip())
        except ValueError:
            skill = 2
        players.append((name, max(1, min(3, skill))))
    return players


def Builder(app: toga.App):
    title = toga.Label(
        "Build Teams",
        style=Pack(font_size=18, font_weight="bold", padding_bottom=8)
    )

    sample = "Alice,1\nBob,2\nCara,2\nDeclan,3\nEoin,1\nFiona,2\nGavin,3\n"
    players_input = toga.MultilineTextInput(
        value=sample,
        placeholder="Enter one player per line as 'Name,Skill' (Skill: 1 strongest – 3 developing)",
        style=Pack(height=160, padding_bottom=8),
    )

    team_count = toga.NumberInput(min_value=2, max_value=10, step=1, value=2,
                                  style=Pack(width=120, padding_bottom=8))

    status = toga.Label("", style=Pack(color="#555", padding_top=4))

    def on_build(_):
        try:
            players = _parse_players(players_input.value or "")
            n = int(team_count.value or 2)
            teams = pick_teams(players, n, seed=42)
            crest_bytes = (resource_path(app, "crest.png").read_bytes()
                           if resource_path(app, "crest.png").exists() else b"")
            app.goto_preview(teams, crest_bytes)
        except Exception as exc:
            status.text = f"Error: {exc}"

    controls = toga.Box(
        children=[
            toga.Label("Teams:", style=Pack(padding_right=8)),
            team_count,
            toga.Button("Create", on_press=on_build, style=Pack(padding_left=12)),
        ],
        style=Pack(direction=ROW, padding_bottom=8)
    )

    box = toga.Box(
        children=[title, players_input, controls, status],
        style=Pack(direction=COLUMN, padding=20)
    )
    return box
