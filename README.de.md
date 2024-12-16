[English README](README.md)

# Installation des Systems auf einem neuen Computer

Diese Anleitung führt Sie durch die Installation des Systems auf einem neuen Computer. Alle Tests wurden auf Windows-Systemen durchgeführt; eine Anleitung für Linux könnte folgen.

## Schritt 1: Dieses Repository klonen

Klonen Sie dieses Repository auf Ihre Festplatte. Für Demonstrationszwecke nehmen wir an, dass der Pfad `C:/IOT-PlantWatering` lautet. Ersetzen Sie dies durch den von Ihnen gewählten Pfad. Sie erhalten eine `.env`-Datei von einer vertrauenswürdigen Quelle. Platzieren Sie die `.env`-Datei im Stammverzeichnis des Projekts. Weiter unten in dieser Anleitung finden Sie eine Übersicht der Verzeichnisstruktur. Da alles lokal ausgeführt wird, können Sie die Werte in Ihrer `.env`-Datei sicher ändern. Dies wird jedoch nicht empfohlen, da einige Werte hartcodiert sein könnten, was zu Fehlern führen kann.

## Schritt 2: Benötigte Programme installieren

Es wird vorausgesetzt, dass Python bereits auf Ihrem Computer installiert ist. Falls nicht, installieren Sie Python.

### Schritt 2.1: VS Code installieren

VS Code wird verwendet, um Dateien zu bearbeiten/auszuführen, und unterstützt alle verwendeten Dateiformate. Sie können jedoch jeden beliebigen Editor verwenden.

### Schritt 2.2: Docker installieren

Docker wird verwendet, um Grafana und InfluxDB bereitzustellen. Wir haben [Docker Desktop](https://www.docker.com/products/docker-desktop/) verwendet. Installieren Sie Docker und erstellen Sie ein Konto bzw. melden Sie sich an. Alles, was für Grafana und InfluxDB benötigt wird, wird später automatisch eingerichtet.

### Schritt 2.3: `python-dotenv` und `influxdb-client` für die Datensimulation installieren

Öffnen Sie das Verzeichnis `scripts` (entweder in VS Code oder über die Eingabeaufforderung) und installieren Sie die benötigten Module mit den folgenden Befehlen:

```bash
pip install python-dotenv
pip install influxdb-client
```

(Dieser Schritt kann übersprungen werden, wenn echte Sensordaten verfügbar sind.)

## Schritt 3: Erste Inbetriebnahme

Öffnen Sie die Eingabeaufforderung und navigieren Sie zu `C:/IOT-PlantWatering`. Führen Sie den Befehl `docker-compose up -d` aus, nachdem Sie sichergestellt haben, dass Docker Desktop läuft. Alternativ können Sie die Datei `start-docker.bat` durch Doppelklicken ausführen. Docker sollte nun die notwendigen Ressourcen für InfluxDB und Grafana installieren. Dies kann einige Zeit in Anspruch nehmen.

### Schritt 3.1: Überprüfen von InfluxDB

Nach der Einrichtung öffnen Sie einen Browser Ihrer Wahl und navigieren zu [http://localhost:8086/](http://localhost:8086/). Dies sollte die InfluxDB-Benutzeroberfläche anzeigen. Die Zugangsdaten können Sie Ihrer `.env`-Datei entnehmen.

#### Schritt 3.1.1: Sicherstellen, dass es funktioniert

Navigieren Sie in der InfluxDB-Benutzeroberfläche zu **Load Data -> API Tokens**. Erstellen Sie einen neuen API-Token oder klonen Sie den Admin-Token. Kopieren Sie den Token und fügen Sie ihn in Ihrer `.env`-Datei unter `INFLUXDB_API_TOKEN=token` ein. Stellen Sie sicher, dass keine Leerzeichen enthalten sind. Nach diesem Schritt können Sie das Skript `influx_data_simulator.py` im Verzeichnis `scripts` ausführen. Nutzen Sie dazu entweder VS Code oder die Eingabeaufforderung. Warten Sie einige Minuten und navigieren Sie zurück zur InfluxDB-Oberfläche. Gehen Sie zu **Data Explorer** und erstellen Sie eine neue Abfrage, indem Sie `iot-data` als Bucket und `plant_data` als Filter auswählen. Klicken Sie auf "Submit"; die Daten sollten in der Graph-Ansicht angezeigt werden. Sie können mit der Maus über die Punkte fahren, um die eingefügten Daten anzuzeigen.

### Schritt 3.2: Überprüfen von Grafana

Navigieren Sie in Ihrem Browser zu [http://localhost:3000/](http://localhost:3000/). Dies sollte die Grafana-Benutzeroberfläche anzeigen. Die Zugangsdaten lauten standardmäßig `admin` für Benutzername und Passwort.

#### Schritt 3.2.1: Verbindung zwischen Grafana und InfluxDB einrichten

Navigieren Sie in der Grafana-Oberfläche zu **Connections -> Data sources** und klicken Sie auf **Add data source**. Wählen Sie aus der Liste `InfluxDB` aus. Richten Sie die Datenquelle mit den folgenden Parametern ein:

| Parameter          | Wert                                           |
|--------------------|------------------------------------------------|
| Name               | InfluxDB                                       |
| Query Language     | Flux                                           |
| URL                | http://influxdb:8086                          |
| Organization       | Name Ihrer Organisation in Influx (Standard: iot) |
| Token              | Der Token aus Schritt 3.1.1                   |
| Min time interval  | 10s                                            |

Die restlichen Einstellungen können unverändert bleiben. Klicken Sie auf **Save & Test**; eine Erfolgsbenachrichtigung sollte angezeigt werden.

#### Schritt 3.2.2: Ein Dashboard einrichten

Um Daten in Grafana anzuzeigen, wird ein Dashboard benötigt. Gehen Sie zu **Dashboards** und klicken Sie auf **New**, dann wählen Sie **Import**. Importieren Sie die `.json`-Datei aus `IOT-PlantWatering/provisioning/dashboards`. Klicken Sie auf "Import". Danach sollte ein Dashboard mit dem Namen "Plant Data Display" erscheinen. Öffnen Sie es durch einen Klick darauf.

## Fehlerbehebung

- **Das Python-Skript funktioniert nicht:** Stellen Sie sicher, dass alle benötigten Bibliotheken mit `pip` installiert sind. Überprüfen Sie außerdem, ob der richtige Token in Ihrer `.env`-Datei gesetzt ist, da dieser zur Autorisierung beim Schreiben von Daten verwendet wird.
- **Grafana/InfluxDB laden nicht:** Überprüfen Sie, ob Docker gestartet ist.
- **Docker funktioniert nicht:** Stellen Sie sicher, dass Docker Desktop läuft.
- **Die Datenquelle funktioniert nicht:** Überprüfen Sie, ob Sie die richtigen Werte bei der Einrichtung verwendet haben.
- **Ich sehe keine Daten in Grafana:** Nutzen Sie die InfluxDB-Oberfläche, um sicherzustellen, dass tatsächlich Daten in der Datenbank vorhanden sind. Nutzen Sie den Simulator, um Daten zu simulieren.
- **Daten sind in der Datenbank und die Verbindung funktioniert, aber ich sehe nichts in Grafana:** Öffnen Sie in Ihrem Dashboard die drei Punkte oben rechts bei einer der Zeitreihen und klicken Sie auf **Edit**. Stellen Sie sicher, dass `InfluxDB` als Datenquelle ausgewählt ist und die Abfrage korrekt ist. Stellen Sie die Anzeigezeit auf "Last 15 minutes" ein und versuchen Sie, manuell zu aktualisieren. Überprüfen Sie auch, ob im Textfeld oben ein Pflanzenname eingegeben ist. Wenn nicht, geben Sie zum Testen "Efeutute" ein.

Ihre Verzeichnisstruktur nach dem ersten Start von Docker sollte wie folgt aussehen:

```
iot-plantwatering/
├── .env                         # Umgebungsvariablen für das Projekt
├── .gitignore                   # Ignorierte Dateien und Verzeichnisse
├── README.md                    # Dokumentation des Projekts
├── docker-compose.yml           # Docker Compose-Konfiguration
├── scripts/                     # Verzeichnis für das Simulationsskript
│   └── influx_data_simulator.py # Skript zur Pflanzendatensimulation
├── provisioning/                # Grafana-Provisionierungsdateien
│   ├── dashboards/              # Verzeichnis für Dashboards
│   │   ├── dashboards.yml       # Konfigurationsdatei für Dashboards
│   │   └── dashboard.json       # Beispiel eines exportierten Dashboards
├── data/                        # Persistente Datenspeicherung für Grafana und InfluxDB
│   ├── grafana/                 # Persistente Grafana-Daten
│   └── influxdb/                # Persistente InfluxDB-Daten
```

## Hardware verstehen
Die verwendete Hardware wird dokumentiert. **In Arbeit.**

## Nach der Installation

Nach Änderungen am Dashboard, die Sie veröffentlichen möchten, klicken Sie auf **Share -> Export -> Save to file** und erstellen Sie eine neue `.json`-Datei im Verzeichnis `IOT-PlantWatering/provisioning/dashboards`.

Alle Änderungen, die Sie vornehmen, sind nur lokal! Daten auf Ihrem Computer werden nicht geteilt, ebenso wenig Dashboards oder Datenquellen.

Eine Möglichkeit, Datenquellen und Dashboards automatisch zu importieren, ist geplant, falls am Ende des Projekts genug Zeit bleibt.

## Zukünftige Pläne

- **Dokumentation des gesamten Projekts** - **In Arbeit**
- **Erstellung einer neuen Benutzeroberfläche in Grafana** - **In Arbeit**
- **Hilfe durch KI einholen** - **Geplant**
- **Unterstützung mehrerer Pflanzen** - Eine Anzeige für mehrere Pflanzen ist geplant; Daten von mehreren Sensoren zu erhalten, ist derzeit nicht geplant.
- **Verwendung eines besseren Sensors** - **In Arbeit**

