# eoghan_rua_team_selector/export_excel.py
import io
from datetime import datetime
from PIL import Image as PILImage
import xlsxwriter

def _scale_png(png_bytes, max_px=300):
    img = PILImage.open(io.BytesIO(png_bytes)).convert("RGBA")
    w, h = img.size
    scale = min(1.0, max_px / max(w, h))
    if scale < 1.0:
        img = img.resize((int(w * scale), int(h * scale)), PILImage.LANCZOS)
    out = io.BytesIO()
    img.save(out, format="PNG")
    out.seek(0)
    return out.read()

def build_excel_bytes_with_cover(teams, crest_png):
    bio = io.BytesIO()
    wb = xlsxwriter.Workbook(bio, {'in_memory': True})

    # Cover page
    cover = wb.add_worksheet("Cover")
    title_fmt = wb.add_format({'bold': True, 'font_size': 22})
    body_fmt = wb.add_format({'font_size': 12})

    cover.write("A10", "Eoghan Rua — Team Sheets", title_fmt)
    cover.write("A12", f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", body_fmt)
    cover.write("A14", f"Teams: {len(teams)}", body_fmt)
    total_players = sum(len(t['players']) for t in teams)
    cover.write("A15", f"Players: {total_players}", body_fmt)

    if crest_png:
        from io import BytesIO
        scaled = _scale_png(crest_png)
        cover.insert_image("A1", "crest.png", {"image_data": BytesIO(scaled)})

    # Summary sheet
    summary = wb.add_worksheet("Summary")
    headers = [
        "Team", "Player", "Skill (1=strongest)", "Team Score",
        "Team 1s", "Team 2s", "Team 3s"
    ]
    summary.write_row(0, 0, headers)
    row = 1
    for t in teams:
        c = t["counts"]
        for name, skill in t["players"]:
            summary.write_row(row, 0, [
                t["name"], name, skill, t["score"],
                c[1], c[2], c[3]
            ])
            row += 1

    # Per-team sheets
    for t in teams:
        ws = wb.add_worksheet(t["name"][:31])
        ws.write_row(0, 0, ["Player", "Skill"])
        for i, (nm, sk) in enumerate(t["players"], start=1):
            ws.write_row(i, 0, [nm, sk])

    wb.close()
    bio.seek(0)
    return bio.read()
