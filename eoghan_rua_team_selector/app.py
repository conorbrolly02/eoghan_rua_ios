
# app.py  — with Option B diagnostics at the very top
# -----------------------------------------------
# 1) Enable verbose import tracing & fatal tracebacks *before* other imports
import sys
import os
import faulthandler
faulthandler.enable()                 # dump Python tracebacks on fatal errors
os.environ["PYTHONVERBOSE"] = "1"     # make Python print verbose import logs to NSLog (via std-nslog)

# 2) Prevent .pyc writes into iOS read-only bundle
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

# 3) Regular imports (after diagnostics are active)
import traceback
import toga
from rubicon.objc import NSLog


class EoghanRuaApp(toga.App):
    def startup(self):
        """
        App entry point for iOS. We:
          1) Log to iOS syslog so we can see what's happening.
          2) Lazy-import Splash so any import-time issues are caught here.
          3) Handle either a Window-returning Splash or a widget-returning Splash.
          4) Show a visible fallback window on error, with the exception text.
        """
        NSLog("EoghanRuaApp.startup() begin")

        try:
            # Lazy import so import errors are caught and logged below
            from eoghan_rua_team_selector.views.splash import Splash

            # Build first view/screen. Works whether Splash returns a Window or a widget.
            content = Splash(self)

            if isinstance(content, toga.Window):
                # Splash is a Window (e.g., toga.MainWindow subclass)
                self.main_window = content
            else:
                # Splash is a widget/layout: mount into a MainWindow
                self.main_window = toga.MainWindow(title=self.formal_name)
                self.main_window.content = content

            self.main_window.show()
            NSLog("EoghanRuaApp.startup() success: window shown")

        except Exception as exc:
            # Log full traceback to the iOS system log and present a visible error window
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            NSLog(f"Startup Exception: {exc}\n{tb}")

            self.main_window = toga.MainWindow(title=f"{self.formal_name} – Startup Error")
            self.main_window.content = toga.Label(
                f"Startup error:\n{exc}\n\nSee device log for details.",
                style=toga.style.Pack(padding=20),
            )
            self.main_window.show()

    # ---------------------------------------------------------
    # Navigation helpers: swap content or replace the window
    # ---------------------------------------------------------
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
    """
    Briefcase calls main(); returning the App is sufficient.
    Providing explicit ids/names is good practice on iOS.
    """
    return EoghanRuaApp(
        app_id="ie.eoghanrua.eoghan-rua-team-selector",
        app_name="Eoghan Rua Team Selector",
        formal_name="Eoghan Rua Team Selector",
    )

# For local debugging outside Briefcase, you could run:
# if __name__ == "__main__":
#     main().main_loop()
