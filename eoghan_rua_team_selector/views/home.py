
import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")


class Home(toga.MainWindow):
    def __init__(self, app):
        super().__init__(title="Home", size=(480, 720))
        self.app = app

        box = toga.Box(style=Pack(direction=COLUMN, alignment="center", padding=16))

        crest_path = os.path.join(ASSETS, "crest.png")
        if os.path.exists(crest_path):
            img = toga.Image(crest_path)
            box.add(toga.ImageView(img, style=Pack(height=140, width=140)))

        box.add(toga.Button("Create Teams", on_press=lambda w: self.app.goto_builder(), style=Pack(padding_top=20)))

        self.content = box
