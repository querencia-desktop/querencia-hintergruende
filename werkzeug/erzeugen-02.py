#!/usr/bin/env python3
"""Hintergründe 0.2 (QD-093): erzeugt die 16 gewählten Flux-Bilder in vier Größen.

Quellen sind die 13 fal-Originale unter `quellen/` dieses Repos (Kandidaten
des Wallpaper-Tests vom 21.10.2026, FLUX1.1 [pro] Ultra über fal.ai,
2752×1536, unverändert mit C2PA-Chunk); jede Quelle wird über ihre SHA256
erkannt. Je Motiv entstehen:

  querencia-<motiv>-3840.png   3840×2160   16:9 mittig (2731×1536), Lanczos
  querencia-<motiv>.png        2560×1440   wie 0.1 die Standardgröße
  querencia-<motiv>-1920.png   1920×1080
  querencia-<motiv>-4x3.png    2048×1536   eigener 4:3-Ausschnitt in voller
                                           Höhe (kein gestauchtes 16:9)

Im Repo und im Paket liegen nur 2560×1440 und 4:3 (`data/hintergruende/`,
Liste `SHA256SUMS`); 3840 und 1920 entstehen nur mit `--alle` und sind über
`werkzeug/SHA256SUMS-alle` (alle 64 Dateien) prüfbar.

Verarbeitung je Ausgabe in Gleitkomma (Pillow-Modus F, feiner als 16 bit):
Zuschnitt, Lanczos, dann feine monochrome Körnung (Gauß-nah aus vier
gleichverteilten Zufallsbytes, Standardabweichung `koernung` in 8-bit-Stufen,
fester Startwert je Datei), die zugleich als Zufalls-Dither für die
Quantisierung auf 8 bit dient (Rundung). Danach Banding-Prüfung wie in
`auswerten.py` des Wallpaper-Tests (Anteil der Pixel, deren 7×7-Umgebung in
allen Kanälen höchstens eine Stufe umfasst); Ziel < 5 %.

Retusche nur bei „huegel“ (C01): zwei kleine helle Artefaktpunkte unten
rechts werden vor dem Skalieren durch den 25×25-Median ihrer Umgebung
ersetzt (Lage im Skript, `RETUSCHE`).

Logo-Fassungen (Markenregel, ENTSCHEIDUNGEN Nr. 5/24) werden aus der
SVG-Vorlage `logo/querencia-logo-wortmarke.svg` gesetzt, nie aus den
KI-Bildern; das Rendern übernimmt `logo-rendern-02.py` (System-Python mit
GdkPixbuf/librsvg), aufgerufen in einen temporären Ordner:
  -logo           kleines oranges Q unten rechts, Höhe 4 % der Bildhöhe,
                  rechts 3 % der Breite, unten 7 % der Höhe frei (Panel)
  -wortmarke      wie -logo mit der Wortmarke „Querencia Desktop“ (weiß oder
                  dunkelgrau nach der Helligkeit unter dem Logo, Schwelle L 140)
  -wasserzeichen  großes Q Ton in Ton, Höhe 55 % der Bildhöhe, Mitte bei
                  70 % der Breite, senkrecht mittig; entsättigt aufgehellt
                  (Weiß) mit so viel Deckkraft, dass der WCAG-Kontrast Q gegen
                  Umgebung 1,15:1 beträgt; Symbolspalte (120 px bei 1080) und
                  Panel-Zone (48 px bei 1080) bleiben frei

Aufruf (Pillow ≥ 10 nötig, z. B. `~/.cache/querencia-wallpaper-test-venv`):
  python3 -I erzeugen-02.py [--alle] [--quellen ORDNER] [--ziel ORDNER] [--nur MOTIV …]
  python3 -I erzeugen-02.py --pruefen [--quellen ORDNER]
`--ziel` ist standardmäßig `data/hintergruende/` des Repos; `--pruefen`
erzeugt alle 64 Dateien in einen temporären Ordner (TMPDIR nie auf tmpfs,
rund 260 MB) und vergleicht sie mit `SHA256SUMS-alle`, die 32 Repo-Dateien
zusätzlich mit `data/hintergruende/SHA256SUMS` und den Dateien dort
(Exit 0 = alles gleich). Das Protokoll (Banding je Datei, Logo-Lagen) geht
nach stdout.
"""
import argparse
import hashlib
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageMath, ImageStat

HIER = Path(__file__).resolve().parent
REPO = HIER.parent
DATEN = REPO / "data" / "hintergruende"
LOGO_SVG = HIER / "logo" / "querencia-logo-wortmarke.svg"
LOGO_SVG_SHA256 = "d96aebff8ce943de0047313e39539464ecd18520456d7b4483607ab405956513"
LOGO_RENDERN = HIER / "logo-rendern-02.py"
SYSTEM_PYTHON = "/usr/bin/python3"
QUELLEN_STANDARD = REPO / "quellen"
SUMMEN = DATEN / "SHA256SUMS"          # die 32 Dateien im Repo und im Paket
SUMMEN_ALLE = HIER / "SHA256SUMS-alle"  # alle 64 Dateien (auch 3840 und 1920)

QUELLE_B, QUELLE_H = 2752, 1536
GROESSEN = {           # Suffix -> (Breite, Höhe); "" ist die Standardgröße wie 0.1
    "-3840": (3840, 2160),
    "": (2560, 1440),
    "-1920": (1920, 1080),
    "-4x3": (2048, 1536),
}
IM_REPO = ("", "-4x3")   # Größen in data/hintergruende/ und im Paket
KOERNUNG_STANDARD = 1.2   # Standardabweichung der Körnung in 8-bit-Stufen
BANDING_ZIEL = 5.0        # Prozent

# Motiv -> Quelle (relativ zu --quellen), SHA256, Seed des Flux-Aufrufs,
# x-Versatz des 4:3-Ausschnitts (Breite 2048 von 2752; 352 = mittig),
# Körnung, ob die Fassung ohne Logo ausgegeben wird.
MOTIVE = {
    "tiefblau": dict(quelle="A/A01.png", seed=1001, x4x3=352,
                     sha="3622df436c2bbb87394e4699710efb68b6ea63b85cdd80906f1dcb3be3e2d8b9"),
    "blaugruen": dict(quelle="A/A04.png", seed=1004, x4x3=352,
                      sha="2b8275bd2beee34b50bd05ead860344e3318eca667362548bb5b57c7165d859d"),
    "blauschein": dict(quelle="A/A10.png", seed=1010, x4x3=352,
                       sha="50d20cb38243614fc2d9011a59097f8ee6b32ea1511a45b853cdb24ef63cf383"),
    "glut": dict(quelle="B/B09.png", seed=2009, x4x3=352,
                 sha="63b5c2814d30870064acc1c7adfc56d19bfb1587411c57f651c84859d338f271"),
    "bernstein": dict(quelle="B/B03.png", seed=2003, x4x3=352, ohne_logo=False,
                      sha="9b94173801699e06777fe4f049970c2feb557513815a0a04794486238030a1ce"),
    "huegel": dict(quelle="C/C01.png", seed=3001, x4x3=352,
                   sha="1e55b75299ac6feb64bd18f619c35f06ecc91887357030b3a960f87bb13247e3"),
    "kueste": dict(quelle="C/C02.png", seed=3002, x4x3=352,
                   sha="f945dbe7722416092ca1b9f184db0f1fabf3f3132c2158b43183c9589b3ac74c"),
    "duenen": dict(quelle="C/C04.png", seed=3004, x4x3=352,
                   sha="bf287db5953dbc293716e55520c3301cef179a3737900ab3fc4e129301f3a3b8"),
    "see": dict(quelle="C/C05.png", seed=3005, x4x3=352,
                sha="e6dbe80360e5dc56ca2258d7616b22ebff29ee258b3c152cc85739e277d68757"),
    "wueste": dict(quelle="C/C08.png", seed=3008, x4x3=200,
                   sha="5c5c77c106de3ab243589d5be22b10ba49009c4706f64f9fa1b0c4dc5c90f8d7"),
    "berge": dict(quelle="C/C09.png", seed=3009, x4x3=352,
                  sha="bd57708e75b182ca2bf6912a9bb21210a7dc9ca9303499539daf0d908d9fa1c0"),
    "strand": dict(quelle="C/C10.png", seed=3010, x4x3=352,
                   sha="f5763c53a50654f76df81420fe3e29644500ee8bc0217beda72f139531bc60ce"),
    "glas": dict(quelle="D/D08.png", seed=4008, x4x3=352,
                 sha="78e7203f32e01801ebc002837b34ac1195652fb36115c0c57116aa49446d2631"),
}

# Logo-Fassungen: (Motiv, Suffix, Variante)
LOGOS = [
    ("tiefblau", "-logo", "L1"),
    ("tiefblau", "-wortmarke", "L2"),
    ("tiefblau", "-wasserzeichen", "L3"),
    ("bernstein", "-logo", "L1"),
]

# Retusche: Motiv -> Liste (x, y, Radius) in Quellkoordinaten
RETUSCHE = {
    "huegel": [(1963, 1407, 11), (2716, 1456, 10)],
}

L1_HOEHE, L1_RECHTS, L1_UNTEN = 0.04, 0.03, 0.07
L2_SCHWELLE = 140
L3_HOEHE, L3_MITTE_X, L3_KONTRAST = 0.55, 0.70, 1.15
FREI_LINKS, FREI_UNTEN = 120 / 1080, 48 / 1080


def sha256(pfad):
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def dateiname(motiv, suffix, groesse):
    return f"querencia-{motiv}{suffix}{groesse}.png"


# --- Bildverarbeitung -------------------------------------------------------

def rauschen(groesse, sigma, seed):
    """Monochrome, nahezu gaußverteilte Körnung als F-Bild (Mittel 0)."""
    rnd = random.Random(seed)
    n = groesse[0] * groesse[1]
    teile = [Image.frombytes("L", groesse, rnd.randbytes(n)).convert("F") for _ in range(4)]
    faktor = sigma / 147.8   # Standardabweichung der Summe von vier Bytes
    return ImageMath.lambda_eval(
        lambda a: (a["u0"] + a["u1"] + a["u2"] + a["u3"] - 510.0) * faktor,
        u0=teile[0], u1=teile[1], u2=teile[2], u3=teile[3])


def quantisieren(kanal_f, koernung):
    """F-Kanal plus Körnung, Rundung auf 8 bit (Pillow schneidet ab, daher +0,5)."""
    return ImageMath.lambda_eval(lambda a: a["k"] + a["n"] + 0.5, k=kanal_f, n=koernung).convert("L")


def ausgabe(bild, box, groesse, sigma, seed):
    """Ausschnitt `box` der Quelle auf `groesse` bringen und körnen."""
    kanaele = [k.convert("F").crop(box) for k in bild.split()]
    if (box[2] - box[0], box[3] - box[1]) != groesse:
        kanaele = [k.resize(groesse, Image.LANCZOS) for k in kanaele]
    n = rauschen(groesse, sigma, seed)
    return Image.merge("RGB", [quantisieren(k, n) for k in kanaele])


def banding(img):
    rng = []
    for ch in img.split():
        rng.append(ImageChops.subtract(ch.filter(ImageFilter.MaxFilter(7)),
                                       ch.filter(ImageFilter.MinFilter(7))))
    worst = ImageChops.lighter(ImageChops.lighter(rng[0], rng[1]), rng[2])
    h = worst.histogram()
    return round(100 * (h[0] + h[1]) / sum(h), 2)


def retuschieren(bild, stellen):
    """Kleine Flecken durch den Median ihrer Umgebung ersetzen (weiche Maske)."""
    from PIL import ImageDraw
    glatt = bild.filter(ImageFilter.MedianFilter(25))
    maske = Image.new("L", bild.size, 0)
    d = ImageDraw.Draw(maske)
    for x, y, r in stellen:
        d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    maske = maske.filter(ImageFilter.GaussianBlur(2))
    return Image.composite(glatt, bild, maske)


# --- Logo -------------------------------------------------------------------

def lin(v):
    c = v / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rel_lum(rgb):
    r, g, b = (lin(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def logo_laden(ordner):
    q = Image.open(ordner / "q.png").convert("RGBA")
    qbox = q.getchannel("A").getbbox()
    marken = {}
    for k in ("weiss", "dunkel"):
        im = Image.open(ordner / f"logo-{k}.png").convert("RGBA")
        box = im.getchannel("A").getbbox()
        marken[k] = im.crop((qbox[0], min(qbox[1], box[1]), box[2], max(qbox[3], box[3])))
    return q.crop(qbox), marken


def skaliert(im, hoehe):
    f = hoehe / im.height
    return im.resize((max(1, round(im.width * f)), max(1, round(im.height * f))), Image.LANCZOS)


def logo_setzen(bild, variante, q, marken):
    """Gibt (Bild, Protokoll) zurück."""
    b, h = bild.size
    bild = bild.convert("RGBA")
    if variante in ("L1", "L2"):
        klein = skaliert(q, round(L1_HOEHE * h))
        rechts, unten = round(L1_RECHTS * b), round(L1_UNTEN * h)
        if variante == "L1":
            marke = klein
            info = {}
        else:
            # Helligkeit unter der weißen Wortmarke entscheidet die Farbe
            probe = skaliert(marken["weiss"], klein.height)
            box = (b - rechts - probe.width, h - unten - probe.height, b - rechts, h - unten)
            unter = ImageStat.Stat(bild.convert("L").crop(box)).mean[0]
            farbe = "weiss" if unter < L2_SCHWELLE else "dunkel"
            marke = skaliert(marken[farbe], klein.height)
            info = {"wortmarke": farbe, "helligkeit_unter_logo": round(unter, 1)}
        x, y = b - rechts - marke.width, h - unten - marke.height
        lage = (x, y, x + marke.width, y + marke.height)
        grund = tuple(ImageStat.Stat(bild.convert("RGB").crop(lage)).mean)
        bild.alpha_composite(marke, (x, y))
        q_orange = tuple(ImageStat.Stat(klein.convert("RGB"),
                                        klein.getchannel("A").point(lambda v: 255 if v > 200 else 0)).mean)
        info.update(lage=lage, q_hoehe_px=klein.height, abstand_unten_px=unten,
                    kontrast_q_grund=round(kontrast(q_orange, grund), 2))
        return bild.convert("RGB"), info
    # L3: großes Q, entsättigt (Weiß) aufgehellt bis Kontrast 1,15:1
    marke = skaliert(q, round(L3_HOEHE * h))
    maske = marke.getchannel("A")
    cx, cy = round(L3_MITTE_X * b), h // 2
    x, y = cx - marke.width // 2, cy - marke.height // 2
    assert x >= round(FREI_LINKS * h) and y + marke.height <= h - round(FREI_UNTEN * h)
    lage = (x, y, x + marke.width, y + marke.height)
    region = bild.crop(lage).convert("RGB")
    innen = maske.point(lambda v: 255 if v > 128 else 0)
    aussen = ImageChops.invert(innen)
    grund = tuple(ImageStat.Stat(region, aussen).mean)
    weiss = Image.new("RGB", region.size, (255, 255, 255))

    def mit(alpha):
        return Image.composite(weiss, region, maske.point(lambda v: round(v * alpha)))

    lo, hi = 0.0, 1.0
    for _ in range(24):
        mitte = (lo + hi) / 2
        if kontrast(tuple(ImageStat.Stat(mit(mitte), innen).mean), grund) < L3_KONTRAST:
            lo = mitte
        else:
            hi = mitte
    alpha = (lo + hi) / 2
    fertig = mit(alpha)
    erreicht = kontrast(tuple(ImageStat.Stat(fertig, innen).mean), grund)
    out = bild.convert("RGB")
    out.paste(fertig, lage[:2])
    return out, {"lage": lage, "q_hoehe_px": marke.height, "deckkraft": round(alpha, 3),
                 "kontrast": round(erreicht, 3)}


# --- Ablauf -----------------------------------------------------------------

def quelle_pruefen(quellen, motiv):
    m = MOTIVE[motiv]
    pfad = quellen / m["quelle"]
    if not pfad.is_file():
        sys.exit(f"Quelle fehlt: {pfad}")
    ist = sha256(pfad)
    if ist != m["sha"]:
        sys.exit(f"Quelle {pfad}: SHA256 {ist} statt {m['sha']}")
    return pfad


def speichern(bild, pfad):
    bild.save(pfad, "PNG", optimize=True, compress_level=9)


def erzeugen(quellen, ziel, nur=None, groessen=IM_REPO):
    if sha256(LOGO_SVG) != LOGO_SVG_SHA256:
        sys.exit(f"Logo {LOGO_SVG}: SHA256 weicht ab")
    ziel.mkdir(parents=True, exist_ok=True)
    protokoll = {}
    with tempfile.TemporaryDirectory(prefix="querencia-logo-") as tmp:
        subprocess.run([SYSTEM_PYTHON, "-I", str(LOGO_RENDERN), str(LOGO_SVG), tmp],
                       check=True, stdout=subprocess.DEVNULL)
        q, marken = logo_laden(Path(tmp))
    logos = {}
    for motiv, suffix, variante in LOGOS:
        logos.setdefault(motiv, []).append((suffix, variante))
    for motiv, m in MOTIVE.items():
        if nur and motiv not in nur:
            continue
        quelle = quelle_pruefen(quellen, motiv)
        bild = Image.open(quelle).convert("RGB")
        if bild.size != (QUELLE_B, QUELLE_H):
            sys.exit(f"{quelle}: {bild.size} statt {(QUELLE_B, QUELLE_H)}")
        if motiv in RETUSCHE:
            bild = retuschieren(bild, RETUSCHE[motiv])
        sigma = m.get("koernung", KOERNUNG_STANDARD)
        for gsuffix, groesse in GROESSEN.items():
            if gsuffix not in groessen:
                continue
            if gsuffix == "-4x3":
                box = (m["x4x3"], 0, m["x4x3"] + 2048, QUELLE_H)
            else:
                x0 = (QUELLE_B - round(QUELLE_H * 16 / 9)) // 2
                box = (x0, 0, x0 + round(QUELLE_H * 16 / 9), QUELLE_H)
            name = dateiname(motiv, "", gsuffix)
            seed = m["seed"] * 100 + list(GROESSEN).index(gsuffix)
            out = ausgabe(bild, box, groesse, sigma, seed)
            eintrag = {"groesse": groesse, "ausschnitt": box, "koernung": sigma,
                       "banding": banding(out)}
            if m.get("ohne_logo", True):
                speichern(out, ziel / name)
                protokoll[name] = eintrag
                print(f"{name}: {groesse[0]}x{groesse[1]} Ausschnitt {box} Körnung {sigma} "
                      f"Banding {eintrag['banding']} %")
            for suffix, variante in logos.get(motiv, []):
                lname = dateiname(motiv, suffix, gsuffix)
                mit_logo, info = logo_setzen(out, variante, q, marken)
                speichern(mit_logo, ziel / lname)
                protokoll[lname] = dict(eintrag, variante=variante, **info)
                print(f"{lname}: {variante} {info}")
    return protokoll


def summen_lesen(datei):
    soll = {}
    for zeile in datei.read_text().splitlines():
        if zeile.strip():
            wert, name = zeile.split(maxsplit=1)
            soll[name.lstrip("*")] = wert
    return soll


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--quellen", type=Path, default=QUELLEN_STANDARD)
    p.add_argument("--ziel", type=Path, default=DATEN)
    p.add_argument("--nur", nargs="*")
    p.add_argument("--alle", action="store_true", help="auch 3840 und 1920 erzeugen")
    p.add_argument("--protokoll", type=Path, help="Messwerte als JSON")
    p.add_argument("--pruefen", action="store_true")
    a = p.parse_args()
    if not a.pruefen:
        groessen = tuple(GROESSEN) if a.alle else IM_REPO
        prot = erzeugen(a.quellen, a.ziel, a.nur, groessen)
        if a.protokoll:
            a.protokoll.write_text(json.dumps(prot, indent=1, ensure_ascii=False) + "\n")
        schlecht = [n for n, e in prot.items() if e["banding"] >= BANDING_ZIEL]
        if schlecht:
            print(f"WARNUNG Banding >= {BANDING_ZIEL} %: {', '.join(schlecht)}")
            return 1
        return 0
    alle = summen_lesen(SUMMEN_ALLE)
    repo = summen_lesen(SUMMEN)
    fehler = 0
    for name, wert in sorted(repo.items()):
        if alle.get(name) != wert:
            fehler += 1
            print(f"FAIL {name}: SHA256SUMS und SHA256SUMS-alle verschieden")
    with tempfile.TemporaryDirectory(prefix="querencia-hintergruende-02-") as tmp:
        erzeugen(a.quellen, Path(tmp), groessen=tuple(GROESSEN))
        for neu in sorted(Path(tmp).iterdir()):
            ist = sha256(neu)
            ok = alle.get(neu.name) == ist
            if neu.name in repo:
                ok = ok and repo[neu.name] == ist and sha256(DATEN / neu.name) == ist
            fehler += not ok
            ort = "Repo " if neu.name in repo else "nur Liste"
            print(f"{'OK  ' if ok else 'FAIL'} {neu.name} {ist[:16]} ({ort.strip()})")
        fehlend = sorted(set(alle) - {p.name for p in Path(tmp).iterdir()})
        for name in fehlend:
            fehler += 1
            print(f"FAIL {name} nicht erzeugt")
    print(f"{'PASS' if not fehler else 'FAIL'}: {fehler} Abweichung(en)")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
