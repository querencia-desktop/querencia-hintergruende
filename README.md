# Querencia Hintergründe

Die 16 KI-Hintergründe von Querencia Desktop ab Version 0.2 (Alpha 2):
ruhige Verläufe, Landschaften und Glasflächen, erzeugt mit FLUX1.1 [pro]
Ultra (Black Forest Labs) über fal.ai, ausgewählt vom Projektbesitzer.
Standardbild ist **tiefblau**. Jedes Motiv liegt in 2560×1440 (16:9) und als
eigener 4:3-Ausschnitt (2048×1536) vor, zusammen 32 PNG-Dateien (104 MB).

| Motiv | Datei (16:9 / 4:3) |
|---|---|
| Tiefblau (Standard) | `querencia-tiefblau.png` / `querencia-tiefblau-4x3.png` |
| Tiefblau mit Logo, mit Wortmarke, mit Wasserzeichen | `querencia-tiefblau-logo…`, `-wortmarke…`, `-wasserzeichen…` |
| Blaugrün, Blauschein, Glut, Glas | `querencia-blaugruen…`, `-blauschein…`, `-glut…`, `-glas…` |
| Bernstein mit Logo | `querencia-bernstein-logo…` |
| Hügel, Küste, Dünen, See, Wüste, Berge, Strand | `querencia-huegel…`, `-kueste…`, `-duenen…`, `-see…`, `-wueste…`, `-berge…`, `-strand…` |

## Installation

Das Debian-Paket `querencia-hintergruende` legt die Bilder nach
`/usr/share/querencia/hintergruende/`. Dort suchen die Arbeitsfläche
(`querencia-desktop`) und Querencia Einstellungen; ein Ordner
`~/.local/share/querencia/hintergruende/` hat Vorrang.

Von Hand:

```bash
sudo install -d /usr/share/querencia/hintergruende
```

```bash
sudo install -m 0644 data/hintergruende/*.png /usr/share/querencia/hintergruende/
```

Ohne Root-Rechte für einen Benutzer: die Dateien nach
`~/.local/share/querencia/hintergruende/` kopieren. Auf der
Entwicklungs-VM gilt `integration/0.2/` (siehe `docs/hintergruende.md`).

## Prüfen und neu erzeugen

```bash
(cd data/hintergruende && sha256sum -c SHA256SUMS)
```

Die Bilder entstehen reproduzierbar aus den Originalen in `quellen/`:

```bash
TMPDIR=~/.cache/hg02-pruefen python3 -I werkzeug/erzeugen-02.py --pruefen
```

(braucht Pillow ≥ 10 und `/usr/bin/python3` mit GdkPixbuf; rund 12 Minuten).

## Aufbau

```
data/hintergruende/   32 Bilder und SHA256SUMS (das Paket)
quellen/              13 fal-Originale mit Content Credentials (C2PA), nicht installiert
werkzeug/             Erzeuger, Logo-Renderer, Kennzahlen, SHA256SUMS-alle
integration/0.2/      Live-Weg der Entwicklungs-VM und Proben
docs/                 Spezifikation, Herkunft, Markenregel
nachweis/             Prüfbelege
```

## Lizenz

Bilder und Originale: **CC-BY-SA-4.0** (Text in `LICENSE`), Namensnennung
„Querencia Desktop contributors“; Werkzeuge: GPL-3.0-or-later
(`werkzeug/LICENSE`). Das Querencia-Logo und die Wortmarke in den Fassungen
`-logo`, `-wortmarke` und `-wasserzeichen` sind davon ausgenommen
(`docs/marke.md`). Die Bilder sind KI-erzeugt; rein KI-erzeugte Werke sind
womöglich nicht urheberrechtlich geschützt, die Lizenzangabe ist dann ein
Hinweis. Einzelheiten: `COPYRIGHT`, Herkunft je Bild: `docs/herkunft.md`.
