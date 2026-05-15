#!/usr/bin/env python3
"""
One-off script: capture sample JSON responses from running ND Dashboard
(localhost:8085) for all GET endpoints used by the frontend. Saves to
_samples/<slug>.json so we know the exact JSON shape mock server must
produce.
"""
import json
import os
import sys
import urllib.request

BASE = "http://localhost:8085"
OUT = os.path.dirname(os.path.abspath(__file__))


def fetch(path):
    try:
        with urllib.request.urlopen(BASE + path, timeout=10) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return {"_error": str(e), "_path": path}


def save(slug, data):
    with open(os.path.join(OUT, slug + ".json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  saved {slug}.json ({len(json.dumps(data, ensure_ascii=False))} chars)")


def main():
    print("Capturing samples from", BASE)

    # 1. Top-level
    overview = fetch("/api/overview")
    save("overview", overview)
    save("stats", fetch("/api/stats"))
    save("delayed", fetch("/api/delayed"))
    save("portfolios", fetch("/api/portfolios"))
    save("plenta-arts", fetch("/api/plenta-arts"))
    save("dca-teams", fetch("/api/dca-teams"))
    save("widget-registry", fetch("/api/widget-registry"))
    save("canvas-layouts", fetch("/api/canvas-layouts"))
    save("changelog", fetch("/api/changelog?limit=20&offset=0"))
    save("cross-art", fetch("/api/cross-art"))
    save("dependency-tracker", fetch("/api/dependency-tracker"))

    # 2. Pick first ART
    art_key = None
    if isinstance(overview, list) and overview:
        art_key = overview[0].get("art_key")
    elif isinstance(overview, dict):
        arts = overview.get("arts") or overview.get("items") or []
        if arts:
            art_key = arts[0].get("art_key") or arts[0].get("key")
    print(f"  picked ART: {art_key}")
    if art_key:
        art_detail = fetch(f"/api/art/{art_key}")
        save("art_detail", art_detail)
        save("tempo", fetch(f"/api/tempo/{art_key}?days=90"))

        # 3. Find first ND from that ART
        nd_key = None
        nds = art_detail.get("nds") or art_detail.get("issues") or []
        if nds:
            nd_key = nds[0].get("nd_key") or nds[0].get("key")
        print(f"  picked ND: {nd_key}")
        if nd_key:
            save("nd_detail", fetch(f"/api/nd/{nd_key}"))
            save("nd-dod", fetch(f"/api/nd-dod/{nd_key}"))
            save("nd-apps", fetch(f"/api/nd-apps/{nd_key}"))
            save("nd-comments", fetch(f"/api/nd-comments/{nd_key}"))
            save("nd-timeline", fetch(f"/api/nd-timeline/{nd_key}"))
            save("nd-timeline-widget", fetch(f"/api/nd-timeline-widget/{nd_key}"))
            save("nd-wiki", fetch(f"/api/nd-wiki/{nd_key}"))
            save("nd-activity", fetch(f"/api/nd-activity/{nd_key}"))
            save("cross-art-drilldown", fetch(f"/api/cross-art/drilldown?nd={nd_key}"))

        # 4. PI board, plenta board
        save("pi-board", fetch(f"/api/pi-board?art={art_key}&pi=PI3 2026"))
        save("plenta-board", fetch(f"/api/plenta-board?art={art_key}&pi=PI3 2026"))
        save("sprint-navigator", fetch(f"/api/sprint-navigator?art={art_key}"))

    # 5. Portfolio tree
    portfolios = fetch("/api/portfolios")
    if isinstance(portfolios, list) and portfolios:
        root = portfolios[0].get("key") or portfolios[0].get("nd_key")
        if root:
            save("tree", fetch(f"/api/tree/{root}"))

    # 6. Canvas layout sample (first one if exists)
    layouts = fetch("/api/canvas-layouts")
    if isinstance(layouts, list) and layouts:
        lid = layouts[0].get("id")
        if lid is not None:
            save("canvas-layout", fetch(f"/api/canvas-layout/{lid}"))

    print("\nDone. Samples in", OUT)


if __name__ == "__main__":
    main()
