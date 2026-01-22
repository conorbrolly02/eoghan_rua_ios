
# app.py
import os
import io
from toga import App
from views.splash import Splash
from views.home import Home
from views.builder import Builder
from views.preview import Preview

class EoghanRuaApp(App):
    def startup(self):
        self.main_window = Splash(self)
        self.main_window.show()

    def goto_home(self):
        self.main_window = Home(self)
        self.main_window.show()

    def goto_builder(self):
        self.main_window = Builder(self)
        self.main_window.show()

    def goto_preview(self, teams, crest_bytes):
        self.main_window = Preview(self, teams, crest_bytes)
        self.main_window.show()


def main():
    return EoghanRuaApp(formal_name="Eoghan Rua Team Selector")
