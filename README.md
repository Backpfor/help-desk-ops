# help-desk-ops

Repository zur Verwaltung von Help-Desk-Buchungen (Lidl / Primark IT-Support).

## Struktur

```
help-desk-ops/
├── bookings/          # Buchungseinträge nach Monat (YYYY-MM/bookings.md)
├── templates/         # Vorlagen pro Buchungstyp (phone / email / onsite)
├── docs/              # Buchungsschema und Referenz
└── scripts/           # Hilfsskripte
```

## Schnellstart

1. Rohnotizen an Claude schicken
2. Formatierte Buchung nach [docs/schema.md](docs/schema.md) erhalten
3. Buchung in `bookings/YYYY-MM/bookings.md` eintragen
