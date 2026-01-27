# eoghan_rua_team_selector/views/preview.py
from pathlib import Path
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from eoghan_rua_team_selector.export_excel import build_excel_bytes_with_cover

def _teams_view(teams):
    cols = []
    for t in teams:
        header = toga.Label(
            f"{t['name']}  (Score {t['score']} • 1s:{t['counts'][1]} 2s:{t['counts'][2]} 3s:{t['counts'][3]})",
            style=Pack(font_weight="bold", padding_bottom=4)
        )
        rows = [toga.Label(f"• {nm}  (skill {sk})") for nm, sk in t["players"]]
        col = toga.Box(children=[header, *rows], style=Pack(direction=COLUMN, padding_right=16, padding_bottom=12))
        cols.append(col)
    return toga.Box(children=cols, style=Pack(direction=ROW, padding=(0, 0, 12, 0)))

def Preview(app: toga.App, teams, crest_bytes: bytes):
    title = toga.Label("Preview Teams", style=Pack(font_size=18, font_weight="bold", padding_bottom=8))

    message = toga.Label("", style=Pack(color="#1a7f37", padding_top=6))

    def on_export(_):
        try:
            xlsx = build_excel_bytes_with_cover(teams, crest_bytes)
            out_path = Path(app.paths.data) / "team_sheets.xlsx"
            out_path.write_bytes(xlsx)
            message.text = f"Saved: {out_path}"
        except Exception as exc:
            message.text = f"Export error: {exc}"
            message.style.update(color="red")

    export_btn = toga.Button("Export Excel", on_press=on_export, style=Pack(padding_right=8))
    back_btn = toga.Button("Back", on_press=lambda w: app.goto_builder())

    actions = toga.Box(children=[export_btn, back_btn], style=Pack(direction=ROW, padding_top=8))

    box = toga.Box(
        children=[title, _teams_view(teams), actions, message],
        style=Pack(direction=COLUMN, padding=20)
    )
    return box
``
