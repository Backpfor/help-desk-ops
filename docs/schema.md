# Buchungsschema

## Format

```
[Länderkürzel]|[Filialnummer / WH Name / FILLER]|[Wie?]|[Customer/Errichter]|[HW/SW]|[Problem]|[Lösungsweg -> Lösung]|[Fazit]|[AU/Betreff]
```

## Regeln

| Feld | Regel |
|------|-------|
| Filialnummer | Fehlt → `FILLER` |
| Warenlager | → `WH [Name]` |
| Wie? | `Phone` / `Email` / `Onsite` |
| Kunde/Errichter | `Lidl/[Firma]` · `Primark/[Firma]` · nur `Lidl` · Telefonnummer |
| Lösungsweg | Schritte mit `->` trennen |
| Sprache | DE → Deutsch · FR → Français · alle anderen → Englisch |
| Mail-Betreff | Am Ende in `"..."` · fehlt → `"FILLER BETREFF"` |

## Beispiele

**Email (DE)**
```
DE|0921|Email|Lidl/Solid System|VMS-Software|VMS-Dienste stürzen ab|Verbindung auf Server -> Prüfen VMS Logs -> Neuinstallation Dienste -> Kunde informiert|Problem behoben|"Kamera Probleme in Filiale 0921"
```

**Phone (EN)**
```
IE|0123|Phone|Lidl/Seakal|Decoder|No picture on entry screen|Connect to store server -> Connect to decoder -> Check settings -> Adjust network configuration|Waiting for feedback
```

**Phone – Nummer statt Firma (EN)**
```
RO|FILLER|Phone|Lidl/+40 730 002 808|Client/QVMS|QVMS update needed|Checked client -> Installer sent credentials -> Connected -> QVMS installed|System OK
```
