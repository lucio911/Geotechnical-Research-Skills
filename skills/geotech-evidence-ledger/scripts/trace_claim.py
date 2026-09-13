#!/usr/bin/env python3
import argparse, json
from collections import defaultdict
from pathlib import Path

ap = argparse.ArgumentParser(description="Trace upstream evidence for a claim/conclusion.")
ap.add_argument("graph")
ap.add_argument("node_id")
args = ap.parse_args()
data = json.loads(Path(args.graph).read_text(encoding="utf-8"))
nodes = {n["id"]: n for n in data["nodes"]}
incoming = defaultdict(list)
for e in data["edges"]:
    incoming[e["to"]].append(e)

if args.node_id not in nodes:
    raise SystemExit(f"Unknown node: {args.node_id}")

seen = set()
def walk(nid, depth=0):
    pref = "  " * depth
    n = nodes[nid]
    print(f"{pref}{nid} [{n['type']}] — {n.get('label','')}")
    if nid in seen:
        print(pref + "  (already visited)")
        return
    seen.add(nid)
    for e in incoming.get(nid, []):
        grade = f" {e['evidence_grade']}" if e.get("evidence_grade") else ""
        print(f"{pref}  <- {e['relation']}{grade}")
        walk(e["from"], depth + 2)

walk(args.node_id)
