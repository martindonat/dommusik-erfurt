# Webseite der Dommusik Erfurt und des Fördervereins

## Einleitung

Die Webseite ist erstellt mit [Hugo](https://gohugo.io/) und wird hier mit Git und Github verwaltet.
Das Deployment läuft automatisch mittels Github Actions. Nächtlich läuft das Skript `Calendar_UpdateScript_from_csv.py`,
um die angezeigten Termine ggf. zu aktualisieren. Die Termine sind in `Kalender_Termine.csv` hinterlegt.

## Workflow Kalender

Die Termine können in der Datei `Kalender_Termine.ods` leicht mittels LibreOffice Calc oder
MS Office Excel gepflegt werden. Anschließend wird die Datei als CSV abgespeichert. Das Skript
liest die CSV-Datei, nicht ODS. Das Format der einzelnen Spalten muss eingehalten werden.

Das Skript sortiert die Termine automatisch nach Datum und löscht vergangene Termine raus. Sie müssen
also nicht manuell aus der CSV gelöscht werden. Es werden automatisch Icons vergeben: Eine Kirche bei Gottesdiensten,
ein Icon aus drei Personen für Chorkonzerte und eine Note für alle anderen. Die Vergabe funktioniert über
eine Stichwortsuche im Beschreibungstext.

Die Datei, die die dargestellten Termine enthält, ist `data/three.yml`.

## Credits

Die Webseite benutzt das [Spectral-Theme](https://github.com/sbruder/spectral/tree/master) - danke an Simon Bruder.
Einige Änderungen und Erweiterungen wurden umgesetzt, jedoch nicht systematisch, mal im Theme, mal in den
eigenen Dateien.

## Contact

Please don't hesitate to contact me if there are any questions or legal concerns.
