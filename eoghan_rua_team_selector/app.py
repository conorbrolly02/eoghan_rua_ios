
# app.py
import sys
import traceback
import toga
from toga import App
from rubicon.objc import NSLog   # logs to iOS system log (visible in idevicesyslog)
from eoghan_rua_team_selector.views.splash import Splash


class EoghanRuaApp(App):
    def startup(self):
        NSLog("EoghanRuaApp.startup() begin")

        try:
            # --- If Splash is a WINDOW subclass (e.g., inherits toga.MainWindow) ---
            # self.main_window = Splash(self)

            # --- If Splash BUILDS CONTENT (e.g., returns a Box), use a MainWindow and set content ---
            # Prefer this pattern unless Splash truly subclasses a Window:
            content = Splash(self)  # If Splash returns a widget, not a Window
            if isinstance(content, toga.Window):
                # Splash *is* a Window subclass
                self.main_window = content
            else:
                # Splash builds widgets; mount them into a Window
                self.main_window = toga.MainWindow(title=self.formal_name)
                self.main_window.content = content

            self.main_window.show()
            NSLog("EoghanRuaApp.startup() success: window shown")

        except Exception as exc:
            # Log full stack trace to iOS syslog *and* show a fallback window so the app stays open
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            NSLog(f"Startup Exception: {exc}\n{tb}")

            # Minimal visible fallback so we can read the error
            self.main_window = toga.MainWindow(title=f"{self.formal_name} – Startup Error")
            self.main_window.content = toga.Label(
                f"Startup error:\n{exc}\n\nSee device log for details.",
                style=toga.style.Pack(padding=20)
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
    # It’s good practice to provide app_id and app_name explicitly on iOS.
    return EoghanRuaApp(
        app_id="ie.eoghanrua.eoghan-rua-team-selector",
        app_name="Eoghan Rua Team Selector",
        formal_name="Eoghan Rua Team Selector",
    )

# If you ever run this module directly (e.g., in a local Python run), uncomment:
# if __name__ == "__main__":
#     main().main_loop()
