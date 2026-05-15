# NDs — New Delivery issues (mock data)
#
# Každý ND = sekce začínající `## ND-XXXX: Název`.
# Pod ní YAML-style metadata + volitelné podsekce (### description,
# ### comments, ### timeline, ### apps, ### wiki, ### dod).
#
# Smaž / přidej sekce podle potřeby — UI po reloadu zobrazí změnu.
# Polopolní sekce mohou být úplně vynechány (vrátí prázdná data).

## ND-1001: Reorganizace billingového modulu pro tarify s rodinnou slevou

- status: Delivery
- assignee: Novák Jan
- created: 2026-01-14
- updated: 2026-05-10
- pi: PI3 2026
- wsjf: 12.5
- funnel: FUNNEL
- arts: IT, DC
- teams: TYM-211, TYM-212, TYM-301
- parent: PROJEKT-101
- description_length: 1850

### description
Implementace mechanismu pro automatické přepočítání měsíčního vyúčtování
u zákazníků, kteří přechází z individuálních tarifů na rodinné slevy.

**Cíle:**
- snížit počet manuálních zásahů customer care
- zkrátit reklamační okno na max. 3 pracovní dny
- pokrýt všechny aktuální produkty Mobilní hlas + Pevný internet

### comments
- 2026-05-08 | Dvořák Petr | Discovery fáze dokončena, čekáme na PreQS schválení.
- 2026-05-03 | Kučera Tomáš | RFO vytvořeno (RFO-2025-014), testing tým připraven.
- 2026-04-22 | Novák Jan | Lean BC schváleno board meetingem 2026-04-20.

### timeline
- 2026-01-14 | created | New
- 2026-02-05 | status | Discovery
- 2026-03-10 | status | PreQS
- 2026-04-15 | status | QS
- 2026-04-28 | status | Delivery

### apps
- AIP-12001 | Billing Core | impacted
- AIP-12002 | Customer Portal | impacted
- AIP-12340 | Tariff Catalogue | informed
- AIP-13002 | Reporting DWH | informed

### wiki
- url: https://confluence.example.com/x/ABCD01
- updated: 2026-04-30
- sections: 5

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: true
- figma_url: https://figma.com/file/MOCK-billing-flow
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 86.5
- score: 6

### deliverables
- BAN | BAN-30101 | RM business case rodinná sleva | Done | Nováková Eva | TYM-211
- ARCH | ARCH-30102 | Billing engine HLD update | Done | Svoboda Petr | TYM-211
- ARCH | ARCH-30103 | Migration strategy for legacy tarify | In Progress | Svoboda Petr | TYM-301
- QS  | QS-30104 | QS rozhodnutí — GO | Done | Veselý Jan | TYM-211
- DEV | DEV-30105 | Backend rodinný-tarif calculator | In Progress | Černý Pavel | TYM-211
- DEV | DEV-30106 | UI flow v Moje O2 | In Progress | Bílá Hana | TYM-301
- DEV | DEV-30107 | B2B portal pro family business plans | New | Bílá Hana | TYM-211
- TST | TST-30108 | Regression suite billing | New | Malý Tomáš | TYM-211

### tempo_roles
- Architekt | 145.5
- Business analytik | 92.0
- Vývojář | 380.0
- Tester | 56.5
- UX/WF | 28.0
- Systémový analytik | 48.0


## ND-1002: Nový landing page pro Moje O2 — variant testing

- status: Discovery
- assignee: Dvořák Petr
- created: 2026-02-20
- updated: 2026-05-12
- pi: PI3 2026
- wsjf: 9.0
- funnel: FUNNEL
- arts: DC, MM
- teams: TYM-301, TYM-302, TYM-401
- parent: PROJEKT-102
- description_length: 920

### description
A/B/C test 3 variant landing page pro hlavní vstup do samoobsluhy.
Cíl: zvýšit konverzi přihlášení nových zákazníků o min. 8 %.

### comments
- 2026-05-11 | Procházková Lenka | Návrhy variant B a C připraveny, A je current state.
- 2026-05-04 | Veselá Klára | UX research s 12 respondenty hotov, výstupy v Figmě.

### timeline
- 2026-02-20 | created | New
- 2026-03-01 | status | Discovery

### apps
- AIP-13550 | Moje O2 Frontend | impacted
- AIP-13551 | Identity Service | informed

### wiki
- url: https://confluence.example.com/x/ABCD02
- updated: 2026-05-05
- sections: 3

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: true
- figma_url: https://figma.com/file/MOCK-mojeo2-landing
- impacted_apps_exist: true
- arch_qs_exist: false
- ban_rm_exist: true
- discovery_tempo_hours: 42.0
- score: 4


## ND-1003: Self-care chat — integrace s LLM agentem

- status: PreQS
- assignee: Kučera Tomáš
- created: 2026-03-05
- updated: 2026-05-14
- pi: PI3 2026
- wsjf: 14.0
- funnel: FUNNEL
- arts: CS, IT
- teams: TYM-401, TYM-211
- parent: PROJEKT-103
- description_length: 2200

### description
Nasazení LLM-based chatbota do samoobsluhy Moje O2. Pokrytí 5 hlavních
scénářů: změna tarifu, dotaz na fakturu, reklamace, kontakt prodejny,
technická podpora pro internet doma.

**Bezpečnost:**
- žádný přístup k osobním údajům bez explicitní autorizace
- audit log všech interakcí
- fallback na lidského operátora po 3 nezdařených pokusech

### comments
- 2026-05-14 | Horák Martin | PreQS review naplánován na 2026-05-22.
- 2026-05-09 | Novák Jan | Architecture diagram aktualizován, přidána GDPR vrstva.
- 2026-04-30 | Veselá Klára | Lean BC: ROI očekávané 18 měsíců, schváleno.

### timeline
- 2026-03-05 | created | New
- 2026-03-18 | status | Discovery
- 2026-05-02 | status | PreQS

### apps
- AIP-14001 | Chat Frontend | impacted
- AIP-14002 | Customer Care BO | impacted
- AIP-14100 | LLM Gateway | impacted
- AIP-12001 | Billing Core | informed

### wiki
- url: https://confluence.example.com/x/ABCD03
- updated: 2026-05-12
- sections: 8

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: true
- figma_url: https://figma.com/file/MOCK-chat-llm
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 120.5
- score: 7

### deliverables
- BAN | BAN-30301 | RM use cases + GDPR review | Done | Černá Petra | TYM-401
- ARCH | ARCH-30302 | LLM gateway HLD | Done | Beran Jakub | TYM-211
- ARCH | ARCH-30303 | Fallback architecture | Done | Beran Jakub | TYM-401
- QS  | QS-30304 | QS rozhodnutí | In Progress | Veselý Jan | TYM-401
- DEV | DEV-30305 | LLM gateway integrace | New | Černý Pavel | TYM-211

### tempo_roles
- Business analytik | 52.0
- Architekt | 41.0
- UX/WF | 18.5
- Systémový analytik | 9.0


## ND-1004: B2B portál — export faktur do účetních systémů (ISDOC)

- status: New
- assignee: Veselá Klára
- created: 2026-04-10
- updated: 2026-05-13
- pi: PI3 2026
- wsjf: 6.5
- funnel: null
- arts: B2B, IT
- teams: TYM-501, TYM-211
- parent: PROJEKT-104
- description_length: 740

### description
Implementace exportu faktur ve formátu ISDOC 6.0.2 pro B2B zákazníky
s integrací do Pohoda, ABRA, Money S5 a Helios.

### comments
- 2026-05-13 | Novák Jan | Čeká na ART vyjádření IT, deadline 2026-05-20.

### timeline
- 2026-04-10 | created | New

### apps
- AIP-15001 | B2B Portal | impacted
- AIP-12001 | Billing Core | impacted

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: false
- ban_rm_exist: false
- discovery_tempo_hours: 8.0
- score: 2


## ND-1005: Optimalizace 5G pokrytí v hustých zónách Prahy

- status: Delivery
- assignee: Horák Martin
- created: 2025-11-12
- updated: 2026-05-09
- pi: PI3 2026
- wsjf: 11.0
- funnel: FUNNEL
- arts: NTW
- teams: TYM-601
- parent: PROJEKT-105
- description_length: 1340

### description
Doplnění 5G sites v lokalitách Karlín, Smíchov, Vršovice. Cíl: pokrytí
min. 95 % obytných ploch signálem ≥ -85 dBm.

### comments
- 2026-05-09 | Procházková Lenka | 8 z 12 sites instalováno, dokončení Q3 2026.
- 2026-04-15 | Kučera Tomáš | Stavební povolení získáno pro všechny lokality.

### timeline
- 2025-11-12 | created | New
- 2025-12-10 | status | Discovery
- 2026-02-20 | status | Delivery

### apps
- AIP-16001 | RAN Configuration | impacted
- AIP-16002 | Network Monitoring | informed

### wiki
- url: https://confluence.example.com/x/ABCD05
- updated: 2026-04-10
- sections: 12

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 210.0
- score: 6

### deliverables
- BAN | BAN-30501 | RM 5G dense urban coverage | Done | Nováková Eva | TYM-601
- ARCH | ARCH-30502 | RAN topology dense urban | Done | Beran Jakub | TYM-601
- QS  | QS-30503 | QS approval | Done | Veselý Jan | TYM-601
- DEV | DEV-30504 | RAN config rollout Praha 1-3 | Done | Krátký Lukáš | TYM-601
- DEV | DEV-30505 | RAN config rollout Praha 4-10 | In Progress | Krátký Lukáš | TYM-601
- TST | TST-30506 | Drive test centra Prahy | In Progress | Malý Tomáš | TYM-601
- RL  | RL-30507 | Commercial enablement | New | Horák Martin | TYM-601

### tempo_roles
- Architekt | 68.0
- Vývojář | 285.0
- Tester | 78.5
- Systémový analytik | 42.0
- Business analytik | 24.0


## ND-1006: Migrace SMS gateway na cloudovou platformu

- status: Discovery
- assignee: Novák Jan
- created: 2026-03-22
- updated: 2026-05-11
- pi: PI4 2026
- wsjf: 7.5
- funnel: FUNNEL
- arts: IT, NTW
- teams: TYM-212, TYM-601
- parent: PROJEKT-104
- description_length: 4120

### description
Stávající SMS gateway běží na on-prem infrastruktuře, která dosahuje EOL v Q4/2026.
Cílem je migrace na cloudovou platformu (AWS SNS / Azure Communication Services) s důrazem
na zachování compliance (GDPR, retention 6 měsíců) a redundance.

### apps
- AIP-17001 | SMS Gateway Core | impacted
- AIP-17002 | Notification Router | impacted
- AIP-12001 | Billing Core | informed

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 145.5
- score: 6

### deliverables
- BAN | BAN-30601 | Lean BC pro cloud migraci | Done | Nováková Eva | TYM-212
- ARCH | ARCH-30602 | HLD návrh hybridní topologie | In Progress | Svoboda Petr | TYM-212
- ARCH | ARCH-30603 | Failover & DR strategie | New | Svoboda Petr | TYM-601
- QS  | QS-30604 | Architecture QS rozhodnutí | New | Veselý Jan | TYM-212

### tempo_roles
- Architekt | 78.0
- Business analytik | 42.5
- UX/WF | 8.0
- Systémový analytik | 17.0


## ND-1007: Refactoring fakturačního modulu pro split-billing

- status: Canceled
- assignee: Dvořák Petr
- created: 2026-01-30
- updated: 2026-04-05
- pi: null
- wsjf: 0.0
- funnel: null
- arts: IT, DC
- teams: TYM-211
- parent: PROJEKT-101

### description
Původně plánovaný refactor pro podporu split-billingu (rozdělení účtu mezi více plátců).
Zrušeno v Q2/2026 — businessový sponsor stáhl požadavek po PreQS rozhodnutí (low ROI).

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: false
- impacted_apps_exist: false
- arch_qs_exist: false
- ban_rm_exist: true
- discovery_tempo_hours: 32.0
- score: 1


## ND-1008: Self-service onboarding pro firemní zákazníky

- status: New
- assignee: Veselá Klára
- created: 2026-04-25
- updated: 2026-05-08
- pi: PI4 2026
- wsjf: 8.0
- funnel: FUNNEL
- arts: B2B, DC
- teams: TYM-501, TYM-302
- parent: PROJEKT-103
- description_length: 980

### description
Umožnit B2B zákazníkům dokončit aktivaci služeb bez kontaktu s account managerem —
od KYC ověření přes digitální podpis až po nastavení administrátorských účtů.

### apps
- AIP-15001 | B2B Portal | impacted
- AIP-15002 | KYC Service | impacted
- AIP-13550 | Moje O2 Frontend | informed

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: false
- ban_rm_exist: false
- discovery_tempo_hours: 12.0
- score: 2


## ND-1009: Nová verze TV aplikace pro smart TVs (Samsung, LG)

- status: PreQS
- assignee: Procházková Lenka
- created: 2026-02-08
- updated: 2026-05-12
- pi: PI3 2026
- wsjf: 9.5
- funnel: FUNNEL
- arts: MM, IT
- teams: TYM-302, TYM-212
- parent: PROJEKT-102
- description_length: 6230

### description
Cílem je dodat novou verzi O2 TV aplikace pro smart TV platformy Samsung Tizen a LG webOS.
Klíčové novinky: hlasové ovládání, doporučovací engine na bázi sledovací historie,
podpora 4K HDR streamů a HbbTV 2.0 integrace.

### apps
- AIP-18001 | O2 TV Backend | impacted
- AIP-18002 | Recommendation Engine | impacted
- AIP-18003 | Smart TV App (Tizen) | impacted
- AIP-18004 | Smart TV App (webOS) | impacted

### wiki
url: https://confluence.cz.o2/display/ND/ND-1009
last_updated: 2026-05-09

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: true
- figma_url: https://figma.com/file/o2tv-smarttv-v2
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 312.0
- score: 8

### deliverables
- BAN | BAN-30901 | RM business case TV v2 | Done | Procházková Lenka | TYM-302
- ARCH | ARCH-30902 | HLD smart TV stack | Done | Beran Jakub | TYM-302
- ARCH | ARCH-30903 | Performance arch pro 4K | Done | Beran Jakub | TYM-212
- QS  | QS-30904 | QS rozhodnutí — GO | Done | Veselý Jan | TYM-302
- DEV | DEV-30905 | Backend recommendation engine | In Progress | Černý Pavel | TYM-212
- DEV | DEV-30906 | Tizen UI implementation | In Progress | Bílá Hana | TYM-302
- DEV | DEV-30907 | webOS UI implementation | New | Bílá Hana | TYM-302
- TST | TST-30908 | E2E test plán | New | Malý Tomáš | TYM-302

### tempo_roles
- Vývojář | 245.0
- Architekt | 95.5
- Business analytik | 62.0
- UX/WF | 38.5
- Systémový analytik | 28.0
- Tester | 12.0


## ND-1010: Audit a refresh privacy policy (GDPR update 2026)

- status: Delivery
- assignee: Kučera Tomáš
- created: 2026-02-15
- updated: 2026-05-13
- pi: PI3 2026
- wsjf: 4.5
- funnel: FUNNEL
- arts: CS, IT, DC
- teams: TYM-401, TYM-211, TYM-301
- parent: PROJEKT-105
- description_length: 2840

### description
Compliance projekt — aktualizace privacy policy ve všech kanálech (web, app, IVR, retail)
podle GDPR aktualizace 2026 + nového AI Act požadavku na transparentnost AI funkcí.

### apps
- AIP-13550 | Moje O2 Frontend | impacted
- AIP-15001 | B2B Portal | impacted
- AIP-14001 | Chat Frontend | impacted

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: true
- figma_url: https://figma.com/file/privacy-2026
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 89.0
- score: 7

### deliverables
- BAN | BAN-31001 | Legal review + RM signoff | Done | Černá Petra | TYM-401
- ARCH | ARCH-31002 | Consent management arch | Done | Svoboda Petr | TYM-211
- DEV | DEV-31003 | Update všech consent dialogů | In Progress | Krátký Lukáš | TYM-301
- TST | TST-31004 | Compliance test suite | In Progress | Malý Tomáš | TYM-401

### tempo_roles
- Business analytik | 48.0
- Architekt | 22.0
- Vývojář | 35.5
- Tester | 18.0


## ND-1011: Performance fix pro Customer 360 dashboard

- status: POSTIMPLEMENTATION
- assignee: Horák Martin
- created: 2025-10-20
- updated: 2026-05-02
- pi: PI2 2026
- wsjf: 5.0
- funnel: FUNNEL
- arts: CS
- teams: TYM-401
- parent: PROJEKT-105

### description
Optimalizace načítání Customer 360 dashboardu z 8s na cíleně <2s. Refactoring SQL dotazů,
přidání cache vrstvy (Redis), lazy-loading widgetů.

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 24.0
- score: 9

### deliverables
- DEV | DEV-31101 | SQL optimalizace | Done | Černý Pavel | TYM-401
- DEV | DEV-31102 | Redis cache integrace | Done | Krátký Lukáš | TYM-401
- TST | TST-31103 | Load test 1000 RPS | Done | Malý Tomáš | TYM-401
- RL  | RL-31104 | Produkční nasazení | Done | Horák Martin | TYM-401

### apps
- AIP-16001 | Network Monitoring | impacted
- AIP-24001 | 5G Core | informed
- AIP-25002 | Tariff Catalogue | informed

## ND-1012: Integrace Apple Pay do checkout flow eshopu

- status: New
- assignee: Dvořák Petr
- created: 2026-05-02
- updated: 2026-05-14
- pi: PI4 2026
- wsjf: 10.5
- funnel: FUNNEL
- arts: DC, IT
- teams: TYM-301, TYM-211
- parent: PROJEKT-101

### apps
- AIP-21001 | AI Chat Service | informed
- AIP-15001 | B2B Portal | informed

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: false
- ban_rm_exist: false
- discovery_tempo_hours: 63.4
- score: 1

## ND-1013: Sjednocení autentizace přes federated SSO (Keycloak)

- status: Discovery
- assignee: Novák Jan
- created: 2026-04-10
- updated: 2026-05-15
- pi: PI4 2026
- wsjf: 8.2
- funnel: FUNNEL
- arts: IT, DC, CS
- teams: TYM-211, TYM-301, TYM-401
- parent: PROJEKT-104

### description
Konsolidace 4 stávajících auth systémů (Moje O2, B2B Portal, Chat, IVR) pod jediný Keycloak.

### apps
- AIP-19001 | Keycloak Cluster | impacted
- AIP-13550 | Moje O2 Frontend | impacted
- AIP-15001 | B2B Portal | impacted
- AIP-14001 | Chat Frontend | impacted

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 88.0
- score: 6

### deliverables
- BAN | BAN-31301 | RM use-case mapping | Done | Nováková Eva | TYM-211
- ARCH | ARCH-31302 | Federation topology HLD | In Progress | Svoboda Petr | TYM-211


## ND-1014: Rebranding zákaznických emailů a SMS šablon

- status: Done
- assignee: Veselá Klára
- created: 2025-11-10
- updated: 2026-03-28
- pi: PI1 2026
- wsjf: 3.2
- funnel: FUNNEL
- arts: DC, MM
- teams: TYM-301, TYM-302
- parent: PROJEKT-102

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: true
- figma_url: https://figma.com/file/rebrand-2026
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 18.0
- score: 9

### apps
- AIP-14001 | Chat Frontend | impacted
- AIP-23001 | Core Router Config | impacted

## ND-1015: Zrušení podpory legacy SIM toolkit (STK)

- status: On Hold
- assignee: Horák Martin
- created: 2026-03-01
- updated: 2026-04-20
- pi: null
- wsjf: 2.0
- funnel: null
- arts: NTW, IT
- teams: TYM-601, TYM-212
- parent: PROJEKT-106

### apps
- AIP-19001 | Keycloak Cluster | informed

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: false
- ban_rm_exist: false
- discovery_tempo_hours: 59.2
- score: 2

## ND-1016: Implementace eSIM transferu mezi zařízeními (QR + bezkontaktní)

- status: QS
- assignee: Novák Jan
- created: 2026-02-22
- updated: 2026-05-14
- pi: PI3 2026
- wsjf: 9.0
- funnel: FUNNEL
- arts: NTW, IT, DC
- teams: TYM-601, TYM-211, TYM-301
- parent: PROJEKT-106

### apps
- AIP-20001 | eSIM Provisioning | impacted
- AIP-13550 | Moje O2 Frontend | impacted
- AIP-17001 | SMS Gateway Core | informed

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: true
- figma_url: https://figma.com/file/esim-transfer
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 156.0
- score: 8

### deliverables
- BAN | BAN-31601 | RM business model eSIM | Done | Nováková Eva | TYM-211
- ARCH | ARCH-31602 | QR provisioning HLD | Done | Beran Jakub | TYM-601
- QS  | QS-31603 | QS approval | Done | Veselý Jan | TYM-601
- DEV | DEV-31604 | Backend provisioning | New | Černý Pavel | TYM-211
- DEV | DEV-31605 | Mobile QR scanner | New | Bílá Hana | TYM-301

### tempo_roles
- Architekt | 68.0
- Business analytik | 38.0
- UX/WF | 22.5
- Vývojář | 18.0
- Systémový analytik | 9.5


## ND-1017: Migrace data warehouse z Oracle na Snowflake

- status: Lean BC
- assignee: Dvořák Petr
- created: 2026-04-05
- updated: 2026-05-12
- pi: PI1 2027
- wsjf: 6.8
- funnel: null
- arts: IT
- teams: TYM-212
- parent: PROJEKT-104

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: false
- impacted_apps_exist: false
- arch_qs_exist: false
- ban_rm_exist: true
- discovery_tempo_hours: 6.0
- score: 1

### apps
- AIP-12002 | Customer Portal | impacted
- AIP-23001 | Core Router Config | impacted
- AIP-14002 | Customer Care BO | informed

## ND-1018: Refaktor doručovacích notifikací pro retail síť

- status: Delivery
- assignee: Kučera Tomáš
- created: 2026-01-20
- updated: 2026-05-15
- pi: PI3 2026
- wsjf: 5.5
- funnel: FUNNEL
- arts: CS, DC
- teams: TYM-401, TYM-301
- parent: PROJEKT-105

### apps
- AIP-17002 | Notification Router | impacted
- AIP-14001 | Chat Frontend | impacted

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 42.0
- score: 7

### deliverables
- ARCH | ARCH-31801 | Refaktor návrh | Done | Svoboda Petr | TYM-401
- DEV | DEV-31802 | Push notification service v2 | In Progress | Krátký Lukáš | TYM-301
- TST | TST-31803 | Smoke testy v retail prostředí | New | Malý Tomáš | TYM-401


## ND-1019: Performance hotfix pro mobilní aplikaci Moje O2 (PI3 release blocker)

- status: Delivery
- assignee: Beneš Aleš
- created: 2026-05-01
- updated: 2026-05-15
- pi: PI3 2026
- wsjf: 12.5
- funnel: FUNNEL
- arts: FIX, DC
- teams: TYM-701, TYM-301
- parent: PROJEKT-107

### apps
- AIP-13550 | Moje O2 Frontend | impacted

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: false
- discovery_tempo_hours: 8.0
- score: 5

### deliverables
- DEV | DEV-31901 | Memory leak fix iOS | In Progress | Bílá Hana | TYM-701
- DEV | DEV-31902 | Bundle size optimalizace Android | Done | Krátký Lukáš | TYM-301
- TST | TST-31903 | Regression test suite | In Progress | Malý Tomáš | TYM-701


## ND-1020: Implementace AI chat asistenta pro Moje O2 (Q3 pilot)

- status: Discovery
- assignee: Procházková Lenka
- created: 2026-04-20
- updated: 2026-05-15
- pi: PI4 2026
- wsjf: 11.0
- funnel: FUNNEL
- arts: MM, DC, IT
- teams: TYM-302, TYM-301, TYM-212
- parent: PROJEKT-102

### apps
- AIP-21001 | AI Chat Service | impacted
- AIP-13550 | Moje O2 Frontend | impacted
- AIP-14001 | Chat Frontend | impacted

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: true
- figma_url: https://figma.com/file/ai-chat-mojeo2
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 112.0
- score: 6

### deliverables
- BAN | BAN-32001 | Use case katalog + ROI | Done | Černá Petra | TYM-302
- ARCH | ARCH-32002 | LLM stack HLD | In Progress | Beran Jakub | TYM-212
- ARCH | ARCH-32003 | Data privacy & compliance | New | Svoboda Petr | TYM-212

### tempo_roles
- Business analytik | 48.0
- Architekt | 38.5
- UX/WF | 18.0
- Systémový analytik | 7.5


## ND-1021: Decommission staré IVR větve pro retenci

- status: PreQS
- assignee: Kučera Tomáš
- created: 2026-03-15
- updated: 2026-05-10
- pi: PI4 2026
- wsjf: 3.8
- funnel: null
- arts: CS, IT
- teams: TYM-402, TYM-212
- parent: PROJEKT-105

### apps
- AIP-19001 | Keycloak Cluster | impacted

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: true
- figma_url: https://figma.com/file/mock-nd-1021
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 159.8
- score: 6

## ND-1022: Optimalizace Tempo reportingu pro management

- status: New
- assignee: Beneš Aleš
- created: 2026-05-08
- updated: 2026-05-15
- pi: PI4 2026
- wsjf: 4.0
- funnel: null
- arts: IT, FIX
- teams: TYM-212, TYM-701
- parent: PROJEKT-104

### apps
- AIP-17002 | Notification Router | impacted
- AIP-12002 | Customer Portal | impacted
- AIP-15001 | B2B Portal | informed

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: true
- figma_url: https://figma.com/file/mock-nd-1022
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: false
- discovery_tempo_hours: 74.9
- score: 1

## ND-1023: B2B custom invoicing pro key accounts

- status: Delivery
- assignee: Veselá Klára
- created: 2025-12-15
- updated: 2026-05-12
- pi: PI2 2026
- wsjf: 7.0
- funnel: FUNNEL
- arts: B2B, IT
- teams: TYM-502, TYM-211
- parent: PROJEKT-103

### apps
- AIP-12001 | Billing Core | impacted
- AIP-15001 | B2B Portal | impacted

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 64.0
- score: 8

### deliverables
- BAN | BAN-32301 | Custom invoice template katalog | Done | Nováková Eva | TYM-502
- ARCH | ARCH-32302 | Template engine HLD | Done | Svoboda Petr | TYM-211
- QS  | QS-32303 | QS approval | Done | Veselý Jan | TYM-211
- DEV | DEV-32304 | Template renderer | In Progress | Černý Pavel | TYM-211
- DEV | DEV-32305 | B2B portal UI flow | Done | Bílá Hana | TYM-502
- TST | TST-32306 | Test sady proti VAT scenarios | In Progress | Malý Tomáš | TYM-502

### tempo_roles
- Vývojář | 145.0
- Architekt | 48.0
- Business analytik | 35.0
- Tester | 22.5
- Systémový analytik | 12.0


## ND-1024: Modernizace retail POS terminálů (HW + SW refresh)

- status: Lean BC
- assignee: Horák Martin
- created: 2026-04-15
- updated: 2026-05-08
- pi: PI1 2027
- wsjf: 6.0
- funnel: FUNNEL
- arts: CS, IT, NTW
- teams: TYM-402, TYM-211, TYM-601
- parent: PROJEKT-105

### apps
- AIP-22001 | IMS Core | informed
- AIP-15001 | B2B Portal | impacted
- AIP-14001 | Chat Frontend | impacted

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: false
- discovery_tempo_hours: 80.9
- score: 2

## ND-1025: Cross-sell engine pro Moje O2 (insurance + smart home)

- status: Discovery
- assignee: Procházková Lenka
- created: 2026-03-28
- updated: 2026-05-13
- pi: PI4 2026
- wsjf: 8.5
- funnel: FUNNEL
- arts: MM, DC
- teams: TYM-303, TYM-301
- parent: PROJEKT-102

### apps
- AIP-21002 | Recommendation Engine | impacted
- AIP-13550 | Moje O2 Frontend | impacted

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: true
- figma_url: https://figma.com/file/crosssell
- impacted_apps_exist: true
- arch_qs_exist: false
- ban_rm_exist: true
- discovery_tempo_hours: 32.0
- score: 4


## ND-1026: PCI DSS recertifikace platebních flow (annual)

- status: POSTIMPLEMENTATION
- assignee: Beneš Aleš
- created: 2025-09-12
- updated: 2026-02-28
- pi: PI4 2025
- wsjf: 6.5
- funnel: FUNNEL
- arts: IT, FIX
- teams: TYM-211, TYM-701
- parent: PROJEKT-107

### apps
- AIP-21001 | AI Chat Service | impacted
- AIP-14002 | Customer Care BO | informed
- AIP-24001 | 5G Core | impacted

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: true
- figma_url: https://figma.com/file/mock-nd-1026
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 209.7
- score: 9

## ND-1027: Self-care voucher portal pro studenty

- status: New
- assignee: Veselá Klára
- created: 2026-05-10
- updated: 2026-05-15
- pi: PI1 2027
- wsjf: 5.2
- funnel: null
- arts: B2B, DC, MM
- teams: TYM-503, TYM-302, TYM-301
- parent: PROJEKT-103

### apps
- AIP-25002 | Tariff Catalogue | impacted
- AIP-25001 | Identity Service | informed
- AIP-19001 | Keycloak Cluster | impacted

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 56.9
- score: 1

## ND-1028: Migrace volání z VoLTE 1.0 na VoLTE 2.0 (CNAM, RTT)

- status: Delivery
- assignee: Horák Martin
- created: 2026-01-08
- updated: 2026-05-15
- pi: PI3 2026
- wsjf: 7.8
- funnel: FUNNEL
- arts: NTW, IT
- teams: TYM-602, TYM-212
- parent: PROJEKT-106

### apps
- AIP-22001 | IMS Core | impacted
- AIP-22002 | VoLTE Signaling | impacted

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 78.0
- score: 8

### deliverables
- ARCH | ARCH-32801 | VoLTE 2.0 signaling design | Done | Beran Jakub | TYM-602
- DEV | DEV-32802 | IMS Core upgrade | In Progress | Krátký Lukáš | TYM-602
- DEV | DEV-32803 | Probe & monitor integrace | Done | Černý Pavel | TYM-212
- TST | TST-32804 | Interop testy s Vodafone/T-Mobile | In Progress | Malý Tomáš | TYM-602
- RL  | RL-32805 | Postupný rollout (5 % → 100 %) | New | Horák Martin | TYM-602

### tempo_roles
- Architekt | 45.0
- Vývojář | 165.0
- Tester | 38.0
- Systémový analytik | 28.0


## ND-1029: Refaktor change-mgmt workflow v Jiře (ND vs. PROJEKT)

- status: Done
- assignee: Novák Jan
- created: 2025-08-20
- updated: 2026-01-15
- pi: PI4 2025
- wsjf: 4.2
- funnel: FUNNEL
- arts: IT
- teams: TYM-212
- parent: PROJEKT-104

### apps
- AIP-19001 | Keycloak Cluster | impacted
- AIP-24002 | RAN Configuration | impacted
- AIP-22001 | IMS Core | informed
- AIP-23001 | Core Router Config | informed

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: true
- figma_url: https://figma.com/file/mock-nd-1029
- impacted_apps_exist: true
- arch_qs_exist: false
- ban_rm_exist: true
- discovery_tempo_hours: 225.6
- score: 9

## ND-1030: Implementace IPv6 dual-stack v core síti

- status: QS
- assignee: Horák Martin
- created: 2026-02-01
- updated: 2026-05-14
- pi: PI4 2026
- wsjf: 6.2
- funnel: FUNNEL
- arts: NTW, IT
- teams: TYM-603, TYM-212
- parent: PROJEKT-106

### apps
- AIP-23001 | Core Router Config | impacted
- AIP-23002 | DNS Service | impacted

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 95.0
- score: 7

### deliverables
- ARCH | ARCH-33001 | Dual-stack topology HLD | Done | Beran Jakub | TYM-603
- QS  | QS-33002 | QS rozhodnutí — GO PI4 | Done | Veselý Jan | TYM-603


## ND-1031: Optimalizace Tempo worklog harvesteru (rychlost + completeness)

- status: New
- assignee: Beneš Aleš
- created: 2026-05-12
- updated: 2026-05-15
- pi: PI1 2027
- wsjf: 2.8
- funnel: null
- arts: FIX, IT
- teams: TYM-702, TYM-212
- parent: PROJEKT-107

### apps
- AIP-24001 | 5G Core | impacted

### dod
- description_filled: true
- has_excalidraw: false
- has_figma: true
- figma_url: https://figma.com/file/mock-nd-1031
- impacted_apps_exist: true
- arch_qs_exist: false
- ban_rm_exist: true
- discovery_tempo_hours: 86.2
- score: 1

## ND-1032: Roll-out 5G SA v Brně a Ostravě (PI4 wave)

- status: Delivery
- assignee: Horák Martin
- created: 2026-02-18
- updated: 2026-05-15
- pi: PI4 2026
- wsjf: 8.8
- funnel: FUNNEL
- arts: NTW
- teams: TYM-601, TYM-602
- parent: PROJEKT-106

### apps
- AIP-24001 | 5G Core | impacted
- AIP-24002 | RAN Configuration | impacted

### dod
- description_filled: true
- has_excalidraw: true
- has_figma: false
- impacted_apps_exist: true
- arch_qs_exist: true
- ban_rm_exist: true
- discovery_tempo_hours: 124.0
- score: 8

### deliverables
- ARCH | ARCH-33201 | 5G SA topology Brno | Done | Beran Jakub | TYM-601
- DEV | DEV-33202 | RAN config rollout Brno | In Progress | Krátký Lukáš | TYM-601
- DEV | DEV-33203 | RAN config rollout Ostrava | New | Krátký Lukáš | TYM-602
- TST | TST-33204 | Drive test Brno | In Progress | Malý Tomáš | TYM-601
- RL  | RL-33205 | Commercial launch | New | Horák Martin | TYM-601

### tempo_roles
- Architekt | 38.0
- Vývojář | 215.0
- Tester | 88.5
- Systémový analytik | 42.0
- Business analytik | 18.0

