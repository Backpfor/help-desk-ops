# Kategorie-Übersicht – Störungstypen

Grundlage für die Buchungszuordnung. Jeder Fall wird einer Kategorie zugeordnet.

---

## 1. VMS / QVMS – Software

Probleme mit der Videomanagementsoftware.

| Beispiele | HW/SW-Feld |
|-----------|-----------|
| Dienste stürzen ab, starten nicht | `VMS-Software` |
| Login-Fehler, API-Fehler | `QVMS` |
| Konfigurationsänderungen | `QVMS` |
| QVMS-Update / Migration | `QVMS` |
| LidlAPI-Fehler | `Server/QVMS` |

---

## 2. Kamera / Decoder

Probleme mit Videogeräten vor Ort.

| Beispiele | HW/SW-Feld |
|-----------|-----------|
| Kein Bild auf Monitor / Eingangsbildschirm | `Decoder` |
| Kamera offline / nicht erreichbar | `Camera` |
| Netzwerkkonfiguration Kamera | `Camera/Network` |
| Decoder-Einstellungen | `Decoder` |

---

## 3. Server

Probleme mit dem Filial- oder Zentralserver.

| Beispiele | HW/SW-Feld |
|-----------|-----------|
| Server nicht erreichbar (RDP) | `Server` |
| IPMI nicht erreichbar | `Server` |
| Server nicht migriert | `Server/QVMS` |
| Dienste auf Server ausgefallen | `Server` |

---

## 4. Netzwerk / Konnektivität

Verbindungsprobleme zur Filiale oder zu Geräten.

| Beispiele | HW/SW-Feld |
|-----------|-----------|
| Keine Verbindung zur Filiale | `Network` |
| VPN-Probleme | `Network` |
| IP-Konfiguration | `Network` |

---

## 5. Benutzerverwaltung / Zugänge

Benutzer- und Rechteverwaltung.

| Beispiele | HW/SW-Feld |
|-----------|-----------|
| Login nicht möglich | `QVMS` |
| Benutzerrechte anpassen | `QVMS` |
| Passwort zurücksetzen | `QVMS` |
| Neuen Benutzer anlegen | `QVMS` |

---

## 6. Hardware vor Ort

Physische Geräteprobleme.

| Beispiele | HW/SW-Feld |
|-----------|-----------|
| Server ohne Strom / nicht hochgefahren | `Server/HW` |
| Kabelverbindungen prüfen | `HW` |
| NVR / DVR defekt | `NVR` / `DVR` |

---

## 7. Sonstiges / Dienstleistung

Aufgaben ohne direkten Störungscharakter.

| Beispiele | HW/SW-Feld |
|-----------|-----------|
| Audit / Prüfung auf Anfrage | nach System |
| Schulung / Anleitung | nach System |
| Dokumentation erstellen | – |
