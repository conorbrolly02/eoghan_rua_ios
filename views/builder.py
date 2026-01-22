
# views/builder.py
import io, os, csv
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from team_logic import pick_teams

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


# --------------------------
# Manual Parsing
# --------------------------
def parse_manual(text: str):
    players, errs = [], []
    for i, line in enumerate((text or "").splitlines(), start=1):
        s = line.strip()
        if not s:
            continue

        if "," not in s:
            errs.append(f"Line {i}: expected 'Name,Skill'")
            continue

        name_part, skill_part = s.split(",", 1)
        name = name_part.strip()

        if not name:
            errs.append(f"Line {i}: empty name")
            continue

        try:
            sk = int(skill_part.strip())
        except Exception:
            errs.append(f"Line {i}: invalid skill '{skill_part.strip()}'")
            continue

        if sk not in (1, 2, 3):
            errs.append(f"Line {i}: skill must be 1,2,3 (got {sk})")
            continue

        players.append((name, sk))

    return players, errs


# --------------------------
# CSV Parsing
# --------------------------
def parse_csv(path: str):
    players, errs = [], []
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            rdr = csv.DictReader(f)
            if rdr.fieldnames is None:
                return [], ["CSV is empty or invalid"]

            hdrs = [h.strip().lower() for h in rdr.fieldnames]

            if "name" not in hdrs or "skill" not in hdrs:
                return [], ["CSV must include headers: name, skill"]

            for idx, row in enumerate(rdr, start=2):
                name = (row.get("name") or "").strip()
                skill_raw = (row.get("skill") or "").strip()

                try:
                    sk = int(skill_raw)
                except Exception:
                    errs.append(f"Row {idx}: invalid skill '{skill_raw}'")
                    continue

                if not name:
                    errs.append(f"Row {idx}: empty name")
                    continue

                if sk not in (1, 2, 3):
                    errs.append(f"Row {idx}: skill must be 1,2,3 (got {sk})")
                    continue

                players.append((name, sk))

    except Exception as e:
        errs.append(f"CSV read error: {e}")

    return players, errs


# --------------------------
# Builder Window
# --------------------------
class Builder(toga.MainWindow):
    def __init__(self, app):
        super().__init__(title="Create Teams", size=(640, 840))
        self.app = app
        self.csv_path = None
        self.crest_bytes = None

        # Widgets
        self.num_teams = toga.NumberInput(
            min_value=2,
            max_value=32,
            step=1,
            default=4,
            style=Pack(width=80)
        )

        self.seed_input = toga.TextInput(
            placeholder="Optional seed",
            style=Pack(width=140)
        )

        self.csv_label = toga.Label("No CSV selected")
        self.crest_label = toga.Label("No crest selected (will use default)")

        self.manual = toga.MultilineTextInput(
            placeholder="Name,Skill\nConor,1\nFinn,2\n...",
            style=Pack(height=200, width=560)
        )

        self.status = toga.Label("", style=Pack(color="#888"))

        # Main layout
        box = toga.Box(style=Pack(direction=COLUMN, padding=16))

        box.add(toga.Label("Number of teams:"))
        box.add(self.num_teams)

        box.add(toga.Label("Random seed (optional):"))
        box.add(self.seed_input)

        box.add(toga.Divider())
        box.add(toga.Label("CSV File (name,skill):"))
        box.add(self.csv_label)
        box.add(toga.Button("Select CSV", on_press=self.choose_csv))

        box.add(toga.Divider())
        box.add(toga.Label("Club crest (optional):"))
        box.add(self.crest_label)
        box.add(toga.Button("Select Crest", on_press=self.choose_crest))

        box.add(toga.Divider())
        box.add(toga.Label("Manual entries:"))
        box.add(self.manual)

        box.add(self.status)
        box.add(toga.Button("Generate Teams", on_press=self.generate, style=Pack(padding_top=10)))

        self.content = box

    # --------------------------
    # File Pickers
    # --------------------------
    async def choose_csv(self, widget):
        path = await self.open_file_dialog(
            title="Select CSV File",
            multiselect=False
        )
        if path:
            self.csv_path = path
            self.csv_label.text = f"CSV: {os.path.basename(path)}"

    async def choose_crest(self, widget):
        path = await self.open_file_dialog(
            title="Select Crest Image",
            multiselect=False
        )
        if not path:
            return
        try:
            with open(path, "rb") as f:
                self.crest_bytes = f.read()
            self.crest_label.text = f"Crest: {os.path.basename(path)}"
        except Exception as e:
            self.crest_label.text = f"Failed to load crest: {e}"

    # --------------------------
    # Generate Teams
    # --------------------------
    def generate(self, widget):
        players_all, errs = [], []

        # CSV
        if self.csv_path:
            p, e = parse_csv(self.csv_path)
            players_all.extend(p)
            errs.extend(e)

        # Manual entries
        p2, e2 = parse_manual(self.manual.value or "")
        players_all.extend(p2)
        errs.extend(e2)

        # Deduplicate names
        dedup = {nm: sk for nm, sk in players_all}
        players_all = [(nm, dedup[nm]) for nm in dedup]

        if errs:
            self.status.text = "Some rows skipped:\n" + "\n".join(errs[:8])

        n = int(self.num_teams.value)
        if len(players_all) < n:
            self.status.text = f"Need at least {n} players. Provided {len(players_all)}."
            return

        seed = None
        txt = (self.seed_input.value or "").strip()
        if txt:
            try:
                seed = int(txt)
            except:
                self.status.text = "Seed must be a whole number."
                return

        teams = pick_teams(players_all, n, seed)

        # Default crest
        if not self.crest_bytes:
            default_path = os.path.join(ASSETS, "crest.png")
            if os.path.exists(default_path):
                with open(default_path, "rb") as f:
                    self.crest_bytes = f.read()

        self.app.goto_preview(teams, self.crest_bytes)
