"""Static checks only. Does not execute training or install dependencies."""
from pathlib import Path
import ast
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def verify():
    errors, warnings = [], []
    files = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts]
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        if p.suffix.lower() in {'.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xlsx', '.npy', '.npz', '.ckpt', '.pub', '.zip'}:
            errors.append(f'Unexpected publication file: {rel}')
        if p.suffix == '.py':
            try:
                ast.parse(p.read_text(encoding='utf-8-sig'))
            except SyntaxError as e:
                errors.append(f'{rel}: {e}')
        if p.suffix == '.ipynb':
            nb = json.loads(p.read_text(encoding='utf-8'))
            for i, c in enumerate(nb['cells']):
                if c.get('outputs') or c.get('execution_count') is not None or c.get('attachments'):
                    errors.append(f'{rel}:{i} contains outputs, execution count or attachments')
                if c['cell_type'] == 'code':
                    try:
                        ast.parse(''.join(c['source']))
                    except SyntaxError as e:
                        errors.append(f'{rel}:{i}: {e}')
        if p.suffix == '.md':
            for link in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
                if '://' not in link and not link.startswith('#'):
                    if not (p.parent / link.split('#')[0]).exists():
                        errors.append(f'{rel}: missing link {link}')
        if p.suffix in {'.py', '.ipynb', '.md', '.json', '.csv', '.txt'}:
            content = p.read_text(encoding='utf-8-sig')
            # Pattern fragments avoid embedding forbidden personal identifiers here.
            if re.search(r'[A-Za-z]:[\\/](?:code_in_vs|Users[\\/])', content, re.I):
                errors.append(f'{rel}: personal absolute path')
            for term in ('\u6bd5\u4e1a\u8bbe\u8ba1', '\u6bd5\u8bbe', '\u9648\u90b1\u6db5', '092290' + '122'):
                if term in content:
                    errors.append(f'{rel}: excluded personal/project label')
            if re.search(r'-----BEGIN (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}', content):
                errors.append(f'{rel}: possible credential')
    manifest = json.loads((ROOT / 'docs/source_manifest.json').read_text(encoding='utf-8'))
    for row in manifest['files']:
        p = ROOT / row['path']
        if not p.is_file():
            errors.append(f'Missing manifest file: {row["path"]}')
        elif row['transformation'].startswith('byte-identical'):
            actual = hashlib.sha256(p.read_bytes()).hexdigest()
            if actual != row['source_sha256']:
                errors.append(f'Source hash differs: {row["path"]}')
    for p in (ROOT / 'results/exploratory').glob('*eval_summary.csv'):
        with p.open(encoding='utf-8-sig', newline='') as f:
            for row in csv.DictReader(f):
                tp, fp, fn = (float(row[k]) for k in ('TP', 'FP', 'FN'))
                precision = tp / (tp + fp) if tp + fp else 0
                recall = tp / (tp + fn) if tp + fn else 0
                f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
                for key, actual in [('Precision', precision), ('Recall', recall), ('F1', f1)]:
                    if abs(float(row[key]) - actual) > 1e-3:
                        warnings.append(f'{p.name}: {row["Setting"]} {key} conflicts with confusion counts')
    for w in warnings:
        print('KNOWN EXPLORATORY WARNING:', w)
    for e in errors:
        print('ERROR:', e)
    print(f'Checked {len(files)} files; {len(errors)} errors; {len(warnings)} exploratory warnings.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(verify())
