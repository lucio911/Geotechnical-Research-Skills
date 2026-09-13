#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from collections import defaultdict
from pathlib import Path

TYPE_PREFIX = {
    "research_question": "RQ", "gap": "GAP", "hypothesis": "HYP", "method": "MTH",
    "dataset": "DAT", "quality_control": "QC", "analysis": "ANA", "parameter_set": "PAR", "result": "RES", "source": "SRC", "mechanism": "MEC",
    "claim": "CLM", "boundary": "BND", "figure": "FIG", "section": "SEC",
    "conclusion": "CON", "decision": "DEC",
}
RELATIONS = {
    "addresses", "tests", "produces", "assessed_by", "analyzed_by", "qualifies", "yields", "estimates", "parameterizes", "validates", "supports", "contradicts", "consistent_with", "discriminates",
    "explains", "bounds", "visualized_by", "reported_in", "concludes", "cites", "depends_on",
}
EVIDENCE_REL = {"supports", "contradicts", "consistent_with", "discriminates", "explains", "validates"}
GRADE = {f"E{i}" for i in range(6)}


def grounded(start, incoming, node_types, seen=None):
    seen = set() if seen is None else seen
    if start in seen:
        return False
    seen.add(start)
    for edge in incoming.get(start, []):
        src = edge["from"]
        if node_types.get(src) in {"result", "source", "dataset", "method", "analysis", "quality_control"}:
            return True
        if node_types.get(src) in {"claim", "mechanism", "hypothesis", "parameter_set"} and grounded(src, incoming, node_types, seen.copy()):
            return True
    return False


def find_cycles(node_types, outgoing):
    allowed = {n for n, t in node_types.items() if t in {"claim", "mechanism"}}
    cycles = []
    temp, perm, stack = set(), set(), []
    def visit(n):
        if n in perm: return
        if n in temp:
            i = stack.index(n) if n in stack else 0
            cycles.append(stack[i:] + [n]); return
        temp.add(n); stack.append(n)
        for e in outgoing.get(n, []):
            if e["to"] in allowed and e["relation"] in {"depends_on", "supports", "explains"}:
                visit(e["to"])
        stack.pop(); temp.remove(n); perm.add(n)
    for n in sorted(allowed): visit(n)
    return cycles


def main():
    ap = argparse.ArgumentParser(description="Validate a Geotechnical Evidence Graph JSON file.")
    ap.add_argument("graph")
    args = ap.parse_args()
    path = Path(args.graph)
    data = json.loads(path.read_text(encoding="utf-8"))
    errors, warnings = [], []
    nodes, edges = data.get("nodes", []), data.get("edges", [])
    ids = [n.get("id") for n in nodes]
    if len(ids) != len(set(ids)):
        errors.append("duplicate node IDs")
    node_map = {n["id"]: n for n in nodes if n.get("id")}
    node_types = {k: v.get("type") for k, v in node_map.items()}

    for nid, n in node_map.items():
        t = n.get("type")
        if t not in TYPE_PREFIX:
            errors.append(f"{nid}: unknown node type {t!r}"); continue
        if not re.fullmatch(rf"{re.escape(TYPE_PREFIX[t])}-\d{{3,}}", nid):
            errors.append(f"{nid}: ID prefix does not match type {t}")
        if not n.get("label"):
            errors.append(f"{nid}: missing label")

    incoming, outgoing = defaultdict(list), defaultdict(list)
    for i, e in enumerate(edges):
        src, dst, rel = e.get("from"), e.get("to"), e.get("relation")
        if src not in node_map: errors.append(f"edge {i}: unknown source {src}")
        if dst not in node_map: errors.append(f"edge {i}: unknown target {dst}")
        if rel not in RELATIONS: errors.append(f"edge {i}: unknown relation {rel}")
        if src in node_map and dst in node_map:
            incoming[dst].append(e); outgoing[src].append(e)
        if rel in EVIDENCE_REL:
            g = e.get("evidence_grade")
            if g is None: warnings.append(f"edge {i} {src}->{dst}: evidence relation has no grade")
            elif g not in GRADE: errors.append(f"edge {i}: invalid evidence grade {g}")
        if rel == "bounds" and node_types.get(src) != "boundary":
            errors.append(f"edge {i}: bounds relation should originate from BND node")
        if rel == "concludes" and not (node_types.get(src) == "claim" and node_types.get(dst) == "conclusion"):
            errors.append(f"edge {i}: concludes must be CLM -> CON")
        if rel == "assessed_by" and not (node_types.get(src) == "dataset" and node_types.get(dst) == "quality_control"):
            errors.append(f"edge {i}: assessed_by must be DAT -> QC")
        if rel == "analyzed_by" and not (node_types.get(src) == "dataset" and node_types.get(dst) == "analysis"):
            errors.append(f"edge {i}: analyzed_by must be DAT -> ANA")
        if rel == "qualifies" and node_types.get(src) != "quality_control":
            errors.append(f"edge {i}: qualifies should originate from QC")
        if rel == "estimates" and not (node_types.get(src) == "analysis" and node_types.get(dst) == "parameter_set"):
            errors.append(f"edge {i}: estimates must be ANA -> PAR")
        if rel == "parameterizes" and not (node_types.get(src) == "parameter_set" and node_types.get(dst) in {"analysis", "method"}):
            errors.append(f"edge {i}: parameterizes must be PAR -> ANA/MTH")
        if rel == "validates" and node_types.get(src) not in {"result", "source"}:
            errors.append(f"edge {i}: validates must originate from RES/SRC evidence")

    # Orphan checks.
    for nid, ntype in node_types.items():
        inc_rels = {e["relation"] for e in incoming.get(nid, [])}
        if ntype == "quality_control" and "assessed_by" not in inc_rels:
            errors.append(f"{nid}: QC node has no DAT -> assessed_by provenance")
        elif ntype == "analysis" and not ({"analyzed_by", "parameterizes", "qualifies"} & inc_rels):
            errors.append(f"{nid}: analysis node has no dataset/QC/parameter provenance")
        elif ntype == "parameter_set" and "estimates" not in inc_rels:
            errors.append(f"{nid}: parameter set has no incoming estimates edge from analysis")
        elif ntype == "result" and not ({"produces", "yields", "supports", "tests"} & inc_rels):
            errors.append(f"{nid}: result has no upstream provenance")
        elif ntype == "claim":
            if not ({"supports", "discriminates", "explains", "depends_on", "tests"} & inc_rels):
                errors.append(f"{nid}: claim has no supporting/dependency edge")
            elif not grounded(nid, incoming, node_types):
                errors.append(f"{nid}: claim dependency chain does not reach result/source/dataset/method evidence")
        elif ntype == "conclusion" and "concludes" not in inc_rels:
            errors.append(f"{nid}: conclusion has no incoming concludes edge from a claim")
        elif ntype == "figure" and "visualized_by" not in inc_rels:
            warnings.append(f"{nid}: figure has no incoming visualized_by relation")
        elif ntype == "mechanism" and not ({"consistent_with", "discriminates", "explains", "supports"} & inc_rels):
            warnings.append(f"{nid}: mechanism has no explicit evidentiary input")

    bounded_claims = {e["to"] for e in edges if e.get("relation") == "bounds"}
    for nid, ntype in node_types.items():
        if ntype == "claim" and nid not in bounded_claims:
            warnings.append(f"{nid}: no explicit BND node bounds this claim")

    for nid, ntype in node_types.items():
        if ntype == "source" and not node_map[nid].get("role"):
            warnings.append(f"{nid}: external source has no declared scientific role")

    contradicted = {e["to"] for e in edges if e.get("relation") == "contradicts"}
    for cid in contradicted:
        n = node_map.get(cid, {})
        if n.get("status") == "active" and n.get("confidence") == "high":
            warnings.append(f"{cid}: high-confidence active claim has contradictory evidence; document resolution")

    for cyc in find_cycles(node_types, outgoing):
        warnings.append("circular claim/mechanism dependency: " + " -> ".join(cyc))

    print(f"Graph: {path}")
    print(f"Nodes: {len(nodes)} | Edges: {len(edges)}")
    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
