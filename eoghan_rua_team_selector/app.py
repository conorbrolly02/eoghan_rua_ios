
# app.py
import sys, os, traceback
from rubicon.objc import NSLog
import toga
from toga import App
from eoghan_rua_team_selector.views.splash import Splash

# Never try to write .pyc into the read-only bundle
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

class EoghanRuaApp(App):
    def startup(self):
        NSLog("EoghanRuaApp.startup() begin")
        try:
            content = Splash(self)  # Works if returns a Window or a widget
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
            # Keep the app open with a visible error
            self.main_window = toga.MainWindow(title=f"{self.formal_name} – Startup Error")
            self.main_window.content = toga.Label(
                f"Startup error:\n{exc}\n\nSee device log for details.", style=toga.style.Pack(padding=20)
            )
            self.main_window.show()

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

    def goto_preview(self, teams, crest_bytes):
        from eoghan_rua_team_selector.views.preview import Preview
        content = Preview(self, teams, crest_bytes)
        if isinstance(content, toga.Window):
            self.main_window = content
        else:
            self.main_window.content = content
        self.main_window.show()

def main():
    # Provide explicit ids/names; Briefcase will call main()
    return EoghanRuaApp(
        app_id="ie.eoghanrua.eoghan-rua-team-selector",
        app_name="Eoghan Rua Team Selector",
        formal_name="Eoghan Rua Team Selector",
    )
