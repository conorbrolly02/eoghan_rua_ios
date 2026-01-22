
# views/splash.py
import os
import toga

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

class Splash(toga.MainWindow):
    def __init__(self, app):
        super().__init__(title="Eoghan Rua — Team Selector", size=(420, 640))
        box = toga.Box(style= toga.style.Pack(direction="column", alignment="center", padding=20))
        crest_path = os.path.join(ASSETS, "crest.png")
        if os.path.exists(crest_path):
            img = toga.Image(crest_path)
            box.add(toga.ImageView(img, style=toga.style.Pack(height=180, width=180, padding_bottom=20)))
        box.add(toga.Label("Eoghan Rua — Team Selector", style=toga.style.Pack(font_size=18, padding=10)))
        box.add(toga.Label("Balanced teams • Offline • Excel export", style=toga.style.Pack(color="#888")))
        box.add(toga.Button("Continue", on_press=lambda w: app.goto_home(), style=toga.style.Pack(padding_top=30)))
        self.content = box
