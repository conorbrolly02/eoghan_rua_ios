
# views/preview.py
import os
import io
import toga
from toga.style import Pack
from toga.style.pack import COLUMN

# Try importing Rubicon-ObjC (iOS-only). On Windows, this will fail: that's expected.
try:
    from rubicon.objc import ObjCClass, NSObject
    RUBICON_AVAILABLE = True
except Exception:
    RUBICON_AVAILABLE = False

from export_excel import build_excel_bytes_with_cover


class Preview(toga.MainWindow):
    def __init__(self, app, teams, crest_bytes):
        super().__init__(title="Teams Preview", size=(720, 920))
        self.app = app
        self.teams = teams
        self.crest_bytes = crest_bytes

        main_box = toga.Box(style=Pack(direction=COLUMN, padding=12))

        main_box.add(
            toga.Label(
                "Teams generated successfully.",
                style=Pack(padding_bottom=6, font_weight="bold")
            )
        )

        # Build preview text
        preview_lines = []
        sizes = [len(t["players"]) for t in teams]
        scores = [t["score"] for t in teams]

        if sizes:
            preview_lines.append(f"Roster sizes: {sizes} (range {max(sizes) - min(sizes)})")

        if scores:
            preview_lines.append(
                f"Strength scores → min: {min(scores)}  max: {max(scores)}  "
                f"range: {max(scores) - min(scores)}  avg: {sum(scores)/len(scores):.2f}"
            )

        preview_lines.append("")

        # Per-team details
        for t in teams:
            c = t["counts"]
            preview_lines.append(
                f"{t['name']}:  1s:{c[1]}  2s:{c[2]}  3s:{c[3]}  | Score:{t['score']}"
            )
            for nm, sk in t["players"]:
                preview_lines.append(f"  - {nm} (skill {sk})")
            preview_lines.append("")

        self.preview_area = toga.MultilineTextInput(
            readonly=True,
            value="\n".join(preview_lines),
            style=Pack(height=560)
        )
        main_box.add(self.preview_area)

        # Buttons row
        btn_row = toga.Box(style=Pack(direction="row", padding_top=10))
        btn_row.add(
            toga.Button(
                "Back",
                on_press=lambda w: app.goto_builder(),
                style=Pack(padding_right=8)
            )
        )
        btn_row.add(
            toga.Button(
                "Export Excel",
                on_press=self.export_excel,
                style=Pack(padding_right=8)
            )
        )
        btn_row.add(
            toga.Button(
                "Share Excel",
                on_press=self.share_excel,
            )
        )
        main_box.add(btn_row)

        self.status = toga.Label("", style=Pack(color="#888", padding_top=8))
        main_box.add(self.status)

        self.content = main_box

    # Create Excel file bytes
    def _excel_bytes(self):
        return build_excel_bytes_with_cover(self.teams, self.crest_bytes)

    # -------------------------------------------------------------------------
    # Export (works anywhere)
    # -------------------------------------------------------------------------
    def export_excel(self, widget):
        # Choose Documents directory for the platform
        try:
            path = toga.documents_path(self.app)  # BeeWare helper
        except Exception:
            # fallback if running on non-mobile platform
            path = os.path.expanduser("~/Documents")

        fname = "EoghanRua_Teams.xlsx"
        out_path = os.path.join(path, fname)

        try:
            with open(out_path, "wb") as f:
                f.write(self._excel_bytes())
            self.status.text = f"Saved Excel to: {out_path}"
        except Exception as e:
            self.status.text = f"Error writing Excel: {e}"

    # -------------------------------------------------------------------------
    # Share Excel (iOS only)
    # -------------------------------------------------------------------------
    def share_excel(self, widget):
        if not RUBICON_AVAILABLE:
            self.status.text = "Sharing is only available on iOS."
            return

        try:
            NSData = ObjCClass("NSData")
            NSURL = ObjCClass("NSURL")
            UIActivityViewController = ObjCClass("UIActivityViewController")
            UIApplication = ObjCClass("UIApplication")

            data_bytes = self._excel_bytes()

            # Write to temp file
            tmp_path = os.path.join(os.path.expanduser("~"), "tmp_eoghan_rua_teams.xlsx")
            with open(tmp_path, "wb") as f:
                f.write(data_bytes)

            # Prepare for share sheet
            url = NSURL.fileURLWithPath_(tmp_path)
            activityVC = UIActivityViewController.alloc().initWithActivityItems_applicationActivities_(
                [url], None
            )

            app = UIApplication.sharedApplication
            rootVC = app.keyWindow.rootViewController

            # Get the top-most presented VC
            while rootVC.presentedViewController:
                rootVC = rootVC.presentedViewController

            rootVC.presentViewController_animated_completion_(activityVC, True, None)
            self.status.text = "Share sheet opened."

        except Exception as e:
            self.status.text = f"Share failed: {e}"
