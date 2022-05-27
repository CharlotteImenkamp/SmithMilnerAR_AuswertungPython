# Auswertung_Python

Die Anwendung beinhaltet alle erforderlichen Skripte zur Auswerung der Daten.

## Ordner
- "auswertung_python\Data":  
	erforderliche .json sowie .xlsx Dateien zur Analyse
	Jedem neuen Datensatz muss eine neue id zugeordnet werden, welche noch nicht in der Ordnerstruktur vorkommt. 
	Um einen neuen Datensatz einer zur Auswertung hinzuzufügen, muss ein neuer Unterordner User*id* (auswertung_python\Data\User*id) 
	erstellt werden und die auszuwertenden Dateien darin gespeichert werden. 
	Die erforderlichen Dateien sind die Ausgaben der Unity-Anwendung, welche im Windows-Device-Portal zugänglich sind.
	Die Namen der Dateien sind: EndObjectLocations*id*, HeadDataLocations*id*, HeadDataPrices*id*, MovingObjectLocations*id*, StartLocationPrices*id* 
	und StartObjectLocations*id*. Im letzten Schritt muss die ID in der main Datei zur Variablen "allIDs" (Zeile 16) hinzugefügt werden.
	
	
- "Results": Ergebnisse der Analyse im .png oder .xlsx Format. Die Dateien werden durch die Anwendung erstellt

## Skripte
- Load:
    - Laden der Start- und Endpositionen der Gegenstände zur Berechnung des absoluten und relativen Fehlers
- AbsoluteError: 
    - Bilder der Positionierung jedes Probanden
    - Absolute Fehlerdistanzen, sowie deren Mittelwerte und Standardabweichungen
- RelativeError:
    - Diagram und direkte Nachbarn nach Voronoi (Ausgabe: Bild)
    - Diagram und direkte Nachbarn nach Delaunay (Ausgabe: Bild)
    - relativer Fehler mittels Quadrantenvergleich (Ausgabe: Excel-Datei)
- Rotations / Times: 
    - Unterschiede der Rotation und Zeiten
    - Ergebnisse in Excel-Datei
- ObjectMovement / HeadDirections: 
    - Lesen und Visualisieren der entsprechenden .json Dateien 
- Testbatterie: 
    - Berechnung von Mittelwert und Standardabweichungen der neuropsychologischen Testbatterie
    - nutzt Klasse "NeuroData" 
    - Visualisierung der Gruppen durch Boxplots





