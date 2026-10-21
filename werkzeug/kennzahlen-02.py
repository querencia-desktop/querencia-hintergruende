#!/usr/bin/env python3
"""Hintergründe 0.2: Kennzahlen je Datei wie im Wallpaper-Test (`auswerten.py`).

Benötigt nur Pillow. Aufruf: kennzahlen-02.py DATEI … > tabelle.tsv

Spalten (Graustufe L 0–255):
- mitte_l, mitte_kontrast: Mittelwert und Standardabweichung im Ausschnitt
  40 % × 40 % um die Bildmitte
- weiss_mitte, weiss_links: WCAG-Kontrast weißer Schrift gegen das
  90-%-Perzentil der Mitte bzw. der Symbolspalte (8 % der Breite zwischen
  zwei 32-px-Panels, auf die Bildhöhe umgerechnet); Ziel ≥ 4,5
- unruhe: mittlere Differenz zwischen leicht (σ 3) und stark (σ 25)
  weichgezeichneter Mitte (grobe Strukturen ohne Körnung)
- banding: Anteil der Pixel, deren 7×7-Umgebung in allen Kanälen höchstens
  eine Stufe umfasst; Ziel < 5 %
"""
import sys

from PIL import Image, ImageChops, ImageFilter, ImageStat


def lin(v):
    c = v / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def weiss_kontrast(stufe):
    return 1.05 / (lin(stufe) + 0.05)


def perzentil(hist, q):
    gesamt = sum(hist)
    acc = 0
    for i, n in enumerate(hist):
        acc += n
        if acc >= q * gesamt:
            return i
    return 255


def bereich(grau, box):
    crop = grau.crop(box)
    st = ImageStat.Stat(crop)
    return st.mean[0], st.stddev[0], perzentil(crop.histogram(), 0.9)


def banding(img):
    rng = []
    for ch in img.split():
        rng.append(ImageChops.subtract(ch.filter(ImageFilter.MaxFilter(7)),
                                       ch.filter(ImageFilter.MinFilter(7))))
    worst = ImageChops.lighter(ImageChops.lighter(rng[0], rng[1]), rng[2])
    h = worst.histogram()
    return 100 * (h[0] + h[1]) / sum(h)


def unruhe(grau, box):
    klein = grau.crop(box)
    klein = klein.resize((klein.width // 2, klein.height // 2), Image.BILINEAR)
    a = klein.filter(ImageFilter.GaussianBlur(3))
    b = klein.filter(ImageFilter.GaussianBlur(25))
    return ImageStat.Stat(ImageChops.difference(a, b)).mean[0]


def messen(pfad):
    img = Image.open(pfad).convert("RGB")
    w, h = img.size
    grau = img.convert("L")
    cbox = (int(0.3 * w), int(0.3 * h), int(0.7 * w), int(0.7 * h))
    panel = int(h * 32 / 1080)
    lbox = (0, panel, int(0.08 * w), h - panel)
    m_mittel, m_kontrast, m_p90 = bereich(grau, cbox)
    _, _, l_p90 = bereich(grau, lbox)
    return (f"{w}x{h}", m_mittel, m_kontrast, weiss_kontrast(m_p90), weiss_kontrast(l_p90),
            unruhe(grau, cbox), banding(img))


def main():
    print("datei\tgroesse\tmitte_l\tmitte_kontrast\tweiss_mitte\tweiss_links\tunruhe\tbanding")
    for pfad in sys.argv[1:]:
        g, ml, mk, wm, wl, u, b = messen(pfad)
        name = pfad.rsplit("/", 1)[-1]
        print(f"{name}\t{g}\t{ml:.0f}\t{mk:.0f}\t{wm:.1f}\t{wl:.1f}\t{u:.1f}\t{b:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
