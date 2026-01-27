# eoghan_rua_team_selector/app.py
import sys
import os
import faulthandler
faulthandler.enable()

# Avoid .pyc in the iOS bundle
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import traceback
from pathlib import Path
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from rubicon.objc import NSLog


def resource_path(app: toga.App, name: str) -> Path:
    """Resolve a file from the bundled iOS resources."""
    return Path(app.paths.app) / "resources" / name


class EoghanRuaApp(toga.App):
    def startup(self):
        """Create the first window and show Splash (or a visible error)."""
        NSLog("EoghanRuaApp.startup() begin")
        try:
            # Lazy import so import-time issues are caught here:
            from eoghan_rua_team_selector.views.splash import Splash

            content = Splash(self)
            if isinstance(content, toga.Window):
                self.main_window = content
            else:
                self.main_window = toga.MainWindow(title=self.formal_name)
                self.main_window.content = content
            self.main_window.show()
            NSLog("EoghanRuaApp.startup() success: window shown")
        except Exception as exc:
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            NSLog(f"Startup Exception: {exc}\n{tb}")
            self.main_window = toga.MainWindow(
                title=f"{self.formal_name} – Startup Error"
            )
            self.main_window.content = toga.Label(
                f"Startup error:\n{exc}\n\nSee device log for details.",
                style=Pack(padding=20),
            )
            self.main_window.show()

    # ---- Navigation helpers ----
    def goto_home(self):
        from eoghan_rua_team_selector.views.home import Home
        content = Home(self)
        if isinstance(content, toga.Window):
            self.main_window = content
        else:
            self.main_window.content = content
        self.main_window.show()

    def goto_builder(self):
        from eoghan_rua_team_selector.views.builder import Builder
        content = Builder(self)
        if isinstance(content, toga.Window):
            self.main_window = content
        else:
            self.main_window.content = content
        self.main_window.show()

    def goto_preview(self, teams, crest_bytes: bytes):
        from eoghan_rua_team_selector.views.preview import Preview
        content = Preview(self, teams, crest_bytes)
        if isinstance(content, toga.Window):
            self.main_window = content
        else:
            self.main_window.content = content
        self.main_window.show()


def main():
    """Briefcase calls main(); returning the App is sufficient."""
    return EoghanRuaApp(
        app_id="ie.eoghanrua.eoghan_rua_team_selector",
        app_name="Eoghan Rua Team Selector",
        formal_name="Eoghan Rua Team Selector",
    )
``
