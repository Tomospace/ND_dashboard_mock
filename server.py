#!/usr/bin/env python3
"""
ND Dashboard MOCK — standalone HTTP server pro UX/UI designera.

Cíl: klikatelný frontend ND Dashboardu nad mock daty. Žádná DB, žádné
externí connectory. Pouze Python stdlib + HTML/CSS/JS.

Spuštění:
    python3 server.py           # http://localhost:8090
    python3 server.py --port 9000

Edituj data/arts.md a data/nds.md, refreshni prohlížeč — UI ukáže
změny (na pozadí soubory automaticky znovu nahrávám při změně mtime).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")
WEB_DIR = os.path.join(ROOT, "web")
ARTS_MD = os.path.join(DATA_DIR, "arts.md")
NDS_MD = os.path.join(DATA_DIR, "nds.md")
STATIC_JSON = os.path.join(DATA_DIR, "static.json")

# ── Stav (cache) ──────────────────────────────────────────────
_state = {
    "arts": [],
    "nds": [],
    "static": {},
    "mtimes": {},
}
_state_lock = threading.Lock()


# ── MD parser ────────────────────────────────────────────────
_FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*$", re.S)


def _parse_simple_yaml(text: str) -> dict:
    """Velmi jednoduchý parser key: value řádků (bez vnořených struktur).
    Hodnoty: number, true/false, null, string (s/bez uvozovek), list (comma)."""
    out = {}
    for line in text.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^\s*-?\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, raw = m.group(1), m.group(2).strip()
        out[key] = _coerce(raw)
    return out


def _coerce(raw: str):
    if raw == "":
        return ""
    if raw.lower() == "null" or raw.lower() == "none":
        return None
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    # quoted string
    if (raw.startswith('"') and raw.endswith('"')) or (
        raw.startswith("'") and raw.endswith("'")
    ):
        return raw[1:-1]
    # number
    try:
        if "." in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        pass
    # comma list (e.g. "IT, DC")
    if "," in raw and not raw.startswith("http"):
        return [p.strip() for p in raw.split(",") if p.strip()]
    return raw


def parse_arts(text: str) -> list:
    """Splitne text podle `---` separátorů a každý blok parsne jako YAML."""
    arts = []
    # split on lines that are exactly `---`
    blocks = re.split(r"^---\s*$", text, flags=re.M)
    for block in blocks:
        block = block.strip()
        if not block or block.startswith("#"):
            continue
        meta = _parse_simple_yaml(block)
        if "art_key" in meta:
            arts.append(meta)
    return arts


def parse_nds(text: str) -> list:
    """Splitne text na `## ND-XXXX: Title` sekce.
    Každá sekce má: metadata (- key: value lines) + volitelné ### podsekce.
    """
    nds = []
    # find all ## ND-* headers
    parts = re.split(r"^##\s+(ND-\d+)\s*:\s*(.+)$", text, flags=re.M)
    # parts: [preamble, key1, title1, body1, key2, title2, body2, ...]
    for i in range(1, len(parts), 3):
        key = parts[i].strip()
        title = parts[i + 1].strip()
        body = parts[i + 2] if i + 2 < len(parts) else ""
        nds.append(_parse_nd_body(key, title, body))
    return nds


def _parse_nd_body(key: str, title: str, body: str) -> dict:
    """Sparsuje tělo jedné ND sekce."""
    # Split body into "header metadata" (dash lines before first ###)
    # and labelled sub-sections (### name)
    sections = re.split(r"^###\s+(\w+)\s*$", body, flags=re.M)
    header_block = sections[0]
    sub_sections = {}
    for j in range(1, len(sections), 2):
        name = sections[j].strip().lower()
        content = sections[j + 1].strip() if j + 1 < len(sections) else ""
        sub_sections[name] = content

    # Parse header metadata (- key: value lines)
    meta = {}
    for line in header_block.splitlines():
        m = re.match(r"^\s*-\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if m:
            meta[m.group(1)] = _coerce(m.group(2).strip())

    nd = {
        "key": key,
        "summary": title,
        "status": meta.get("status", "New"),
        "assignee": meta.get("assignee"),
        "created": meta.get("created"),
        "updated": meta.get("updated"),
        "pi": meta.get("pi"),
        "wsjf": meta.get("wsjf", 0.0) or 0.0,
        "funnel": meta.get("funnel"),
        "arts": _as_list(meta.get("arts")),
        "teams": _as_list(meta.get("teams")),
        "parent": meta.get("parent"),
        "description_length": meta.get("description_length", 0) or 0,
    }

    # sub-sections
    nd["description"] = sub_sections.get("description", "")

    nd["comments"] = _parse_pipe_lines(
        sub_sections.get("comments", ""),
        ["date", "author", "body"],
    )
    nd["timeline"] = _parse_pipe_lines(
        sub_sections.get("timeline", ""),
        ["date", "field", "to_value"],
    )
    nd["apps"] = _parse_pipe_lines(
        sub_sections.get("apps", ""),
        ["app_key", "app_name", "impact"],
    )

    nd["wiki"] = _parse_simple_yaml(sub_sections.get("wiki", ""))
    nd["dod"] = _parse_simple_yaml(sub_sections.get("dod", ""))

    # Rozšířené sekce pro ART DoD v2 + role views
    # deliverables: pipe-line items `role | key | summary | status | assignee | team`
    nd["deliverables_raw"] = _parse_pipe_lines(
        sub_sections.get("deliverables", ""),
        ["role", "key", "summary", "status", "assignee", "team"],
    )
    # tempo_roles: pipe-line items `role | hours`
    nd["tempo_roles_raw"] = _parse_pipe_lines(
        sub_sections.get("tempo_roles", ""),
        ["role", "hours"],
    )

    return nd


def _as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def _parse_pipe_lines(text: str, fields: list) -> list:
    """Parse `- a | b | c` lines into list of dicts."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^\s*-\s+(.+)$", line)
        if not m:
            continue
        parts = [p.strip() for p in m.group(1).split("|")]
        if len(parts) < len(fields):
            parts += [""] * (len(fields) - len(parts))
        out.append({fields[i]: parts[i] for i in range(len(fields))})
    return out


# ── Loader ───────────────────────────────────────────────────
def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def reload_state(force: bool = False) -> dict:
    """Načte data ze souborů, pokud se změnily (mtime check)."""
    changed = []
    with _state_lock:
        for label, path, parser in [
            ("arts", ARTS_MD, lambda t: parse_arts(t)),
            ("nds", NDS_MD, lambda t: parse_nds(t)),
            ("static", STATIC_JSON, lambda t: json.loads(t)),
        ]:
            try:
                mt = os.path.getmtime(path)
            except OSError:
                continue
            if force or _state["mtimes"].get(label) != mt:
                _state[label] = parser(_read(path))
                _state["mtimes"][label] = mt
                changed.append(label)
        return {"reloaded": changed, "arts": len(_state["arts"]), "nds": len(_state["nds"])}


# ── Aggregace pro endpointy ──────────────────────────────────
def _nds_for_art(art_short: str) -> list:
    """Vrátí seznam NDs, které mají daný ART v poli arts."""
    return [n for n in _state["nds"] if art_short in (n.get("arts") or [])]


def api_overview() -> list:
    arts = _state["arts"]
    out = []
    for art in arts:
        related = _nds_for_art(art.get("short_name", ""))
        in_progress = sum(
            1 for n in related if n.get("status") in ("Delivery", "PreQS", "Discovery")
        )
        done = sum(1 for n in related if n.get("status") == "POSTIMPLEMENTATION")
        out.append({
            "art_key": art["art_key"],
            "art_name": art["art_name"],
            "short_name": art["short_name"],
            "plan_count": len(related),
            "nd_count": len(related),
            "team_count": art.get("team_count", 0),
            "done_count": done,
            "in_progress_count": in_progress,
            "tempo_hours": art.get("tempo_hours", 0.0),
        })
    return out


def api_stats() -> dict:
    nds = _state["nds"]
    arts = _state["arts"]
    statuses = {}
    for n in nds:
        statuses[n["status"]] = statuses.get(n["status"], 0) + 1
    tempo = sum(a.get("tempo_hours", 0) or 0 for a in arts)
    plans = sum(len(n.get("arts") or []) for n in nds)
    apps = sum(len(n.get("apps") or []) for n in nds)
    return {
        "art_count": len(arts),
        "nd_count": len(nds),
        "plan_count": plans,
        "app_count": apps,
        "team_assignments": sum(len(n.get("teams") or []) for n in nds),
        "tempo_hours": round(tempo, 2),
        "tempo_authors": 42,
        "portfolio_count": len(_state["static"].get("portfolios", [])),
        "table_counts": {
            "arts": len(arts),
            "plans": plans,
            "impacted_apps": apps,
            "dca_teams": len(_state["static"].get("dca_teams", [])),
            "portfolio_epics": len(_state["static"].get("portfolios", [])),
            "tempo_worklogs": 1234,
            "schema_version": 1,
        },
        "_mock_mode": True,
    }


def api_art(art_key: str):
    art = next((a for a in _state["arts"] if a["art_key"] == art_key), None)
    if not art:
        return None
    related = _nds_for_art(art.get("short_name", ""))
    nds = []
    for n in related:
        nds.append({
            "nd_key": n["key"],
            "nd_summary": n["summary"],
            "nd_status": n["status"],
            "plan_count": 1,
            "done_plans": 1 if n["status"] == "POSTIMPLEMENTATION" else 0,
            "active_plans": 1 if n["status"] in ("Delivery", "PreQS", "Discovery") else 0,
            "pi": n.get("pi"),
            "funnel_status": n.get("funnel"),
            "wsjf": n.get("wsjf", 0.0),
            "team_keys": n.get("teams", []),
            "total_plans": len(n.get("arts") or []),
            "art_plans": {a: n["status"] for a in (n.get("arts") or [])},
        })
    return {
        "art": {
            "key": art["art_key"],
            "name": art["art_name"],
            "short_name": art["short_name"],
        },
        "nds": nds,
        "teams": [
            t for t in _state["static"].get("dca_teams", [])
            if t.get("art_short") == art.get("short_name")
        ],
    }


def _find_nd(nd_key: str):
    return next((n for n in _state["nds"] if n["key"] == nd_key), None)


def _normalize_apps(apps: list) -> list:
    """Mapuje MD apps shape -> shape očekávaný frontendem."""
    out = []
    for a in apps or []:
        out.append({
            "key": a.get("app_key") or a.get("key") or "",
            "app_name": a.get("app_name") or "",
            "status": a.get("impact") or a.get("status") or "informed",
            "assignee": a.get("assignee") or "",
            "teams": a.get("teams") or [],
            "dev_hours": a.get("dev_hours") or 0,
        })
    return out


def api_nd(nd_key: str):
    nd = _find_nd(nd_key)
    if not nd:
        return None
    plans = []
    for short in nd.get("arts") or []:
        art = next((a for a in _state["arts"] if a.get("short_name") == short), None)
        plans.append({
            "key": f"ROLE-{abs(hash(nd_key + short)) % 90000 + 10000}",
            "summary": f"{nd_key} {nd['summary']} | ART Implementation Plan | ART - {short}",
            "status": nd["status"],
            "assignee": nd.get("assignee"),
            "art_key": art["art_key"] if art else "",
            "art_name": art["art_name"] if art else f"ART - {short}",
            "pi": nd.get("pi"),
            "funnel_status": nd.get("funnel"),
            "wsjf": nd.get("wsjf", 0.0),
            "teams": " | ".join(nd.get("teams") or []),
        })
    return {
        "nd": {
            "key": nd["key"],
            "summary": nd["summary"],
            "description": nd.get("description") or "",
            "status": nd["status"],
            "assignee": nd.get("assignee"),
            "created": nd.get("created"),
            "updated": nd.get("updated"),
            "labels": json.dumps([nd["pi"]] if nd.get("pi") else []),
            "parent_key": nd.get("parent"),
            "last_synced": "2026-05-15T08:00:00",
        },
        "plans": plans,
        "apps": _normalize_apps(nd.get("apps")),
        "app_statuses": {},
        "tempo": [],
        "tempo_total_hours": 0,
    }


_ROLE_LABELS = {
    "BAN": {"label": "BAN / RM", "phase": "discovery"},
    "ARCH": {"label": "Arch QS", "phase": "discovery"},
    "QS": {"label": "QS & Execution", "phase": "discovery"},
    "TST": {"label": "Testing", "phase": "delivery"},
    "RL": {"label": "Release", "phase": "delivery"},
    "DEV": {"label": "Implementation", "phase": "delivery"},
}
_DONE_STATUSES = {"Done", "Closed", "Hotovo", "Resolved"}
_DISC_ROLES = {"BAN", "ARCH", "QS"}
_DELIV_ROLES = {"DEV", "TST", "RL"}


def _build_deliverables(items: list) -> tuple:
    """Z raw deliverables items vyrobí (deliverables[], ban[], lean_bc[], testing[], release[], children_total)."""
    by_role = {}
    for it in items or []:
        role = (it.get("role") or "").strip().upper()
        if role not in _ROLE_LABELS:
            continue
        child = {
            "key": it.get("key", ""),
            "summary": it.get("summary", ""),
            "status": it.get("status", "New"),
            "assignee": it.get("assignee", ""),
            "team": it.get("team", ""),
            "role": role,
        }
        if role not in by_role:
            by_role[role] = {"items": [], "done": 0, "total": 0, "assignees": set()}
        by_role[role]["items"].append(child)
        by_role[role]["total"] += 1
        if child["status"] in _DONE_STATUSES:
            by_role[role]["done"] += 1
        if child["assignee"]:
            by_role[role]["assignees"].add(child["assignee"])
    deliverables = []
    for role in ["BAN", "ARCH", "QS", "TST", "RL", "DEV"]:
        info = by_role.get(role)
        if not info:
            continue
        meta = _ROLE_LABELS[role]
        deliverables.append({
            "role": role,
            "label": meta["label"],
            "phase": meta["phase"],
            "total": info["total"],
            "done": info["done"],
            "tempo_hours": 0.0,
            "assignees": sorted(info["assignees"]),
            "responsible": sorted(info["assignees"]),
            "items": info["items"],
        })
    ban = by_role.get("BAN", {}).get("items", [])
    testing = by_role.get("TST", {}).get("items", [])
    release = by_role.get("RL", {}).get("items", [])
    children_total = sum(d["total"] for d in deliverables)
    return deliverables, ban, [], testing, release, children_total


_ROLE_HOURS_MAP = {
    "BAN": "Business analytik", "ARCH": "Architekt", "UX": "UX/WF",
    "QS": "Architekt", "SA": "Systémový analytik",
    "DEV": "Vývojář", "TST": "Tester", "RL": "Test architekt",
}


def _build_tempo_roles(raw: list) -> tuple:
    """Z raw tempo_roles items vyrobí (roles[], total, discovery_h, delivery_h)."""
    roles = []
    total = 0.0
    disc_h = 0.0
    deliv_h = 0.0
    for it in raw or []:
        role = (it.get("role") or "").strip()
        try:
            hours = float(it.get("hours") or 0)
        except (TypeError, ValueError):
            hours = 0.0
        if not role:
            continue
        roles.append({"role": role, "hours": round(hours, 1)})
        total += hours
        if role in {"Business analytik", "Architekt", "UX/WF"}:
            disc_h += hours
        elif role in {"Systémový analytik", "Vývojář", "Tester", "Test architekt"}:
            deliv_h += hours
    roles.sort(key=lambda x: -x["hours"])
    return roles, round(total, 1), round(disc_h, 1), round(deliv_h, 1)


_APP_TEAM_MAP = {
    # bestaehnt heuristic — namapování typických app prefixů na týmy
    "Billing Core": "TYM-211", "B2B Portal": "TYM-501", "KYC Service": "TYM-501",
    "Customer Portal": "TYM-301", "Moje O2 Frontend": "TYM-301",
    "Chat Frontend": "TYM-401", "Customer Care BO": "TYM-401", "LLM Gateway": "TYM-211",
    "AI Chat Service": "TYM-302",
    "RAN Configuration": "TYM-601", "Network Monitoring": "TYM-603",
    "SMS Gateway Core": "TYM-212", "Notification Router": "TYM-301",
    "O2 TV Backend": "TYM-302", "Recommendation Engine": "TYM-303",
    "Smart TV App (Tizen)": "TYM-302", "Smart TV App (webOS)": "TYM-302",
    "Keycloak Cluster": "TYM-213",
    "eSIM Provisioning": "TYM-601",
    "IMS Core": "TYM-602", "VoLTE Signaling": "TYM-602",
    "Core Router Config": "TYM-603", "DNS Service": "TYM-603",
    "5G Core": "TYM-601",
}


def _hash_pick(seed: str, options: list):
    if not options:
        return None
    return options[abs(hash(seed)) % len(options)]


def _build_delivery_teams(nd: dict, deliverables: list) -> list:
    """Pro každou impacted app vyrobí 1 řádek s týmem + MIRO + tasks + tempo + risk.

    Tvar očekávaný frontendem (sekce DELIVERY PLANNING):
        {app_key, app_name, team_name, miro_planned, miro_sprint,
         miro_commitment, tasks_created: [{key, status}], tempo_hours, risk_level, risk_reason}
    """
    apps = nd.get("apps") or []
    nd_teams = nd.get("teams") or []
    deliv_items_by_team = {}
    for d in deliverables:
        for it in d["items"]:
            t = it.get("team")
            if t:
                deliv_items_by_team.setdefault(t, []).append(it)

    rows = []
    if not apps and nd_teams:
        # fallback: 1 řádek per přiřazený tým, bez konkrétní aplikace
        for t in nd_teams:
            items = deliv_items_by_team.get(t, [])
            rows.append(_compose_delivery_row(nd, app_key="", app_name="", team_name=t, items=items))
        return rows

    for idx, a in enumerate(apps):
        app_key = a.get("app_key") or a.get("key") or ""
        app_name = a.get("app_name") or ""
        team = _APP_TEAM_MAP.get(app_name)
        if not team:
            # rotuj přes ND teams pro variabilitu
            team = nd_teams[idx % len(nd_teams)] if nd_teams else "—"
        items = deliv_items_by_team.get(team, [])
        rows.append(_compose_delivery_row(nd, app_key, app_name, team, items))
    return rows


def _compose_delivery_row(nd: dict, app_key: str, app_name: str, team_name: str, items: list) -> dict:
    """Vyrobí jeden řádek pro DELIVERY PLANNING tabulku."""
    status = nd.get("status") or "New"
    # MIRO planning — deterministická "fake" logika dle statusu + seed
    seed = f"{nd['key']}|{team_name}|{app_name}"
    in_active = status in {"Delivery", "PreQS", "QS", "POSTIMPLEMENTATION", "Done"}
    miro_planned = in_active and (abs(hash(seed)) % 10) < 8
    miro_sprint = None
    miro_commitment = None
    if miro_planned:
        sprint_num = (abs(hash(seed + "sprint")) % 6) + 1
        miro_sprint = f"S{sprint_num} {nd.get('pi') or 'PI3 2026'}"
        miro_commitment = "committed" if (abs(hash(seed + "c")) % 3) > 0 else "planned"
    tasks = [{"key": it["key"], "status": it["status"]} for it in items[:3]]
    # Tempo hours per team — odhad
    if items:
        done_ratio = sum(1 for it in items if it["status"] in _DONE_STATUSES) / max(len(items), 1)
        tempo_h = round(40 + done_ratio * 220 + (abs(hash(seed + "t")) % 60), 1)
    else:
        tempo_h = round((abs(hash(seed + "t2")) % 80), 1) if in_active else 0.0
    # Risk: red pokud aktivní status ale chybí MIRO; yellow pokud bez tasků; green jinak
    if in_active and not miro_planned:
        risk_level = "red"
        risk_reason = "Aktivní delivery, ale chybí MIRO sprint plánování"
    elif in_active and not tasks:
        risk_level = "yellow"
        risk_reason = "Žádné Jira children tasky pro tento tým"
    elif in_active:
        risk_level = "green"
        risk_reason = ""
    else:
        risk_level = "yellow"
        risk_reason = "ND zatím není v aktivní delivery fázi"
    return {
        "app_key": app_key,
        "app_name": app_name,
        "team_name": team_name,
        "team_art": "",
        "miro_planned": miro_planned,
        "miro_sprint": miro_sprint,
        "miro_commitment": miro_commitment,
        "tasks_created": tasks,
        "tempo_hours": tempo_h,
        "risk_level": risk_level,
        "risk_reason": risk_reason,
        # legacy fields (kompatibilita s ostatními views)
        "team": team_name,
        "hours": tempo_h,
        "roles": sorted({it.get("role") for it in items if it.get("role")}),
        "size": len(items),
    }


def api_nd_dod(nd_key: str):
    nd = _find_nd(nd_key)
    if not nd:
        return None
    base = api_nd(nd_key)
    dod = nd.get("dod") or {}
    deliverables, ban, lean_bc, testing, release, children_total = _build_deliverables(
        nd.get("deliverables_raw")
    )
    tempo_roles, tempo_total, disc_h, deliv_h = _build_tempo_roles(
        nd.get("tempo_roles_raw")
    )
    # fallback: pokud nemáme tempo_roles, použij discovery_tempo_hours z dod
    if tempo_total == 0 and dod.get("discovery_tempo_hours"):
        tempo_total = dod.get("discovery_tempo_hours", 0.0) or 0.0
        disc_h = tempo_total
    delivery_teams = _build_delivery_teams(nd, deliverables)
    return {
        "nd_key": nd_key,
        "summary": nd["summary"],
        "status": nd["status"],
        "description_length": nd.get("description_length", 0),
        "plans": base["plans"],
        "ban": ban,
        "lean_bc": lean_bc,
        "apps": _normalize_apps(nd.get("apps")),
        "discovery": {
            "arch": {
                "children": next((d["items"] for d in deliverables if d["role"] == "ARCH"), []),
                "has_excalidraw": bool(dod.get("has_excalidraw")),
                "has_figma": bool(dod.get("has_figma")),
                "figma_url": dod.get("figma_url"),
                "done": bool(dod.get("score", 0) and dod.get("score") >= 5),
            },
            "qs": next((d["items"] for d in deliverables if d["role"] == "QS"), []),
        },
        "discovery_signals": {
            "description_filled": bool(dod.get("description_filled")),
            "has_excalidraw": bool(dod.get("has_excalidraw")),
            "has_figma": bool(dod.get("has_figma")),
            "figma_url": dod.get("figma_url"),
            "impacted_apps_exist": bool(dod.get("impacted_apps_exist")),
            "arch_qs_exist": bool(dod.get("arch_qs_exist")),
            "ban_rm_exist": bool(dod.get("ban_rm_exist")),
            "discovery_tempo_hours": dod.get("discovery_tempo_hours", 0.0) or 0.0,
            "score": dod.get("score", 0) or 0,
        },
        "delivery_teams": delivery_teams,
        "testing": testing,
        "release": release,
        "impl_by_project": {},
        "deliverables": deliverables,
        "children_total": children_total,
        "tempo": {
            "total_hours": tempo_total,
            "discovery_hours": disc_h,
            "delivery_hours": deliv_h,
            "roles": tempo_roles,
            "teams": [],
            "unassigned": {"hours": 0.0, "authors": 0},
        },
    }


def api_nd_apps(nd_key: str):
    nd = _find_nd(nd_key)
    if not nd:
        return None
    return {"nd_key": nd_key, "apps": _normalize_apps(nd.get("apps"))}


def api_nd_comments(nd_key: str):
    nd = _find_nd(nd_key)
    if not nd:
        return None
    comments = []
    for c in nd.get("comments") or []:
        comments.append({
            "id": abs(hash(c.get("date", "") + c.get("body", ""))) % 1000000,
            "author": c.get("author") or "Unknown",
            "created": c.get("date"),
            "body": c.get("body") or "",
        })
    return {"nd_key": nd_key, "comments": comments, "total": len(comments)}


def api_nd_timeline(nd_key: str):
    nd = _find_nd(nd_key)
    if not nd:
        return None
    events = []
    for t in nd.get("timeline") or []:
        events.append({
            "date": t.get("date"),
            "field": t.get("field"),
            "from_value": "",
            "to_value": t.get("to_value"),
            "author": nd.get("assignee") or "system",
        })
    return {"nd_key": nd_key, "events": events, "total": len(events)}


def api_nd_timeline_widget(nd_key: str):
    """Kompaktnější verze pro widget."""
    tl = api_nd_timeline(nd_key)
    if not tl:
        return None
    return {
        "nd_key": nd_key,
        "current_status": (_find_nd(nd_key) or {}).get("status"),
        "events": tl["events"][-5:],
        "milestones": [],
    }


def api_nd_wiki(nd_key: str):
    nd = _find_nd(nd_key)
    if not nd:
        return None
    wiki = nd.get("wiki") or {}
    return {
        "nd_key": nd_key,
        "url": wiki.get("url"),
        "updated": wiki.get("updated"),
        "sections": wiki.get("sections", 0) or 0,
        "attachments": [],
    }


def api_nd_activity(nd_key: str):
    nd = _find_nd(nd_key)
    if not nd:
        return None
    items = []
    for c in nd.get("comments") or []:
        items.append({"type": "comment", "date": c.get("date"), "author": c.get("author"), "text": c.get("body")})
    for t in nd.get("timeline") or []:
        items.append({"type": "status", "date": t.get("date"), "author": nd.get("assignee"), "text": f"{t.get('field')} → {t.get('to_value')}"})
    items.sort(key=lambda x: x.get("date") or "", reverse=True)
    return {"nd_key": nd_key, "items": items}


def api_tempo(art_key: str, days: int = 90):
    art = next((a for a in _state["arts"] if a["art_key"] == art_key), None)
    if not art:
        return None
    total = art.get("tempo_hours", 0.0) or 0.0
    # rozdělíme tempo do roles
    roles = [
        {"role": "Developer", "hours": round(total * 0.45, 1), "authors": 8},
        {"role": "Tester", "hours": round(total * 0.20, 1), "authors": 4},
        {"role": "BAN", "hours": round(total * 0.15, 1), "authors": 3},
        {"role": "Architect", "hours": round(total * 0.10, 1), "authors": 2},
        {"role": "Ostatní", "hours": round(total * 0.10, 1), "authors": 5},
    ]
    return {
        "art_key": art_key,
        "art_name": art["art_name"],
        "days": days,
        "total_hours": total,
        "roles": roles,
        "by_week": [],
    }


def api_delayed():
    return _state["static"].get("delayed", [])


def api_portfolios():
    return _state["static"].get("portfolios", [])


def api_tree(root_key: str):
    """Strom hierarchie — root + NDs jako children."""
    portfolio = next((p for p in _state["static"].get("portfolios", []) if p["key"] == root_key), None)
    if not portfolio:
        return {"key": root_key, "summary": root_key, "children": []}
    children = []
    for n in _state["nds"]:
        if n.get("parent") == root_key:
            children.append({
                "key": n["key"],
                "summary": n["summary"],
                "status": n["status"],
                "children": [],
            })
    return {
        "key": portfolio["key"],
        "summary": portfolio["summary"],
        "status": portfolio["status"],
        "children": children,
    }


def api_pi_board(art: str = "", pi: str = ""):
    nds = [n for n in _state["nds"] if (not art or art in (n.get("arts") or []) or n.get("teams") and art in n.get("teams"))]
    if pi:
        nds = [n for n in nds if (n.get("pi") or "") == pi]
    return {
        "art": art,
        "pi": pi,
        "sprints": [
            {"name": "Sprint 1", "capacity": 80, "committed": 65, "completed": 60},
            {"name": "Sprint 2", "capacity": 80, "committed": 72, "completed": 58},
            {"name": "Sprint 3", "capacity": 80, "committed": 70, "completed": 0},
        ],
        "items": [
            {"nd_key": n["key"], "summary": n["summary"], "status": n["status"], "wsjf": n.get("wsjf", 0)}
            for n in nds
        ],
    }


def api_plenta_arts():
    return [
        {"art_key": a["art_key"], "art_name": a["art_name"], "short_name": a["short_name"]}
        for a in _state["arts"]
    ]


def api_plenta_board(art: str = "", pi: str = ""):
    """Plenta board ~ kapacitní plánování per team."""
    board = api_pi_board(art, pi)
    return {
        "art": art,
        "pi": pi,
        "teams": [
            {"team_key": t["team_key"], "team_name": t["team_name"], "capacity": 200, "allocated": 160}
            for t in _state["static"].get("dca_teams", [])
        ],
        "items": board["items"],
    }


def api_cross_art(source: str = ""):
    """Cross-ART matrix + per-ND plan table.

    Frontend (web/index.html, renderCrossArt) expects:
      - data.matrix:    [{source_group, target_group, total, active, canceled}, ...]
      - data.group_list: ["DC", "IT", ...]
      - data.stats:     {total, cross_art, nd_count}
      - data.nds:       [{nd_key, summary, nd_status, source_art, wsjf, pi,
                          planning_status, team_keys,
                          art_plans: {ART: {plans, status, cell_status, teams}}}]
    """
    def _cell_status_for(nd_status: str) -> str:
        s = (nd_status or "").lower()
        if "done" in s or "closed" in s:
            return "done"
        if "cancel" in s:
            return "canceled"
        if "delivery" in s or "realiz" in s or "progress" in s:
            return "active"
        return "empty"

    def _plan_status_for(nd_status: str) -> str:
        cs = _cell_status_for(nd_status)
        return {"done": "Done", "canceled": "Canceled", "active": "Active"}.get(cs, "Planned")

    # Deterministicky náhodný rozptyl per (nd, art) — některé ARTy "Planned",
    # jiné "Active", "Done", "Not planned" podle statusu ND.
    _STATUS_WEIGHTS = {
        "Done":               [("Done", 8), ("Active", 1), ("Planned", 1)],
        "POSTIMPLEMENTATION": [("Done", 7), ("Active", 2), ("Planned", 1)],
        "Delivery":           [("Active", 6), ("Done", 2), ("Planned", 2), ("Not planned", 1)],
        "QS":                 [("Active", 4), ("Planned", 4), ("Done", 1), ("Not planned", 1)],
        "PreQS":              [("Planned", 5), ("Active", 3), ("Not planned", 2)],
        "Discovery":          [("Planned", 5), ("Not planned", 3), ("Active", 2)],
        "Lean BC":            [("Planned", 3), ("Not planned", 6), ("Active", 1)],
        "New":                [("Not planned", 5), ("Planned", 4), ("Active", 1)],
        "On Hold":            [("Not planned", 7), ("Planned", 2), ("Active", 1)],
        "Canceled":           [("Canceled", 10)],
    }
    _CELL_FROM_LABEL = {
        "Done": "done", "Active": "active", "Canceled": "canceled",
        "Planned": "planned", "Not planned": "empty",
    }

    def _pick_plan(nd_key: str, art: str, nd_status: str) -> str:
        weights = _STATUS_WEIGHTS.get(nd_status, _STATUS_WEIGHTS["New"])
        total = sum(w for _, w in weights)
        h = abs(hash(f"{nd_key}|{art}|plan")) % total
        acc = 0
        for label, w in weights:
            acc += w
            if h < acc:
                return label
        return weights[-1][0]

    # Apply optional source filter (= owner ART)
    nds_filtered = []
    for n in _state["nds"]:
        nd_arts = n.get("arts") or []
        if not nd_arts:
            continue
        owner = nd_arts[0]
        if source and owner != source:
            continue
        nds_filtered.append((n, owner, nd_arts))

    # Build per-ND art_plans
    out_nds = []
    matrix_counter: dict = {}  # (src, tgt) -> {total, active, canceled}
    cross_art_count = 0
    total_plans = 0
    for n, owner, nd_arts in nds_filtered:
        nd_status = n.get("status", "")
        teams = n.get("teams") or []
        art_plans = {}
        plan_labels = []
        for a in nd_arts:
            plan_label = _pick_plan(n["key"], a, nd_status)
            plan_labels.append(plan_label)
            cell = _CELL_FROM_LABEL.get(plan_label, "empty")
            art_plans[a] = {
                "plans": 1 if plan_label != "Not planned" else 0,
                "status": plan_label,
                "cell_status": cell,
                "status_label": plan_label,
                "teams": {t: {"cell_status": cell} for t in teams},
            }
            total_plans += 1
        # Souhrnný planning_status na ND úrovni — agreguje stav napříč ARTy
        if all(l == "Not planned" for l in plan_labels):
            nd_plan_status = "Not planned"
        elif any(l == "Active" for l in plan_labels):
            nd_plan_status = "Active"
        elif all(l == "Done" for l in plan_labels):
            nd_plan_status = "Done"
        elif all(l == "Canceled" for l in plan_labels):
            nd_plan_status = "Canceled"
        else:
            nd_plan_status = "Planned"
        if len(nd_arts) > 1:
            cross_art_count += 1
            for tgt in nd_arts[1:]:
                key = (owner, tgt)
                m = matrix_counter.setdefault(key, {"total": 0, "active": 0, "canceled": 0})
                m["total"] += 1
                tgt_cell = art_plans[tgt]["cell_status"]
                if tgt_cell == "active":
                    m["active"] += 1
                elif tgt_cell == "canceled":
                    m["canceled"] += 1
        out_nds.append({
            "nd_key": n["key"],
            "summary": n.get("summary", ""),
            "nd_status": n.get("status", ""),
            "source_art": owner,
            "wsjf": n.get("wsjf"),
            "pi": n.get("pi", ""),
            "planning_status": nd_plan_status,
            "team_keys": teams,
            "art_plans": art_plans,
            "art_count": len(nd_arts),
        })

    matrix = [
        {"source_group": s, "target_group": t, **counts}
        for (s, t), counts in matrix_counter.items()
    ]
    group_list = sorted({owner for _, owner, _ in nds_filtered}
                        | {a for _, _, arr in nds_filtered for a in arr})

    return {
        "matrix": matrix,
        "group_list": group_list,
        "nds": out_nds,
        "stats": {
            "total": total_plans,
            "cross_art": cross_art_count,
            "nd_count": len(out_nds),
        },
        "source_filter": source,
    }


def api_cross_art_drilldown(nd: str = "", art: str = ""):
    n = _find_nd(nd)
    if not n:
        return {"nd_key": nd, "edges": []}
    nd_arts = n.get("arts") or []
    return {
        "nd_key": nd,
        "summary": n["summary"],
        "edges": [
            {"source": nd_arts[0] if nd_arts else "", "target": x, "status": n["status"]}
            for x in nd_arts[1:]
        ],
    }


def api_dependency_tracker(art: str = "", pi: str = ""):
    edges = []
    for n in _state["nds"]:
        arts = n.get("arts") or []
        if art and art not in arts:
            continue
        if pi and (n.get("pi") or "") != pi:
            continue
        for i, a in enumerate(arts):
            for b in arts[i + 1:]:
                edges.append({
                    "nd_key": n["key"],
                    "summary": n["summary"],
                    "from_art": a,
                    "to_art": b,
                    "status": n["status"],
                    "pi": n.get("pi"),
                })
    return {"art": art, "pi": pi, "edges": edges, "total": len(edges)}


def api_dca_teams():
    return _state["static"].get("dca_teams", [])


def api_changelog(limit: int = 20, offset: int = 0):
    items = _state["static"].get("changelog", [])
    return {
        "items": items[offset:offset + limit],
        "total": len(items),
        "limit": limit,
        "offset": offset,
    }


def api_sprint_navigator(art: str = "", pi: str = ""):
    return {
        "art": art,
        "pi": pi,
        "current_sprint": "Sprint 3",
        "sprints": ["Sprint 1", "Sprint 2", "Sprint 3", "Sprint 4", "Sprint 5"],
    }


def api_widget_registry():
    return _state["static"].get("widget_registry", [])


def api_canvas_layouts():
    return _state["static"].get("canvas_layouts", [])


def api_canvas_layout(layout_id: int):
    return _state["static"].get("canvas_layout_default")


def api_wiki_stats():
    nds_with_wiki = [n for n in _state["nds"] if (n.get("wiki") or {}).get("url")]
    return {
        "total_nds": len(_state["nds"]),
        "with_wiki": len(nds_with_wiki),
        "coverage": round(100.0 * len(nds_with_wiki) / max(len(_state["nds"]), 1), 1),
    }


# ── HTTP handler ─────────────────────────────────────────────
class ThreadedServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stdout.write(f"[{time.strftime('%H:%M:%S')}] {self.command} {self.path}\n")
        sys.stdout.flush()

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: str, content_type: str):
        try:
            with open(path, "rb") as f:
                body = f.read()
        except OSError:
            self.send_error(404, "not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict:
        ln = int(self.headers.get("Content-Length") or 0)
        if not ln:
            return {}
        try:
            return json.loads(self.rfile.read(ln).decode("utf-8"))
        except Exception:
            return {}

    def do_GET(self):
        reload_state()
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        q = urllib.parse.parse_qs(parsed.query)
        try:
            data = self._dispatch_get(path, q)
            if data is None:
                self.send_error(404, "not found")
                return
            if isinstance(data, tuple):  # raw bytes response
                return
            self._send_json(data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self._send_json({"error": str(e)}, status=500)

    def _dispatch_get(self, path: str, q: dict):
        # Static files
        if path == "/" or path == "/index.html":
            self._send_file(os.path.join(WEB_DIR, "index.html"), "text/html; charset=utf-8")
            return ("raw",)
        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return ("raw",)
        if path.startswith("/web/"):
            ext = os.path.splitext(path)[1].lower()
            ct = {
                ".css":  "text/css; charset=utf-8",
                ".js":   "application/javascript; charset=utf-8",
                ".html": "text/html; charset=utf-8",
                ".svg":  "image/svg+xml",
                ".png":  "image/png",
                ".jpg":  "image/jpeg",
                ".jpeg": "image/jpeg",
                ".woff": "font/woff",
                ".woff2": "font/woff2",
                ".json": "application/json; charset=utf-8",
            }.get(ext, "application/octet-stream")
            self._send_file(os.path.join(ROOT, path.lstrip("/")), ct)
            return ("raw",)

        # API
        if path == "/api/overview":
            return api_overview()
        if path == "/api/stats":
            return api_stats()
        if path == "/api/delayed":
            return api_delayed()
        if path == "/api/portfolios":
            return api_portfolios()
        if path == "/api/plenta-arts":
            return api_plenta_arts()
        if path == "/api/dca-teams":
            return api_dca_teams()
        if path == "/api/widget-registry":
            return api_widget_registry()
        if path == "/api/canvas-layouts":
            return api_canvas_layouts()
        if path == "/api/wiki-stats":
            return api_wiki_stats()
        if path == "/api/changelog":
            return api_changelog(
                int(q.get("limit", [20])[0]),
                int(q.get("offset", [0])[0]),
            )
        if path == "/api/pi-board":
            return api_pi_board(q.get("art", [""])[0], q.get("pi", [""])[0])
        if path == "/api/plenta-board":
            return api_plenta_board(q.get("art", [""])[0], q.get("pi", [""])[0])
        if path == "/api/cross-art":
            return api_cross_art(q.get("source", [""])[0])
        if path == "/api/cross-art/drilldown":
            return api_cross_art_drilldown(q.get("nd", [""])[0], q.get("art", [""])[0])
        if path == "/api/dependency-tracker":
            return api_dependency_tracker(q.get("art", [""])[0], q.get("pi", [""])[0])
        if path == "/api/sprint-navigator":
            return api_sprint_navigator(q.get("art", [""])[0], q.get("pi", [""])[0])
        if path == "/api/reload":
            return reload_state(force=True)

        # Prefix routes
        if path.startswith("/api/art/"):
            return api_art(path[len("/api/art/"):])
        if path.startswith("/api/tempo/"):
            return api_tempo(
                path[len("/api/tempo/"):],
                int(q.get("days", [90])[0]),
            )
        if path.startswith("/api/tree/"):
            return api_tree(path[len("/api/tree/"):])
        if path.startswith("/api/nd-dod/"):
            return api_nd_dod(path[len("/api/nd-dod/"):])
        if path.startswith("/api/nd-apps/"):
            return api_nd_apps(path[len("/api/nd-apps/"):])
        if path.startswith("/api/nd-comments/"):
            return api_nd_comments(path[len("/api/nd-comments/"):])
        if path.startswith("/api/nd-timeline-widget/"):
            return api_nd_timeline_widget(path[len("/api/nd-timeline-widget/"):])
        if path.startswith("/api/nd-timeline/"):
            return api_nd_timeline(path[len("/api/nd-timeline/"):])
        if path.startswith("/api/nd-wiki/"):
            return api_nd_wiki(path[len("/api/nd-wiki/"):])
        if path.startswith("/api/nd-activity/"):
            return api_nd_activity(path[len("/api/nd-activity/"):])
        if path.startswith("/api/nd/"):
            return api_nd(path[len("/api/nd/"):])
        if path.startswith("/api/canvas-layout/"):
            try:
                lid = int(path[len("/api/canvas-layout/"):])
            except ValueError:
                return None
            return api_canvas_layout(lid)

        return None

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        body = self._read_body()
        if parsed.path == "/api/sync":
            self._send_json({"status": "mock_mode", "message": "Sync je v mock režimu vypnutý.", "synced": 0})
            return
        if parsed.path == "/api/widget-data":
            # body: {"widget_type": "...", "config": {...}}
            wtype = body.get("widget_type") or body.get("type")
            cfg = body.get("config") or {}
            # routuj na příslušný endpoint
            mapping = {
                "nd-list": lambda: api_overview(),
                "discovery-signals": lambda: api_nd_dod(cfg.get("nd_key")) or {},
                "deliverables": lambda: api_nd_dod(cfg.get("nd_key")) or {},
                "tempo": lambda: api_tempo(cfg.get("art_key"), int(cfg.get("days", 90))) or {},
                "apps": lambda: api_nd_apps(cfg.get("nd_key")) or {},
                "activity": lambda: api_nd_activity(cfg.get("nd_key")) or {},
                "wiki": lambda: api_nd_wiki(cfg.get("nd_key")) or {},
                "cross-art": lambda: api_cross_art(),
            }
            fn = mapping.get(wtype, lambda: {})
            self._send_json({"widget_type": wtype, "data": fn()})
            return
        if parsed.path == "/api/canvas-layout":
            # Save layout — pretend success
            self._send_json({"id": int(time.time()), "saved": True, "_mock": "not persisted"})
            return
        if parsed.path == "/api/changelog":
            self._send_json({"id": int(time.time()), "added": True, "_mock": "not persisted"})
            return
        if parsed.path == "/api/reload":
            self._send_json(reload_state(force=True))
            return
        self.send_error(404, "not found")

    def do_PUT(self):
        # Stub — frontend nepoužívá, ale jistota
        self._send_json({"_mock": "PUT not supported"}, status=200)

    def do_DELETE(self):
        if self.path.startswith("/api/canvas-layout/"):
            self._send_json({"deleted": True, "_mock": "not persisted"})
            return
        self.send_error(404)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8090)
    ap.add_argument("--host", default="")
    args = ap.parse_args()

    res = reload_state(force=True)
    print(f"ND Dashboard MOCK running on http://localhost:{args.port}")
    print(f"  Data: {res['arts']} ARTs, {res['nds']} NDs")
    print(f"  Edit data/arts.md or data/nds.md → refresh browser")
    print(f"  Hot reload: file mtime check on every request")

    server = ThreadedServer((args.host, args.port), MockHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")


if __name__ == "__main__":
    main()
