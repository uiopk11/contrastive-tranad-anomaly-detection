"""Print saved historical stdout without importing model dependencies."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
print('Historical source outputs only; not rerun. Read docs/evaluation.md before comparison.')
for name in ('02_frozen_cl_wadi', '03_joint_cl_negative_case', '04_frozen_cl_smap'):
    p = ROOT / 'results/historical' / (name + '.json')
    record = json.loads(p.read_text(encoding='utf-8'))
    print('\n' + record['notebook'])
    for row in record['outputs']:
        text = row['stdout']
        if any(marker in text for marker in ('CL(', '最优', 'best alpha', 'Final best alpha', 'CL POT')):
            print(text)
