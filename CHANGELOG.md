# Änderungen – querencia-hintergruende

## 0.2 – 2026-10-21

Erste Fassung als eigenes Datenrepo (QD-093, Entscheidung des Besitzers
21.10.2026 19:50). Übernommen aus `querencia-runtime`, Zweig
`hintergruende-0.2`, Commit `370eddf`.

- 16 Flux-Bilder (12 Motive, dazu `tiefblau-logo`, `-wortmarke`,
  `-wasserzeichen` und `bernstein-logo`) in 2560×1440 und 4:3: 32 Dateien,
  104 MB, `data/hintergruende/SHA256SUMS`. Standardbild `tiefblau`.
- 3840 und 1920 nicht im Repo, mit `werkzeug/erzeugen-02.py --alle`
  bit-gleich erzeugbar (`werkzeug/SHA256SUMS-alle`).
- `quellen/`: die 13 fal-Originale unverändert mit C2PA.
- Lizenz CC-BY-SA-4.0 mit KI-Vorbehalt, Logo-Fassungen zusätzlich
  Markenregel; Werkzeuge GPL-3.0-or-later.
- `integration/0.2/`: Ablage `~/opt/querencia/hintergruende/<sha16>/` und
  Links in `~/.local/share/querencia/hintergruende/` (ohne sudo), Probe.
