
import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")


class Splash(toga.MainWindow):
    def __init__(self, app):
        super().__init__(title="Eoghan Rua — Team Selector", size=(420, 640))
        self.app = app

        box = toga.Box(style=Pack(direction=COLUMN, alignment="center", padding=20))

        crest_path = os.path.join(ASSETS, "crest.png")
        if os.path.exists(crest_path):
            img = toga.Image(crest_path)
            box.add(toga.ImageView(img, style=Pack(height=180, width=180)))

        box.add(toga.Label("Eoghan Rua — Team Selector", style=Pack(font_size=20, padding_top=10)))

        box.add(
            toga.Button("Continue", on_press=lambda w: self.app.goto_home(), style=Pack(padding_top=20))
        )

        self.content = box
