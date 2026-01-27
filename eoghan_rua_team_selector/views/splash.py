# eoghan_rua_team_selector/views/splash.py
from pathlib import Path
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER

def Splash(app: toga.App):
    from eoghan_rua_team_selector.app import resource_path

    crest_img_path = resource_path(app, "crest.png")
    img = toga.Image(crest_img_path) if crest_img_path.exists() else None
    image_view = toga.ImageView(image=img, style=Pack(height=160)) if img else toga.Label(
        "crest.png not found in resources", style=Pack(color="red", padding_bottom=8)
    )

    title = toga.Label(
        "Eoghan Rua Team Selector",
        style=Pack(font_size=20, font_weight="bold", padding_top=8)
    )
    subtitle = toga.Label(
        "Build balanced teams offline.",
        style=Pack(color="#555", padding_bottom=16)
    )
    start_btn = toga.Button(
        "Start",
        on_press=lambda w: app.goto_home(),
        style=Pack(padding_top=8, width=200, alignment=CENTER)
    )

    box = toga.Box(
        children=[image_view, title, subtitle, start_btn],
        style=Pack(direction=COLUMN, alignment=CENTER, padding=20)
    )
    return box
