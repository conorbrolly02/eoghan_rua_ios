# eoghan_rua_team_selector/views/home.py
import toga
from toga.style import Pack
from toga.style.pack import COLUMN

def Home(app: toga.App):
    title = toga.Label(
        "Home",
        style=Pack(font_size=18, font_weight="bold", padding_bottom=8)
    )
    info = toga.Label(
        "Create balanced teams by entering players and skills (1 strongest – 3 developing).",
        style=Pack(padding_bottom=12)
    )
    to_builder = toga.Button(
        "Build Teams",
        on_press=lambda w: app.goto_builder(),
        style=Pack(padding=(8, 0), width=200)
    )

    box = toga.Box(
        children=[title, info, to_builder],
        style=Pack(direction=COLUMN, padding=20)
    )
    return box
