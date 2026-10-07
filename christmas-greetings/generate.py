#!/usr/bin/env python3
"""
Christmas Greetings landing page generator.

Reads template.html, program.json and prospects.csv, then builds
output/<folder>/index.html for every prospect. Each page is a single
self-contained file: the logo and greeting audio are embedded, so you
can upload it anywhere or attach it to an email.

Run:  python3 generate.py
"""
import base64, csv, json, mimetypes, random, sys
from pathlib import Path

ROOT = Path(__file__).parent
LOGO_NAMES = ["logo.png", "logo.jpg", "logo.jpeg", "logo.webp", "logo.svg", "logo.gif"]
AUDIO_NAMES = ["greeting.mp3", "greeting.m4a", "greeting.wav", "greeting.ogg"]
MIME = {".svg": "image/svg+xml", ".mp3": "audio/mpeg", ".m4a": "audio/mp4",
        ".wav": "audio/wav", ".ogg": "audio/ogg", ".webp": "image/webp"}


def data_uri(path):
    mime = MIME.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def first_existing(folder, names):
    for n in names:
        p = folder / n
        if p.exists():
            return p
    # also accept any file that starts with logo/greeting
    stem = names[0].split(".")[0]
    for p in sorted(folder.glob(stem + ".*")):
        return p
    return None


def main():
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    program = json.loads((ROOT / "program.json").read_text(encoding="utf-8"))

    # Optional station logos in /assets
    for s in program["radio"]["stations"]:
        p = ROOT / s.get("logo_file", "")
        s["logo"] = data_uri(p) if s.get("logo_file") and p.is_file() else None
    daily = first_existing(ROOT / "assets", ["northumberland-daily.png", "northumberland-daily.svg"]) if (ROOT / "assets").exists() else None

    out_dir = ROOT / "output"
    out_dir.mkdir(exist_ok=True)
    built, problems = [], []

    with open(ROOT / "prospects.csv", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    for i, row in enumerate(rows):
        row = {k.strip(): (v or "").strip() for k, v in row.items() if k}
        folder_name = row.get("folder")
        name = row.get("business_name")
        if not folder_name or not name:
            problems.append(f"Row {i + 2}: missing folder or business_name, skipped")
            continue

        folder = ROOT / "prospects" / folder_name
        if not folder.is_dir():
            folder.mkdir(parents=True)
            problems.append(f"{name}: created empty folder prospects/{folder_name}")

        logo = first_existing(folder, LOGO_NAMES)
        audio = first_existing(folder, AUDIO_NAMES)
        if not logo:
            problems.append(f"{name}: no logo found, page shows business name in the digital greeting")
        if not audio:
            problems.append(f"{name}: no greeting audio found, page shows the script only")

        location = row.get("location", "")
        script = row.get("custom_script") or program["default_script"]
        script = script.replace("{CLIENT}", name).replace("{LOCATION}", location)
        if not location:
            script = script.replace(f"{name}, .", f"{name}.")

        headline = row.get("digital_headline") or program["digital_headlines"][i % len(program["digital_headlines"])]
        rep = {
            "name": row.get("rep_name") or program["default_rep"]["name"],
            "email": row.get("rep_email") or program["default_rep"]["email"],
            "phone": row.get("rep_phone") or program["default_rep"]["phone"],
        }

        data = {
            "business_name": name,
            "location": location,
            "contact_first_name": row.get("contact_first_name", ""),
            "script": script,
            "digital_headline": headline,
            "logo": data_uri(logo) if logo else None,
            "audio": data_uri(audio) if audio else None,
            "daily_logo": data_uri(daily) if daily else None,
            "rep": rep,
            "offer_note": row.get("offer_note", ""),
            "default_station": row.get("default_station", ""),
            "program": program,
        }
        blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
        html = template.replace("{{PAGE_DATA}}", blob)
        html = html.replace("{{BUSINESS_NAME}}", name.replace("&", "&amp;").replace("<", "&lt;"))

        dest = out_dir / folder_name
        dest.mkdir(exist_ok=True)
        (dest / "index.html").write_text(html, encoding="utf-8")
        built.append(f"{name}: output/{folder_name}/index.html")

    report = ["Built:"] + [f"  {b}" for b in built] + ["", "Needs attention:"] + ([f"  {p}" for p in problems] or ["  Nothing, all set."])
    (out_dir / "report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    sys.exit(main())
