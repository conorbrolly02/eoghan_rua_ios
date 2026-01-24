
# eoghan_rua_team_selector/views/splash.py
from pathlib import Path
from rubicon.objc import NSLog
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER

class Splash(toga.MainWindow):
    def __init__(self, app):
        # On iOS, MainWindow is full-screen; size=... is ignored and sometimes confusing.
        super().__init__(title="Eoghan Rua — Team Selector")
        self.app = app

        NSLog("Splash: building view")

        # --- Locate resources safely on iOS ---
        # Briefcase copies your declared resources into <app bundle>/resources/
        resources = Path(app.paths.app) / "resources"

        # UI layout
        box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=20,
                                  width=toga.FLEX, height=toga.FLEX))

        crest_path = resources / "crest.png"
        if crest_path.exists():
            try:
                img = toga.Image(crest_path)
                box.add(toga.ImageView(img, style=Pack(height=180, width=180)))
            except Exception as exc:
                NSLog(f"Splash: failed to load crest.png: {exc}")

        box.add(toga.Label("Eoghan Rua — Team Selector", style=Pack(font_size=20, padding_top=10)))

        box.add(
            toga.Button(
                "Continue",
                on_press=lambda w: self.app.goto_home(),
                style=Pack(padding_top=20, width=200),
            )
        )

        self.content = box
        NSLog("Splash: view ready")
