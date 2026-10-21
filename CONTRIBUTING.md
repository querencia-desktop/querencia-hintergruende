# Mitmachen bei Querencia Hintergründe

Danke für das Interesse. Querencia ist in einer frühen Alpha-Phase; bitte
rechne mit Rückfragen und langsamen Antworten.

## Fehler melden

In der gemeinsamen Meldestelle:
<https://github.com/querencia-desktop/querencia/issues/new/choose>.

**Sicherheitslücken nicht öffentlich melden:** siehe [SECURITY.md](SECURITY.md).

## Vor einem Pull Request

- Die Bilder entstehen reproduzierbar mit `werkzeug/erzeugen-02.py` (siehe
  README, „Prüfen und neu erzeugen“). Erzeugte Bilder nie von Hand
  nachbearbeiten.

Checkliste:

- [ ] Prüfung: `python3 -I werkzeug/erzeugen-02.py --pruefen` (Exit 0)
- [ ] Lizenzkopf bzw. Lizenzangabe: neue Dateien stehen unter der Lizenz des
      Repos; Fremdmaterial mit Herkunft und Lizenz in `COPYRIGHT`
- [ ] Keine Geheimnisse (Schlüssel, Passwörter, Tokens), keine privaten Pfade
      oder Adressen
- [ ] `CHANGELOG.md` ergänzt; Unfertiges ist als unfertig gekennzeichnet

Über Merge und Release entscheiden die Betreuer des Projekts.

## Regeln für den Code

1. Vorab ein Issue, wenn es um mehr als eine kleine Korrektur geht –
   besonders bei Bedienung und Optik. Maßstab ist GNOME 2 / Ubuntu 10.04 (Standardhintergründe).
2. Zweig von `main`, kleine, thematisch geschlossene Commits
   (Conventional Commits).
3. App-IDs, Desktop-Dateien und D-Bus-Namen folgen `org.querencia.*`.
4. Keine fest verdrahteten Pfade (`/home/<name>`, `~/projects`, `~/opt`,
   `target/`), keine privaten Adressen in Code, Tests und Doku.
5. Symbole: nie 48×48 zusammen mit `scalable` installieren (GTK-4.22-Absturz,
   siehe Regel M in `querencia-packaging`).
6. Neue Abhängigkeiten nur mit Begründung; die Lizenz muss zu CC-BY-SA-4.0
   passen und in `COPYRIGHT` stehen. Nichtfreie Anteile (z. B. UnRAR) sind
   ausgeschlossen.
7. Quellcode und Texte ohne Fremdmaterial: keine Übernahme aus den Vorbild­
   programmen (siehe README).

## Lizenz der Beiträge

Mit einem Beitrag stimmst du zu, dass er unter der Lizenz des jeweiligen Teils
veröffentlicht wird: Bilder und Originale unter CC-BY-SA-4.0, die Werkzeuge in
`werkzeug/` unter GPL-3.0-or-later (siehe COPYRIGHT). Du versicherst, dass du
ihn selbst geschrieben hast oder die Lizenz des Ursprungs es erlaubt.
