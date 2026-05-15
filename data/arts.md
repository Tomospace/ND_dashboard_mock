# ARTs — Agile Release Trains (mock data)
#
# Format: jeden ART = jeden blok mezi `---` čarami.
# Frontmatter klíče (všechny povinné):
#   art_key      — interní klíč (formát TYM-XXX)
#   art_name     — celý název včetně prefixu a vlastníka
#   short_name   — krátký kód (do hlavičky karet)
#   team_count   — počet týmů v ARTu
#   tempo_hours  — celkový součet vykázaných hodin (libovolné float číslo)
#
# Smaž / přidej bloky podle potřeby. UI po reloadu prohlížeče zobrazí změnu.

---
art_key: TYM-101
art_name: "[ART - IT] IT Platform | Novák Jan"
short_name: IT
team_count: 9
tempo_hours: 24560.5
---

---
art_key: TYM-102
art_name: "[ART - DC] Digital Channels | Dvořák Petr"
short_name: DC
team_count: 7
tempo_hours: 11240.0
---

---
art_key: TYM-103
art_name: "[ART - MM Art] Mass Market Art | Procházková Lenka"
short_name: MM
team_count: 5
tempo_hours: 8120.75
---

---
art_key: TYM-104
art_name: "[ART - CS] Customer Service | Kučera Tomáš"
short_name: CS
team_count: 4
tempo_hours: 3210.0
---

---
art_key: TYM-105
art_name: "[ART - B2B] Business to Business | Veselá Klára"
short_name: B2B
team_count: 4
tempo_hours: 2980.5
---

---
art_key: TYM-106
art_name: "[ART - NTW] Network | Horák Martin"
short_name: NTW
team_count: 3
tempo_hours: 1420.25
---

---
art_key: TYM-107
art_name: "[ART - FIX] Maintenance & Hotfixes | Beneš Aleš"
short_name: FIX
team_count: 2
tempo_hours: 1850.0
---
