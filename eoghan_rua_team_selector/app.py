# eoghan_rua_team_selector/app.py
import sys
import os
import faulthandler

faulthandler.enable()
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import traceback
from pathlib import Path
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from rubicon.objc import NSLog


def resource_path(app: toga.App, name: str) -> Path:
    """Resolve a file bundled in the iOS app (Briefcase puts them under resources/)."""
    return Path(app.paths.app) / "resources" / name


class EoghanRuaApp(toga.App):
    def startup(self):
        """
        Create the main window and show the first screen.
        If anything goes wrong, log the traceback and present a visible error window
        (this prevents the 'opens then closes' symptom).
        """
        NSLog("EoghanRuaApp.startup() begin")
        try:
            # --- Minimal Splash so we can prove launch works ---
            title = toga.Label(
                "Eoghan Rua Team Selector",
                style=Pack(font_size=18, font_weight="bold", padding_bottom=8),
            )
            subtitle = toga.Label(
                "Launch OK – tap to continue",
                style=Pack(color="#555", padding_bottom=12),
            )
            go = toga.Button("Continue", on_press=lambda w: self.goto_home())

            content = toga.Box(children=[title, subtitle, go], style=Pack(direction=COLUMN, padding=20))

            self.main_window = toga.MainWindow(title=self.formal_name)
            self.main_window.content = content
            self.main_window.show()
            NSLog("EoghanRuaApp.startup() success: window shown")
        except Exception as exc:
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            NSLog(f"Startup Exception: {exc}\n{tb}")
            self.main_window = toga.MainWindow(title=f"{self.formal_name} – Startup Error")
            self.main_window.content = toga.Label(
                f"Startup error:\n{exc}\n\nSee device log for details.",
                style=Pack(padding=20),
            )
            self.main_window.show()

    # ---- Navigation helpers you can call from views ----
    def goto_home(self):
        try:
            from eoghan_rua_team_selector.views.home import Home  # optional; keep if you have views
            content = Home(self)
        except Exception:
            # fallback if views/home.py not present
            content = toga.Label("Home view placeholder", style=Pack(padding=20))
        self.main_window.content = content
        self.main_window.show()

    def goto_builder(self):
        try:
            from eoghan_rua_team_selector.views.builder import Builder
            content = Builder(self)
        except Exception:
            content = toga.Label("Builder view placeholder", style=Pack(padding=20))
        self.main_window.content = content
        self.main_window.show()

    def goto_preview(self, teams, crest_bytes: bytes):
        try:
            from eoghan_rua_team_selector.views.preview import Preview
            content = Preview(self, teams, crest_bytes)
        except Exception:
            content = toga.Label("Preview view placeholder", style=Pack(padding=20))
        self.main_window.content = content
        self.main_window.show()


def main():
    """Briefcase calls main(); returning the App is sufficient."""
    return EoghanRuaApp(
        app_id="ie.eoghanrua.eoghanruateamselector",
        app_name="Eoghan Rua Team Selector",
        formal_name="Eoghan Rua Team Selector",
    )
