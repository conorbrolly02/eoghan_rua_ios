
# export_excel.py
import io
from datetime import datetime
from typing import List, Dict, Optional

from PIL import Image as PILImage
import xlsxwriter

def _scale_png(png_bytes: bytes, max_px: int = 512) -> bytes:
    img = PILImage.open(io.BytesIO(png_bytes)).convert("RGBA")
    w, h = img.size
    scale = min(1.0, max_px / max(w, h))
    if scale < 1.0:
        img = img.resize((int(w*scale), int(h*scale)), PILImage.LANCZOS)
    out = io.BytesIO()
    img.save(out, format="PNG")
    out.seek(0)
    return out.read()

def build_excel_bytes_with_cover(teams: List[Dict], crest_png: Optional[bytes]) -> bytes:
    bio = io.BytesIO()
    wb = xlsxwriter.Workbook(bio, {'in_memory': True})
    # Cover
    cover = wb.add_worksheet("Cover")
    title_fmt = wb.add_format({'bold': True, 'font_size': 20})
    normal = wb.add_format({'font_size': 12})

    cover.write("A10", "Eoghan Rua — Team Sheets", title_fmt)
    cover.write("A12", f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal)
    cover.write("A14", f"Teams: {len(teams)}", normal)
    total_players = sum(len(t['players']) for t in teams)
    cover.write("A15", f"Total players: {total_players}", normal)

    if crest_png:
        crest_scaled = _scale_png(crest_png, max_px=300)
        # insert_image(x, y, filename=None, options={"image_data": BytesIO})
        cover.insert_image("A1", "crest.png", {"image_data": io.BytesIO(crest_scaled)})

    # Summary
    summary = wb.add_worksheet("Summary")
    headers = ["Team", "Player", "Skill (1=strongest)", "Team Score", "Team 1s", "Team 2s", "Team 3s"]
    for c, h in enumerate(headers):
        summary.write(0, c, h)

    r = 1
    for t in teams:
        cts = t["counts"]
        for name, skill in t["players"]:
            row = [t["name"], name, skill, t["score"], cts[1], cts[2], cts[3]]
            for c, val in enumerate(row):
                summary.write(r, c, val)
            r += 1

    # Per-team sheets
    for t in teams:
        ws = wb.add_worksheet(t["name"][:31])  # Excel sheet name limit
        ws.write_row(0, 0, ["Player", "Skill (1=strongest)"])
        for i, (nm, s) in enumerate(t["players"], start=1):
            ws.write_row(i, 0, [nm, s])

    wb.close()
    bio.seek(0)
    return bio.read()
