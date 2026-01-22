
# app.py
from toga import App
from eoghan_rua_team_selector.views.splash import Splash
from toga.style import Pack


class EoghanRuaApp(App):
    def startup(self):
        self.main_window = Splash(self)
        self.main_window.show()

    def goto_home(self):
        from eoghan_rua_team_selector.views.home import Home
        self.main_window = Home(self)
        self.main_window.show()

    def goto_builder(self):
        from eoghan_rua_team_selector.views.builder import Builder
        self.main_window = Builder(self)
        self.main_window.show()

    def goto_preview(self, teams, crest_bytes):
        from eoghan_rua_team_selector.views.preview import Preview
        self.main_window = Preview(self, teams, crest_bytes)
        self.main_window.show()


def main():
    return EoghanRuaApp(formal_name="Eoghan Rua Team Selector")
