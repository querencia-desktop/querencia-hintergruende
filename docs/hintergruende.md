# Hintergründe 0.2: 16 Flux-Bilder, Paket querencia-hintergruende

Stand 21.10.2026. 16 ausgewählte Bilder aus dem Wallpaper-Test mit
FLUX1.1 [pro] Ultra über fal.ai, je in 2560×1440 und 4:3: 32 Dateien.
Entscheidung vom 21.10.2026: alle 16 in den Alpha-2-Paketsatz, Lizenz
freigegeben, Standardbild `tiefblau` (A01), eigenes Datenrepo und Paket,
damit das Repo `querencia-shell` klein bleibt. Herkunft, Seeds, Prompts und
Lizenz je Bild: `docs/herkunft.md`.

Die 17 Bilder von 0.1 (Querencia Blau, Abend, Blau 2, Erde, Nacht) bleiben
im Repo `querencia-shell` (`data/hintergruende/`).

## Dateien

| Ort | Inhalt |
|---|---|
| `data/hintergruende/querencia-<motiv>.png` | 2560×1440, 16:9 mittig aus dem Original (2731×1536), Lanczos; Standardgröße wie 0.1 |
| `data/hintergruende/querencia-<motiv>-4x3.png` | 2048×1536, eigener Ausschnitt in voller Höhe, nie gestaucht |
| `data/hintergruende/SHA256SUMS` | die 32 Dateien (Paket, Integration) |
| `quellen/<A–D>/<Bild>.png`, `quellen/SHA256SUMS` | die 13 fal-Originale unverändert mit C2PA (`caBX`); nicht installiert |
| `werkzeug/erzeugen-02.py` | erzeugt die Bilder aus `quellen/` (SHA256 der Quellen im Skript) |
| `werkzeug/logo-rendern-02.py`, `werkzeug/logo/querencia-logo-wortmarke.svg` | Logo-Vorlage (Kopie aus `querencia-web`, Commit `57a7697`) und Renderer (GdkPixbuf/librsvg) |
| `werkzeug/SHA256SUMS-alle` | alle 64 Dateien, auch 3840×2160 und 1920×1080 (nicht im Repo) |
| `werkzeug/kennzahlen-02.py` | Kennzahlen Mitte, Symbolspalte, Unruhe, Banding |

Motive (Dateistamm): `tiefblau` (A01, **Standard**), `blaugruen` (A04),
`blauschein` (A10), `glut` (B09), `huegel` (C01), `kueste` (C02), `duenen`
(C04), `see` (C05), `wueste` (C08), `berge` (C09), `strand` (C10), `glas`
(D08); dazu `tiefblau-logo`, `tiefblau-wortmarke`, `tiefblau-wasserzeichen`
und `bernstein-logo` (B03 nur mit Logo, so gewählt). Die Dateinamen und der
Installationspfad sind fest; Querencia Einstellungen 0.1.4 baut ihren
Galerie-Katalog darauf auf.

### Größen

3840×2160 und 1920×1080 sind nicht im Repo: Mit der Körnung komprimiert PNG
schlecht (alle 64 Dateien 256 MB). Im Repo und im Paket liegen 2560 und 4:3
(32 Dateien, 104 009 674 Bytes, 2,1–4,7 MB je Datei); der Desktop skaliert
auf jede Bildschirmgröße. Die beiden anderen Größen entstehen bit-gleich mit
`--alle` und sind gegen `werkzeug/SHA256SUMS-alle` prüfbar.

## Erzeugen und prüfen

Braucht Pillow ≥ 10 (z. B. in einer eigenen venv) und `/usr/bin/python3`
mit GdkPixbuf und SVG-Lader für das Logo. TMPDIR nie
auf `/tmp` (tmpfs), die Prüfung schreibt rund 260 MB:

```bash
TMPDIR=~/.cache/hg02-pruefen python3 -I werkzeug/erzeugen-02.py --pruefen
```

Erzeugt alle 64 Dateien in einen temporären Ordner und vergleicht sie mit
`werkzeug/SHA256SUMS-alle`, die 32 Repo-Dateien zusätzlich mit
`data/hintergruende/SHA256SUMS` und den Dateien selbst. Laufzeit rund 12
Minuten (Gleitkomma in Pillow, kein numpy). Neu erzeugen:
`werkzeug/erzeugen-02.py` (nur 2560 und 4:3 nach `data/hintergruende/`),
mit `--alle --ziel <ordner>` alle vier Größen.

## Verarbeitung

Je Ausgabe in Gleitkomma (Pillow-Modus F): Zuschnitt, Lanczos, dann eine
feine monochrome Körnung (nahezu gaußverteilt aus vier Zufallsbytes,
Standardabweichung 1,2 Stufen, fester Startwert je Datei), die zugleich als
Zufalls-Dither für die Rundung auf 8 bit dient. Das verhindert Banding beim
Skalieren und glättet die beiden Kandidaten mit sichtbaren Tonwertstufen
(A04 14,1 %, D08 31,2 % Banding-Risiko in der Quelle): alle Dateien liegen
bei 0,0 % (Maß wie `auswerten.py` des Tests: Anteil der Pixel, deren
7×7-Umgebung in allen Kanälen höchstens eine Stufe umfasst; Ziel < 5 %).

Retusche nur bei `huegel` (C01): zwei kleine helle Artefaktpunkte unten
rechts (1963/1407 und 2716/1456 im Original, Radius 11 bzw. 10 px) sind vor
dem Skalieren durch den 25×25-Median ihrer Umgebung ersetzt. Der übrige
Bildinhalt ist unverändert.

Die Ableitungen tragen keinen C2PA-Chunk mehr; deshalb liegen die
Originale mit ihren Content Credentials in `quellen/` (BFL Developer Terms
§6(i), `docs/herkunft.md`).

## Logo

Quelle `werkzeug/logo/querencia-logo-wortmarke.svg` (SHA256
`d96aebff8ce943de…`), gerendert in 1600 px Höhe, je Ausgabegröße mit
Lanczos verkleinert und mit Alpha aufgesetzt:

| Fassung | Lage |
|---|---|
| `-logo` | oranges Q, Höhe 4 % der Bildhöhe, rechts 3 % der Breite, **unten 7 % der Höhe** frei (über dem Panel); Kontrast Q gegen Grund `tiefblau` 6,6:1, `bernstein` 5,8:1 |
| `-wortmarke` | wie `-logo` mit Wortmarke, Farbe nach Helligkeit unter dem Logo (Schwelle L 140): bei `tiefblau` Weiß |
| `-wasserzeichen` | Q, Höhe 55 % der Bildhöhe, Mitte bei 70 % der Breite, senkrecht mittig; mit Weiß (entsättigt) aufgehellt bis WCAG-Kontrast **1,15:1**; Symbolspalte und Panel-Zone frei |

Logo und Wortmarke fallen unter die Markenregel (`docs/marke.md`).

## Einbau in Desktop und Einstellungen

Desktop und Einstellungen suchen die Bilder in `querencia/hintergruende/`
der XDG-Datenordner, zuerst `~/.local/share`, dann `/usr/share`
(`crates/querencia-desktop/src/config.rs` in `querencia-shell`,
`hintergrund.rs` in `querencia-einstellungen`).

- **Paket** `querencia-hintergruende` (Alpha 2, Packaging-Repo): installiert
  `data/hintergruende/*.png` nach `/usr/share/querencia/hintergruende/`
  (Modus 0644), dazu `COPYRIGHT`, `docs/herkunft.md` und `docs/marke.md`
  nach `/usr/share/doc/querencia-hintergruende/`. `quellen/` und
  `werkzeug/` gehören zur Quelle, nicht ins Binärpaket.
- **Standardbild:** Desktop 0.2.1 (`querencia-shell`)
  zeigt ohne `File=` `querencia-tiefblau.png`, fehlt es, wie bisher
  `querencia-blau.png`. Die Galerie der Einstellungen stellt den Standard
  in 0.1.4 um (Katalog `hintergrund_katalog.rs`).
- Desktop 0.2.0 und Einstellungen 0.1.3 kennen die neuen Motive
  nicht im Katalog; über den Dateidialog sind sie wählbar, `desktop.ini`
  mit `File=` auf eine der Dateien zeigt sie.

Helle Landschaften (`huegel`, `kueste`, `duenen`, `see`, `berge`, `wueste`):
Die weiße Symbolbeschriftung des Desktops (Textschatten, keine Hinterlegung)
ist dort schlecht lesbar (Weiß-Kontrast in der Symbolspalte 1,1–1,6:1).
Eine Hinterlegung ist ein eigener Punkt für Desktop 0.2.x, nicht Teil von
0.2.

## Grenzen

- 3840×2160 und 1920×1080 sind nicht installiert; auf 4K-Bildschirmen
  skaliert der Desktop 2560×1440 hoch (×1,5).
- Ultrabreite Bildschirme (21:9) schneiden oben und unten ab; das kleine Q
  liegt bei 16:10 noch im Bild (3 % Rand), die Wortmarke auch.
- Bilder werden bei `File=` leer nicht nach Seitenverhältnis gewählt: der
  Desktop zeigt die 16:9-Datei. Die 4:3-Fassung greift, wenn die
  Einstellungen sie in `File=` schreiben.
