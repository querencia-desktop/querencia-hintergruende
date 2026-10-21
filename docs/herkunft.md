# Herkunft der Hintergründe 0.2

Stand 21.10.2026 (QD-093). Herkunft, Erzeuger, Prompts, Bearbeitung und
Lizenz je Bild in `data/hintergruende/`. Prüfsummen: `data/hintergruende/SHA256SUMS`
(32 Dateien im Repo und im Paket), `werkzeug/SHA256SUMS-alle` (alle 64
Dateien, auch 3840 und 1920), `quellen/SHA256SUMS` (13 Originale).
Erzeugt mit `werkzeug/erzeugen-02.py` (Prüfung `--pruefen`). Übernommen aus
`querencia-runtime`, Zweig `hintergruende-0.2`, Commit `370eddf`
(`data/hintergruende/HERKUNFT.md`, Abschnitt „Hintergründe 0.2“); die 17
Bilder von 0.1 (Querencia Blau, Abend, Blau 2, Erde, Nacht) bleiben im
Runtime-Repo und sind hier nicht enthalten.

16 vom Besitzer gewählte Bilder aus dem Wallpaper-Test
(, Auswahl §11: A01, A04, A10, B09, C01,
C02, C04, C05, C08, C09, C10, D08 sowie die Logo-Fassungen L-A01-L1/L2/L3 und
L-B03-L1). Entscheidung des Besitzers 21.10.2026 19:50: alle 16 kommen in den
Alpha-2-Paketsatz, Standardbild ist `tiefblau` (A01), Ablage als eigenes
Datenrepo und Paket `querencia-hintergruende`.

## Lizenz

**Freigegeben vom Besitzer am 21.10.2026 19:50** (08 QD-093). Befund der
Startsession zu den Nutzungsbedingungen: Black Forest Labs, Developer Terms
vom 4.8.2026, §3(b) und §4(b): die Ausgaben gehören dem Nutzer, kommerzielle
Nutzung ist erlaubt; §6(i): Content Credentials (C2PA) nicht entfernen.

- Bilder **ohne Logo**: **CC-BY-SA-4.0** mit KI-Vorbehalt wie ENTSCHEIDUNGEN
  Nr. 15 und Nr. 19. Rein KI-erzeugte Bilder sind in manchen
  Rechtsordnungen womöglich nicht urheberrechtlich geschützt; die
  Lizenzangabe ist dann ein Hinweis zur Nutzung, kein durchsetzbarer Schutz.
- Bilder **mit Q-Logo oder Wortmarke** (`-logo`, `-wortmarke`,
  `-wasserzeichen`): das Grundbild wie oben, das Logo zusätzlich unter der
  **Markenregel** (Nr. 5, Nr. 24, `docs/marke.md`). Das Logo ist Kennzeichen
  von Querencia Desktop, nicht frei und von der Bildlizenz ausgenommen; es
  wurde per Skript aus der SVG-Vorlage aufgeprägt, nie von der KI gemalt.
- **Content Credentials:** Die bearbeiteten Ableitungen in
  `data/hintergruende/` tragen keinen C2PA-Chunk mehr (Pillow schreibt nur
  IHDR/IDAT/IEND). Die Originale liegen deshalb unverändert mit ihrem
  C2PA-Chunk `caBX` unter `quellen/` und gehören zur Quelle jeder
  Weitergabe; sie werden nicht installiert.
- `werkzeug/` (Skripte): GPL-3.0-or-later, Text in `werkzeug/LICENSE`.

## Erzeuger

| Angabe | Wert |
|---|---|
| Dienst | fal.ai, Endpunkt `fal-ai/flux-pro/v1.1-ultra` |
| Modell | **FLUX1.1 [pro] Ultra** (Black Forest Labs) |
| Datum | 21.10.2026, 18:10:43 bis 18:12:54 Uhr (Zeitstempel der Antwortdateien) |
| Bediener | Worker-Session Wallpaper-Test im Auftrag der Startsession, Zugangsschlüssel des Besitzers |
| Parameter | `aspect_ratio 16:9`, `output_format png`, `num_images 1`, `enable_safety_checker true`, `safety_tolerance "2"`; `raw true` nur bei den Landschaften (C) |
| Ergebnis | 2752×1536 PNG je Bild, 0,06 USD je Bild |
| Prompts, Antworten | `~/projects/querencia-wallpaper-test/prompts.md`, `logs/<Bild>.json` (kein Repo); Grundprompt und Variation je Motiv unten |
| Logo | nicht von der KI: aus `werkzeug/logo/querencia-logo-wortmarke.svg` (Kopie von `querencia-web/assets/querencia-logo.svg`, Commit `57a7697`, SHA256 `d96aebff8ce943de…`) mit `werkzeug/logo-rendern-02.py` gerendert und von `werkzeug/erzeugen-02.py` aufgeprägt |

Grundprompts (die Variation steht je Motiv in der Tabelle):

- **A „Querencia Blau“:** Minimalist abstract desktop wallpaper, soft deep
  blue color gradient with smooth tonal transitions from midnight navy to
  classic cobalt blue, a faint diffuse glow of light, subtle fine film grain,
  calm and empty center area, no objects, no text, no letters, no logos, no
  symbols, no people, *Variation*
- **B „Human“:** Minimalist abstract desktop wallpaper in the spirit of
  classic 2010 Linux desktops, warm brown, ochre and burnt orange tones,
  smooth velvety gradient, soft subtle lighting, calm and empty center area,
  no objects, no text, no letters, no logos, no symbols, no people, *Variation*
- **C „Landschaften“:** Serene landscape photograph for a desktop wallpaper,
  wide composition with lots of open sky, low horizon in the bottom quarter
  of the frame, calm empty center, soft natural light, muted colors, no
  people, no buildings, no animals, no text, no logos, no watermark,
  *Variation*
- **D „Abstrakt-geometrisch“:** Minimalist abstract desktop wallpaper, soft
  smooth flowing shapes in blue and slate grey-blue tones, gentle gradients,
  low contrast, calm and empty center area, elegant and quiet, no objects,
  no text, no letters, no logos, no symbols, no people, *Variation*

## Quellen

`quellen/<Familie>/<Bild>.png`: die 13 fal-Originale, byte-gleich aus
`~/projects/querencia-wallpaper-test/kandidaten/` kopiert (Chunks IHDR,
IDAT, IEND und C2PA `caBX`). 13 statt 16, weil die vier Logo-Fassungen aus
A01 und B03 entstehen; die Testdateien `kandidaten/L/L-*.png` sind lokale
Ableitungen ohne C2PA und werden nicht verwendet.

| Datei | Bytes | SHA256 |
|---|---|---|
| `A/A01.png` | 3 271 235 | `3622df436c2bbb87394e4699710efb68b6ea63b85cdd80906f1dcb3be3e2d8b9` |
| `A/A04.png` | 3 445 449 | `2b8275bd2beee34b50bd05ead860344e3318eca667362548bb5b57c7165d859d` |
| `A/A10.png` | 4 135 581 | `50d20cb38243614fc2d9011a59097f8ee6b32ea1511a45b853cdb24ef63cf383` |
| `B/B03.png` | 4 007 010 | `9b94173801699e06777fe4f049970c2feb557513815a0a04794486238030a1ce` |
| `B/B09.png` | 3 957 782 | `63b5c2814d30870064acc1c7adfc56d19bfb1587411c57f651c84859d338f271` |
| `C/C01.png` | 1 903 971 | `1e55b75299ac6feb64bd18f619c35f06ecc91887357030b3a960f87bb13247e3` |
| `C/C02.png` | 2 551 462 | `f945dbe7722416092ca1b9f184db0f1fabf3f3132c2158b43183c9589b3ac74c` |
| `C/C04.png` | 2 239 726 | `bf287db5953dbc293716e55520c3301cef179a3737900ab3fc4e129301f3a3b8` |
| `C/C05.png` | 2 248 872 | `e6dbe80360e5dc56ca2258d7616b22ebff29ee258b3c152cc85739e277d68757` |
| `C/C08.png` | 2 609 520 | `5c5c77c106de3ab243589d5be22b10ba49009c4706f64f9fa1b0c4dc5c90f8d7` |
| `C/C09.png` | 2 201 843 | `bd57708e75b182ca2bf6912a9bb21210a7dc9ca9303499539daf0d908d9fa1c0` |
| `C/C10.png` | 2 505 389 | `f5763c53a50654f76df81420fe3e29644500ee8bc0217beda72f139531bc60ce` |
| `D/D08.png` | 2 750 050 | `78e7203f32e01801ebc002837b34ac1195652fb36115c0c57116aa49446d2631` |

## Je Motiv

Alle Fassungen: 16:9 mittig aus 2752×1536 (2731×1536), Lanczos auf die
Zielgröße; 4:3 als Ausschnitt 2048×1536 in voller Höhe (x-Versatz 352 =
mittig, sonst in der Tabelle); danach feine monochrome Körnung
(Standardabweichung 1,2 Stufen, fester Startwert je Datei) als
Zufalls-Dither bei der Rundung auf 8 bit. Banding je Datei:
`nachweis/kennzahlen.tsv`.

| Motiv (Dateistamm) | Bild | Seed | Uhrzeit | fal-Request-ID | Variation | Bearbeitung |
|---|---|---|---|---|---|---|
| `tiefblau` (**Standard**) | A01 | 1001 | 18:10:43 | `01a15f3a-78d9-7812-a315-df768c31bc2d` | the soft glow comes from the upper left corner | Zuschnitt, Lanczos, Körnung |
| `blaugruen` | A04 | 1004 | 18:10:43 | `01a15f3a-78d9-7a52-9f67-01f5a8565971` | slight teal undertone, the glow comes from the right side | wie oben; **Nachkörnung** gegen Banding (Quelle 14,1 %) |
| `blauschein` | A10 | 1010 | 18:11:08 | `01a15f3a-d998-7ea2-811f-a6c0df27935a` | misty periwinkle light diffusing through dark blue, like light through frosted glass | wie oben |
| `glut` | B09 | 2009 | 18:11:43 | `01a15f3b-6df8-7153-941b-0c76e09256a5` | dark aubergine blending into warm brown with a hint of orange warmth | wie oben |
| `bernstein` | B03 | 2003 | 18:11:22 | `01a15f3b-0ff9-7ff0-83f6-1e7378959686` | deep chocolate brown fading into a soft amber glow at the bottom | wie oben; **nur als Logo-Fassung** ausgegeben (Auswahl L-B03-L1) |
| `huegel` | C01 | 3001 | 18:11:59 | `01a15f3b-9c62-7da3-aded-51256dedfea2` | dawn over gently rolling hills, soft pink and pale blue sky | **Retusche**: zwei helle Artefaktpunkte unten rechts (Quellkoordinaten 1963/1407 und 2716/1456, Radius 11 bzw. 10 px) durch den 25×25-Median ersetzt; dann wie oben |
| `kueste` | C02 | 3002 | 18:12:01 | `01a15f3b-9c60-74b3-9768-5b18f205db45` | a quiet coastline in warm evening light, calm sea, low sun near the horizon | wie oben |
| `duenen` | C04 | 3004 | 18:12:01 | `01a15f3b-9c62-7810-963b-3cd699175558` | smooth sand dunes under a pale blue dusk sky | wie oben |
| `see` | C05 | 3005 | 18:12:12 | `01a15f3b-d6f4-7693-ac3a-08cffb6bde92` | a misty lake at blue hour with a distant tree line | wie oben |
| `wueste` | C08 | 3008 | 18:12:11 | `01a15f3b-e179-7f70-9d80-0c9b92fdd366` | desert dunes with long soft shadows at sunset, warm sky | wie oben; 4:3-Ausschnitt x = 200 (Abendlicht links bleibt im Bild) |
| `berge` | C09 | 3009 | 18:12:24 | `01a15f3c-0842-7cc0-8eaf-588d5db13555` | layered mountain ridges in blue haze at dawn | wie oben |
| `strand` | C10 | 3010 | 18:12:23 | `01a15f3c-0a23-7341-a59c-1098033cff31` | a calm beach at twilight, wet sand reflecting the sky | wie oben |
| `glas` | D08 | 4008 | 18:12:54 | `01a15f3c-6a2c-7a01-8e52-420f26707f69` | layered translucent frosted glass planes in grey-blue | wie oben; **Nachkörnung** gegen Banding (Quelle 31,2 %) |

Alle Bilder wurden im Wallpaper-Test bei 100 % auf erfundene Wasserzeichen
und Oberflächen geprüft; keines der 16 ist betroffen.

## Logo-Fassungen

Entsprechen den gewählten Kandidaten L-A01-L1, L-A01-L2, L-A01-L3 und
L-B03-L1, aber neu gesetzt (nicht die Testdateien übernommen): Abstand
unten 7 % der Bildhöhe statt 3 % (Platz für das untere Panel), Wasserzeichen
1,15:1 statt 1,22:1 und entsättigt (mit Weiß) statt mit gesättigter
Grundfarbe aufgehellt.

| Datei (je Größe) | Grundbild | Logo |
|---|---|---|
| `querencia-tiefblau-logo[-4x3].png` | `tiefblau` | oranges Q, Höhe 4 % der Bildhöhe, rechts 3 % der Breite und unten 7 % der Höhe frei |
| `querencia-tiefblau-wortmarke[-4x3].png` | `tiefblau` | wie `-logo`, dazu die Wortmarke „Querencia Desktop“ in Weiß (Helligkeit unter dem Logo L ≈ 19 < 140) |
| `querencia-tiefblau-wasserzeichen[-4x3].png` | `tiefblau` | großes Q Ton in Ton, Höhe 55 % der Bildhöhe, Mitte bei 70 % der Breite, senkrecht mittig, mit Weiß aufgehellt bis WCAG-Kontrast 1,15:1; Symbolspalte links und Panel-Zone unten frei |
| `querencia-bernstein-logo[-4x3].png` | `bernstein` | wie `querencia-tiefblau-logo` |

Bilder mit Logo oder Wortmarke unterliegen der Markenregel (siehe Lizenz).
