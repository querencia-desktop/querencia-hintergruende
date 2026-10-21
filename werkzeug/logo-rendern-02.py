#!/usr/bin/env python3
"""Hintergründe 0.2: Querencia-Logo (SVG, nur lesend) in große PNG rendern.

Benötigt System-Python mit PyGObject/GdkPixbuf (SVG-Lader librsvg), kein GTK-Fenster.
Aufruf: /usr/bin/python3 -I logo-rendern-02.py <quell.svg> <zielordner>
Erzeugt q.png (nur Q-Zeichen), logo-weiss.png und logo-dunkel.png (Q orange,
Wortmarke weiß/hellgrau bzw. dunkelgrau/mittelgrau), alle im selben Maßstab (Höhe 1600 px).
"""
import hashlib
import os
import re
import sys

import gi
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf

src, out = sys.argv[1], sys.argv[2]
raw = open(src, "rb").read()
print("sha256", hashlib.sha256(raw).hexdigest())
svg = raw.decode("utf-8")
head = svg[:svg.index(">", svg.index("<svg")) + 1]
group = re.search(r"<g\b.*?</g>", svg, re.S).group(0)
variants = {
    "q": head + group + "</svg>",
    "logo-weiss": svg.replace("#3D2E1F", "#FFFFFF").replace("#6B5B4D", "#D8D8D8"),
    "logo-dunkel": svg.replace("#3D2E1F", "#3A3A3A").replace("#6B5B4D", "#6A6A6A"),
}
H = 1600
W = round(349 * H / 64)
for name, text in variants.items():
    tmp = os.path.join(out, name + ".svg")
    open(tmp, "w", encoding="utf-8").write(text)
    pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(tmp, W, H, True)
    pb.savev(os.path.join(out, name + ".png"), "png", [], [])
    print(name, pb.get_width(), pb.get_height())
