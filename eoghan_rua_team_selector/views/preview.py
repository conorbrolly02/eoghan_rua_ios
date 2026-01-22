
# views/preview.py
import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from eoghan_rua_team_selector.export_excel import build_excel_bytes_with_cover


class Preview(toga.MainWindow):
    def __init__(self, app, teams, crest_bytes):
        super().__init__(title="Teams Preview", size=(720, 900))
        self.app = app
        self.teams = teams
        self.crest_bytes = crest_bytes

        box = toga.Box(style=Pack(direction=COLUMN, padding=12))

        box.add(toga.Label("Teams generated:", style=Pack(font_weight="bold", padding_bottom=10)))

        lines = []
        sizes = [len(t["players"]) for t in teams]
        scores = [t["score"] for t in teams]

        if sizes:
            lines.append(f"Roster sizes: {sizes} (range {max(sizes) - min(sizes)})")

        if scores:
            lines.append(
                f"Strength scores → min:{min(scores)} max:{max(scores)} "
                f"range:{max(scores)-min(scores)} avg:{sum(scores)/len(scores):.2f}"
            )

        lines.append("")

        for t in teams:
            c = t["counts"]
            lines.append(f"{t['name']}: 1s:{c[1]} 2s:{c[2]} 3s:{c[3]} | Score:{t['score']}")
            for nm, sk in t["players"]:
                lines.append(f"  - {nm} (skill {sk})")
            lines.append("")

        self.preview = toga.MultilineTextInput(
            value="\n".join(lines), readonly=True, style=Pack(height=560)
        )
        box.add(self.preview)

        btn_row = toga.Box(style=Pack(direction="row", padding_top=10))
        btn_row.add(toga.Button("Back", on_press=lambda w: self.app.goto_builder(), style=Pack(padding_right=8)))
        btn_row.add(toga.Button("Export Excel", on_press=self.export_excel, style=Pack(padding_right=8)))
        btn_row.add(toga.Button("Share Excel", on_press=self.share_excel))
        box.add(btn_row)

        self.status = toga.Label("", style=Pack(color="#888", padding_top=10))
        box.add(self.status)

        self.content = box

    def _excel_bytes(self):
        return build_excel_bytes_with_cover(self.teams, self.crest_bytes)

    def export_excel(self, widget):
        try:
            path = toga.documents_path(self.app)
        except Exception:
            path = os.path.expanduser("~/Documents")

        out_path = os.path.join(path, "EoghanRua_Teams.xlsx")

        try:
            with open(out_path, "wb") as f:
                f.write(self._excel_bytes())
            self.status.text = f"Saved to {out_path}"
        except Exception as e:
            self.status.text = f"Error: {e}"

    def share_excel(self, widget):
        # Import iOS-only library inside function (Windows-safe)
        try:
            from rubicon.objc import ObjCClass
        except Exception:
            self.status.text = "Sharing available only on iOS."
            return

        try:
            NSData = ObjCClass("NSData")
            NSURL = ObjCClass("NSURL")
            UIActivityViewController = ObjCClass("UIActivityViewController")
            UIApplication = ObjCClass("UIApplication")

            bytes_data = self._excel_bytes()

            tmp = os.path.join(os.path.expanduser("~"), "tmp_eoghan_rua.xlsx")
            with open(tmp, "wb") as f:
                f.write(bytes_data)

            url = NSURL.fileURLWithPath_(tmp)
            activityVC = UIActivityViewController.alloc().initWithActivityItems_applicationActivities_([url], None)

            app = UIApplication.sharedApplication
            root = app.keyWindow.rootViewController
            while root.presentedViewController:
                root = root.presentedViewController

            root.presentViewController_animated_completion_(activityVC, True, None)
            self.status.text = "Share sheet opened."

        except Exception as e:
            self.status.text = f"Share failed: {e}"
