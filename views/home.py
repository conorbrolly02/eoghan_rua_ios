
# views/home.py
import os
import toga

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

class Home(toga.MainWindow):
    def __init__(self, app):
        super().__init__(title="Eoghan Rua — Home", size=(480, 720))
        box = toga.Box(style=toga.style.Pack(direction="column", padding=16, alignment="center"))

        crest_path = os.path.join(ASSETS, "crest.png")
        if os.path.exists(crest_path):
            img = toga.Image(crest_path)
            box.add(toga.ImageView(img, style=toga.style.Pack(height=140, width=140, padding_bottom=10)))

        box.add(toga.Label("Create Teams", style=toga.style.Pack(font_size=20, padding=10)))
        box.add(toga.Button("Start", on_press=lambda w: app.goto_builder(), style=toga.style.Pack(padding=10, width=200)))

        self.content = box
