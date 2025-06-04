import xml.etree.ElementTree as ET
import copy
import logging
import json
from typing import List, Optional

# Logging Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SchildGenerator:
    """Klasse zur Generierung von Namensschildern aus einer SVG-Vorlage."""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialisiert den SchildGenerator mit Konfigurationswerten.
        
        Args:
            config_file: Pfad zur Konfigurationsdatei
        """
        self.config = self._load_config(config_file)
        self.namespaces = {'svg': 'http://www.w3.org/2000/svg'}
        
    def _load_config(self, config_file: str) -> dict:
        """Lädt die Konfiguration aus einer JSON-Datei."""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Konfigurationsdatei {config_file} nicht gefunden. Verwende Standardwerte.")
            return {
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

    def _calculate_spacing(self) -> tuple:
        """Berechnet die Abstände zwischen den Schildern.

        Wenn nur eine Spalte oder Zeile vorhanden ist, wird der jeweilige
        Abstand zu 0 gesetzt, um eine Division durch Null zu vermeiden.
        """

        spalten = self.config.get('spalten', 1)
        zeilen = self.config.get('zeilen', 1)

        if spalten < 1 or zeilen < 1:
            raise ValueError("'spalten' und 'zeilen' müssen mindestens 1 sein")

        if spalten == 1:
            horizontal_abstand = 0
        else:
            horizontal_abstand = (
                self.config['canvas_breite']
                - spalten * self.config['schild_breite']
            ) / (spalten - 1)

        if zeilen == 1:
            vertical_abstand = 0
        else:
            vertical_abstand = (
                self.config['canvas_hoehe']
                - zeilen * self.config['schild_hoehe']
            ) / (zeilen - 1)

        return horizontal_abstand, vertical_abstand

    def _find_template_group(self, layer: ET.Element) -> Optional[ET.Element]:
        """Findet die erste Gruppe als Vorlage."""
        groups = layer.findall('svg:g', self.namespaces)
        if not groups:
            return None
        return groups[0]  # Verwende die erste Gruppe als Vorlage

    def _read_names(self) -> List[str]:
        """Liest die Namen aus der Datei."""
        try:
            with open(self.config['namen_datei'], "r", encoding="utf-8") as f:
                return [zeile.strip() for zeile in f if zeile.strip()]
        except FileNotFoundError:
            logger.error(f"Namensdatei {self.config['namen_datei']} nicht gefunden!")
            raise

    def generate(self) -> None:
        """Generiert die Namensschilder aus der Vorlage."""
        try:
            # SVG einlesen
            baum = ET.parse(self.config['vorlage_svg'])
            wurzel = baum.getroot()
            
            # Layer finden
            layer = wurzel.find('.//svg:g[@id="layer1"]', self.namespaces)
            if layer is None:
                raise ValueError("Layer 'layer1' nicht gefunden!")
            
            # Vorlage-Gruppe finden
            original_group = self._find_template_group(layer)
            if original_group is None:
                raise ValueError("Keine Gruppen in der SVG-Datei gefunden. Bitte stellen Sie sicher, dass die Vorlage SVG-Elemente enthält.")

            # Namen einlesen
            namen = self._read_names()
            
            # Abstände berechnen
            horizontal_abstand, vertical_abstand = self._calculate_spacing()

            # Bestehende Gruppen löschen (außer Vorlage)
            for g in layer.findall('svg:g', self.namespaces):
                if g is not original_group:
                    layer.remove(g)

            # Schilder erzeugen
            for i, name in enumerate(namen):
                spalte = i % self.config['spalten']
                reihe = i // self.config['spalten']
                
                if reihe >= self.config['zeilen']:
                    logger.warning(f"⚠️  '{name}' wurde nicht eingefügt (zu viele Namen für das Raster).")
                    continue

                x = spalte * (self.config['schild_breite'] + horizontal_abstand)
                y = reihe * (self.config['schild_hoehe'] + vertical_abstand)

                neue_gruppe = copy.deepcopy(original_group)
                neue_gruppe.attrib['transform'] = f"translate({x:.2f},{y:.2f})"

                # IDs löschen
                for elem in neue_gruppe.iter():
                    if 'id' in elem.attrib:
                        del elem.attrib['id']

                # Name einfügen
                for text in neue_gruppe.findall('.//svg:text', self.namespaces):
                    for tspan in text.findall('svg:tspan', self.namespaces):
                        tspan.text = name

                layer.append(neue_gruppe)

            # Vorlage-Gruppe entfernen
            layer.remove(original_group)

            # SVG speichern
            baum.write(self.config['ausgabe_svg'], encoding="utf-8", xml_declaration=True)
            logger.info(f"✅ {len(namen)} Schilder wurden in '{self.config['ausgabe_svg']}' gespeichert.")

        except Exception as e:
            logger.error(f"Fehler beim Generieren der Schilder: {str(e)}")
            raise

if __name__ == "__main__":
    generator = SchildGenerator()
    generator.generate()
