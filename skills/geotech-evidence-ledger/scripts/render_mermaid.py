#!/usr/bin/env python3
import argparse, json
from pathlib import Path

ap = argparse.ArgumentParser(description="Render Evidence Graph as Mermaid flowchart text.")
ap.add_argument("graph")
args = ap.parse_args()
data = json.loads(Path(args.graph).read_text(encoding="utf-8"))
label = {n["id"]: n.get("label", "") for n in data["nodes"]}
print("```mermaid")
print("flowchart LR")
for n in data["nodes"]:
    text = n.get("label", "").replace('"', "'")
    if len(text) > 58:
        text = text[:55] + "..."
    print(f'  {n["id"].replace("-", "_")}["{n["id"]}: {text}"]')
for e in data["edges"]:
    a = e["from"].replace("-", "_")
    b = e["to"].replace("-", "_")
    rel = e["relation"]
    print(f"  {a} -->|{rel}| {b}")
print("```")
