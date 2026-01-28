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
    return Path(app.paths.app) / "resources" / name


class EoghanRuaApp(toga.App):
    def startup(self):
        NSLog("EoghanRuaApp.startup() begin")
        try:
            title = toga.Label(
                "Eoghan Rua Team Selector",
                style=Pack(font_size=18, font_weight="bold", padding_bottom=8),
            )
            subtitle = toga.Label(
                "Launch OK – tap Continue",
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

    def goto_home(self):
        try:
            from eoghan_rua_team_selector.views.home import Home
            content = Home(self)
        except Exception:
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
    return EoghanRuaApp(
        app_id="ie.eoghanrua.eoghanruateamselector",
        app_name="Eoghan Rua Team Selector",
        formal_name="Eoghan Rua Team Selector",
    )
