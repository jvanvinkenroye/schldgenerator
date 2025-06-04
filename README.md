# SchildGenerator

Ein Python-Tool zur automatischen Generierung von Namensschildern aus einer SVG-Vorlage.

## Beschreibung

SchildGenerator ist ein Python-Programm, das eine SVG-Vorlage verwendet, um mehrere Namensschilder zu generieren. Es liest Namen aus einer Textdatei und erstellt ein SVG-Dokument mit den Namen in einem Raster-Layout.

## Funktionen

- Generiert Namensschilder aus einer SVG-Vorlage
- Liest Namen aus einer Textdatei
- Konfigurierbare Raster-Layout (Anzahl der Spalten und Zeilen)
- Anpassbare Canvas-Größe und Schild-Dimensionen
- Automatische Berechnung der Abstände zwischen den Schildern

## Voraussetzungen

- Python 3.6 oder höher
- Keine externen Bibliotheken erforderlich (verwendet nur Standardbibliotheken)

## Installation

1. Klonen Sie das Repository oder laden Sie die Dateien herunter
2. Stellen Sie sicher, dass Python 3.6 oder höher installiert ist

## Konfiguration

Die Konfiguration erfolgt über die Datei `config.json`:

```json
{
    "vorlage_svg": "vorlage.svg",
    "namen_datei": "namen.txt",
    "ausgabe_svg": "ausgabe.svg",
    "canvas_breite": 700,
    "canvas_hoehe": 400,
    "spalten": 4,
    "zeilen": 10,
    "schild_breite": 135.94,
    "schild_hoehe": 29.82
}
```

### Konfigurationsparameter

- `vorlage_svg`: Pfad zur SVG-Vorlage
- `namen_datei`: Pfad zur Textdatei mit den Namen (ein Name pro Zeile)
- `ausgabe_svg`: Pfad zur Ausgabe-SVG-Datei
- `canvas_breite`: Breite des Canvas in Pixeln
- `canvas_hoehe`: Höhe des Canvas in Pixeln
- `spalten`: Anzahl der Spalten im Raster
- `zeilen`: Anzahl der Zeilen im Raster
- `schild_breite`: Breite eines einzelnen Schildes in Pixeln
- `schild_hoehe`: Höhe eines einzelnen Schildes in Pixeln

## Verwendung

1. Erstellen Sie eine SVG-Vorlage mit einem Schild-Design
2. Erstellen Sie eine Textdatei mit den Namen (ein Name pro Zeile)
3. Passen Sie die Konfiguration in `config.json` an
4. Führen Sie das Programm aus:

```bash
python schildGenerator.py
```

## SVG-Vorlage

Die SVG-Vorlage sollte folgende Eigenschaften haben:

- Ein Layer mit der ID "layer1"
- Eine Gruppe innerhalb des Layers, die als Vorlage für die Schilder dient
- Text-Elemente mit tspan-Elementen, die den Platzhalter-Text enthalten

## Beispiele

### Vorlage-SVG

Die Vorlage-SVG sollte ein einzelnes Schild-Design enthalten, das als Vorlage für alle generierten Schilder dient.

### Namen-Datei

Die Namen-Datei sollte eine Liste von Namen enthalten, ein Name pro Zeile:

```
Max Mustermann
Anna Schmidt
...
```

## Lizenz

/* This program is free software. It comes without any warranty, to
     * the extent permitted by applicable law. You can redistribute it
     * and/or modify it under the terms of the Do What The Fuck You Want
     * To Public License, Version 2, as published by Sam Hocevar. See
     * http://www.wtfpl.net/ for more details. */

## Autor

Jan Vanvinkenroye <jan@vanvinkenroye.de>

