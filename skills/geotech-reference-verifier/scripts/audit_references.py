#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import resolve_reference as rr  # noqa: E402


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def debrace(value: str) -> str:
    # BibTeX braces used only for case protection must not create false title tokens.
    return re.sub(r'[{}]', '', value or '').strip()


def normalize_bib_author(name: str) -> str:
    name = debrace(name).strip()
    if ',' in name:
        parts = [x.strip() for x in name.split(',') if x.strip()]
        if len(parts) >= 2:
            # Common BibTeX "Family, Given" form -> "Given Family" for identity matching.
            return ' '.join(parts[1:] + [parts[0]])
    return name


def split_authors(value: str) -> list[str]:
    return [normalize_bib_author(x) for x in re.split(r'\s+and\s+', value or '', flags=re.I) if x.strip()]


def parse_year(value: str) -> int | None:
    m = re.search(r'(?<!\d)(1[5-9]\d{2}|20\d{2}|21\d{2})(?!\d)', value or '')
    return int(m.group(1)) if m else None


def strip_value(value: str) -> str:
    value = value.strip().rstrip(',').strip()
    if len(value) >= 2 and ((value[0] == '{' and value[-1] == '}') or (value[0] == '"' and value[-1] == '"')):
        value = value[1:-1]
    return value.strip()


def split_top_level(text: str, delimiter: str = ',') -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for i, ch in enumerate(text):
        if escaped:
            escaped = False
            continue
        if ch == '\\':
            escaped = True
            continue
        if ch == '"' and depth == 0:
            quoted = not quoted
            continue
        if not quoted:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth = max(0, depth - 1)
            elif ch == delimiter and depth == 0:
                parts.append(text[start:i])
                start = i + 1
    parts.append(text[start:])
    return parts


def parse_bibtex(text: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    i, n = 0, len(text)
    while i < n:
        at = text.find('@', i)
        if at < 0:
            break
        m = re.match(r'@\s*([A-Za-z]+)\s*([({])', text[at:])
        if not m:
            i = at + 1
            continue
        entry_type = m.group(1).lower()
        open_ch = m.group(2)
        close_ch = '}' if open_ch == '{' else ')'
        body_start = at + m.end()
        depth = 1
        quoted = False
        escaped = False
        j = body_start
        while j < n and depth:
            ch = text[j]
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"' and open_ch == '{':
                quoted = not quoted
            elif not quoted:
                if ch == open_ch:
                    depth += 1
                elif ch == close_ch:
                    depth -= 1
            j += 1
        if depth:
            raise ValueError(f'unclosed BibTeX entry beginning at character {at}')
        body = text[body_start:j-1].strip()
        chunks = split_top_level(body)
        if not chunks:
            i = j
            continue
        citekey = chunks[0].strip()
        fields: dict[str, str] = {}
        for chunk in chunks[1:]:
            if '=' not in chunk:
                continue
            key, value = chunk.split('=', 1)
            fields[key.strip().lower()] = strip_value(value)
        if entry_type not in {'comment', 'preamble', 'string'} and citekey:
            title = debrace(fields.get('title', ''))
            venue = debrace(fields.get('journal') or fields.get('booktitle') or fields.get('publisher') or '')
            entries.append({
                'citekey': citekey,
                'entry_type': entry_type,
                'original': {
                    'title': title,
                    'authors': split_authors(fields.get('author', '')),
                    'year': parse_year(fields.get('year', '')),
                    'venue': venue,
                    'doi': rr.clean_doi(debrace(fields.get('doi', ''))) or '',
                },
                'fields': fields,
            })
        i = j
    return entries


def cache_key(entry: dict[str, Any], use_openalex: bool) -> str:
    payload = {'original': entry['original'], 'use_openalex': use_openalex, 'resolver_schema': 1}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()


def build_report(reference_id: str, original: dict[str, Any], candidates: list[dict[str, Any]], provenance: list[dict[str, Any]], rows: int, mode: str, use_openalex: bool) -> dict[str, Any]:
    seen, unique = set(), []
    for c in candidates:
        key = (rr.clean_doi(c.get('doi')) or '', rr.norm_text(c.get('title')), c.get('year'))
        if key not in seen:
            seen.add(key)
            unique.append(c)
    ranked = sorted((rr.score(original, c) for c in unique), key=lambda x: x['identity_score'], reverse=True)
    verdict, confidence, needs_human = rr.classify(original, ranked)
    top = ranked[0] if ranked else None
    resolved = dict(top['candidate']) if top else {}
    if resolved.get('doi'):
        for c in candidates:
            if c.get('source') == 'openalex' and rr.clean_doi(c.get('doi')) == rr.clean_doi(resolved.get('doi')) and c.get('is_retracted') is not None:
                resolved['is_retracted'] = c.get('is_retracted')
                resolved['retraction_status_source'] = 'openalex'
                break
    checks = dict(top['checks']) if top else {'identifier_resolves': False, 'identity_match': False, 'identity_score': None}
    if top:
        checks['identity_match'] = verdict in {'VERIFIED', 'VERIFIED_WITH_DRIFT'}
        checks['identity_score'] = top['identity_score']
        checks['candidate_margin'] = round(top['identity_score'] - ranked[1]['identity_score'], 4) if len(ranked) > 1 else None
    return {
        'reference_id': reference_id,
        'original': original,
        'resolver': {'mode': mode, 'sources_attempted': [p.get('source') for p in provenance], 'openalex_enabled': bool(use_openalex), 'retrieved_at': now_iso()},
        'resolved': resolved,
        'checks': checks,
        'identity_score': top['identity_score'] if top else None,
        'verdict': verdict,
        'confidence': confidence,
        'human_review': False,
        'requires_human_review': needs_human or verdict in {'IDENTIFIER_MISMATCH', 'AMBIGUOUS', 'UNRESOLVED'},
        'publication_status': {
            'is_retracted': resolved.get('is_retracted') if resolved else None,
            'source': resolved.get('retraction_status_source') if resolved else None,
            'note': 'OpenAlex is_retracted is secondary status evidence; absence of a flag is not proof of clean status.',
        },
        'candidates': ranked[:max(1, min(rows, 10))],
        'provenance': provenance,
        'policy': {'not_found_is_not_fabricated': True, 'automatic_fabrication_confirmation': False, 'formatting_may_not_modify_identity': True},
    }


def resolve_entry(entry: dict[str, Any], ns: argparse.Namespace, cache_dir: Path | None) -> tuple[dict[str, Any], bool]:
    key = cache_key(entry, ns.use_openalex)
    cache_path = cache_dir / f'{key}.json' if cache_dir else None
    if cache_path and cache_path.exists() and not ns.refresh_cache:
        return json.loads(cache_path.read_text(encoding='utf-8')), True

    original = entry['original']
    candidates: list[dict[str, Any]] = []
    provenance: list[dict[str, Any]] = []
    mode = 'online'
    if ns.offline_dir:
        mode = 'offline'
        fixture = Path(ns.offline_dir) / f"{entry['citekey']}.json"
        if fixture.exists():
            raw = json.loads(fixture.read_text(encoding='utf-8'))
            candidates = raw.get('candidates', []) if isinstance(raw, dict) else raw
            provenance.append({'source': 'offline_fixture', 'url': str(fixture), 'status': f'loaded_{len(candidates)}'})
        else:
            provenance.append({'source': 'offline_fixture', 'url': str(fixture), 'status': 'missing'})
    else:
        ua = rr.DEFAULT_UA + (f' mailto:{ns.email}' if ns.email else '')
        got, prov = rr.crossref(original, ns.email, ua, ns.timeout, ns.rows)
        candidates += got; provenance += prov
        if not got or not rr.clean_doi(original.get('doi')):
            got, prov = rr.datacite(original, ua, ns.timeout, ns.rows)
            candidates += got; provenance += prov
        if ns.use_openalex:
            got, prov = rr.openalex(original, ns.openalex_api_key, ua, ns.timeout, ns.rows)
            candidates += got; provenance += prov
        if ns.delay > 0:
            time.sleep(ns.delay)

    report = build_report(entry['citekey'], original, candidates, provenance, ns.rows, mode, ns.use_openalex)
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report, False


def duplicate_groups(entries: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_doi: dict[str, list[str]] = defaultdict(list)
    for e in entries:
        doi = rr.clean_doi(e['original'].get('doi'))
        if doi:
            by_doi[doi].append(e['citekey'])
    doi_groups = [{'doi': doi, 'citekeys': keys} for doi, keys in sorted(by_doi.items()) if len(keys) > 1]

    title_groups: list[dict[str, Any]] = []
    seen_pairs = set()
    for i, a in enumerate(entries):
        ta = a['original'].get('title') or ''
        if not ta:
            continue
        for b in entries[i+1:]:
            tb = b['original'].get('title') or ''
            if not tb:
                continue
            sim = rr.text_similarity(ta, tb)
            if sim < 0.94:
                continue
            ya, yb = a['original'].get('year'), b['original'].get('year')
            ao = rr.author_overlap(a['original'].get('authors') or [], b['original'].get('authors') or [])
            if (ya and yb and abs(ya-yb) > 1) or ao < 0.34:
                continue
            pair = tuple(sorted([a['citekey'], b['citekey']]))
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                title_groups.append({'citekeys': list(pair), 'title_similarity': sim, 'author_overlap': ao, 'years': [ya, yb]})
    return doi_groups, title_groups


def render_markdown(report: dict[str, Any]) -> str:
    s = report['summary']
    lines = [
        '# Reference Integrity Report', '',
        f"Generated: `{report['generated_at']}`", '',
        '## Summary', '',
        '| Metric | Count |', '|---|---:|',
        f"| Total references | {s['total_references']} |",
    ]
    for verdict in ['VERIFIED','VERIFIED_WITH_DRIFT','IDENTIFIER_MISMATCH','AMBIGUOUS','UNRESOLVED']:
        lines.append(f"| {verdict} | {s['verdict_counts'].get(verdict,0)} |")
    lines += [
        f"| Retracted flags | {s['retracted_flags']} |",
        f"| Duplicate DOI groups | {s['duplicate_doi_groups']} |",
        f"| Near-duplicate title pairs | {s['near_duplicate_title_pairs']} |",
        f"| Human-review records | {s['human_review_records']} |",
        f"| Cache hits | {s['cache_hits']} |", '',
        '## Critical / manual actions', '',
    ]
    actions = report.get('actions') or []
    if not actions:
        lines.append('- None detected by deterministic rules.')
    else:
        for a in actions:
            lines.append(f"- **{a['severity']}** `{a.get('citekey','')}` — {a['message']}")
    lines += ['', '## Per-reference results', '', '| Citekey | Verdict | Score | DOI | Human review | Retracted |', '|---|---|---:|---|---|---|']
    for item in report['references']:
        doi = item.get('original',{}).get('doi') or ''
        score = item.get('identity_score')
        score_s = '' if score is None else f'{score:.3f}'
        lines.append(f"| `{item['reference_id']}` | {item['verdict']} | {score_s} | {doi} | {'yes' if item.get('requires_human_review') else 'no'} | {'yes' if item.get('publication_status',{}).get('is_retracted') else 'no'} |")
    lines += ['', '## Duplicate DOI groups', '']
    if report['duplicates']['doi']:
        for g in report['duplicates']['doi']:
            lines.append(f"- `{g['doi']}`: " + ', '.join(f"`{x}`" for x in g['citekeys']))
    else:
        lines.append('- None.')
    lines += ['', '## Near-duplicate title pairs', '']
    if report['duplicates']['title']:
        for g in report['duplicates']['title']:
            lines.append(f"- {', '.join(f'`{x}`' for x in g['citekeys'])}: title={g['title_similarity']:.3f}, author-overlap={g['author_overlap']:.3f}")
    else:
        lines.append('- None.')
    lines += ['', '> `UNRESOLVED` is not evidence of fabrication. Confirmed fabrication remains a human scientific-integrity decision.', '']
    return '\n'.join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description='Batch forensic audit for BibTeX references using the v0.5 reference resolver.')
    ap.add_argument('bib')
    ap.add_argument('--email', help='Crossref polite-pool contact email')
    ap.add_argument('--use-openalex', action='store_true')
    ap.add_argument('--openalex-api-key')
    ap.add_argument('--timeout', type=float, default=12.0)
    ap.add_argument('--rows', type=int, default=5)
    ap.add_argument('--delay', type=float, default=0.15, help='Delay between online references')
    ap.add_argument('--cache-dir', default='.geotech/cache/reference-resolver')
    ap.add_argument('--no-cache', action='store_true')
    ap.add_argument('--refresh-cache', action='store_true')
    ap.add_argument('--offline-dir', help='Directory containing <citekey>.json candidate fixtures; disables network')
    ap.add_argument('--output-json', default='reference-integrity-report.json')
    ap.add_argument('--output-md', default='reference-integrity-report.md')
    ap.add_argument('--fail-on-critical', action='store_true', help='Return nonzero when deterministic critical actions are found')
    ns = ap.parse_args()

    bib_path = Path(ns.bib)
    entries = parse_bibtex(bib_path.read_text(encoding='utf-8'))
    if not entries:
        print('ERROR: no BibTeX entries parsed', file=sys.stderr)
        return 2
    keys = [e['citekey'] for e in entries]
    if len(keys) != len(set(keys)):
        print('ERROR: duplicate citekeys in BibTeX input', file=sys.stderr)
        return 2

    cache_dir = None if ns.no_cache else Path(ns.cache_dir)
    doi_dups, title_dups = duplicate_groups(entries)
    results = []
    cache_hits = 0
    for entry in entries:
        result, cached = resolve_entry(entry, ns, cache_dir)
        results.append(result)
        cache_hits += int(cached)
        print(f"{entry['citekey']}: {result['verdict']}" + (f" ({result['identity_score']:.3f})" if result.get('identity_score') is not None else ''))

    counts = Counter(r['verdict'] for r in results)
    actions: list[dict[str, str]] = []
    for r in results:
        citekey = r['reference_id']
        if r['verdict'] == 'IDENTIFIER_MISMATCH':
            actions.append({'severity':'CRITICAL','citekey':citekey,'code':'IDENTIFIER_MISMATCH','message':'Persistent identifier resolves, but the resolved work does not match the claimed reference.'})
        elif r['verdict'] in {'AMBIGUOUS','UNRESOLVED'}:
            actions.append({'severity':'REVIEW','citekey':citekey,'code':r['verdict'],'message':'Reference identity is not sufficiently established; do not auto-delete or label fabricated.'})
        if r.get('publication_status',{}).get('is_retracted') is True:
            actions.append({'severity':'CRITICAL','citekey':citekey,'code':'RETRACTED_FLAG','message':'Secondary metadata reports this work as retracted; verify against publisher/retraction notice before scientific use.'})
    for g in doi_dups:
        actions.append({'severity':'REVIEW','citekey':','.join(g['citekeys']),'code':'DUPLICATE_DOI','message':f"Same DOI appears under multiple citekeys: {g['doi']}. Determine whether these are duplicate records."})

    report = {
        'schema_version': '0.5.0',
        'generated_at': now_iso(),
        'input': {'path': str(bib_path), 'mode': 'offline' if ns.offline_dir else 'online', 'cache_enabled': cache_dir is not None},
        'summary': {
            'total_references': len(results),
            'verdict_counts': dict(sorted(counts.items())),
            'retracted_flags': sum(r.get('publication_status',{}).get('is_retracted') is True for r in results),
            'duplicate_doi_groups': len(doi_dups),
            'near_duplicate_title_pairs': len(title_dups),
            'human_review_records': sum(bool(r.get('requires_human_review')) for r in results),
            'cache_hits': cache_hits,
            'critical_actions': sum(a['severity']=='CRITICAL' for a in actions),
        },
        'duplicates': {'doi': doi_dups, 'title': title_dups},
        'actions': actions,
        'references': results,
        'policy': {'unresolved_is_not_fabricated': True, 'automatic_fabrication_confirmation': False, 'metadata_repairs_require_identity': True},
    }
    Path(ns.output_json).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    Path(ns.output_md).write_text(render_markdown(report), encoding='utf-8')
    print(f"Wrote {ns.output_json} and {ns.output_md}")
    if ns.fail_on_critical and report['summary']['critical_actions']:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
