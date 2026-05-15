"""更新 history.json 紀錄某個 check 的執行結果"""
import json, os, sys, hashlib
from datetime import datetime

if len(sys.argv) < 3:
    print("用法: python update_history.py {check_id} {issues_found} [fixes_applied] [agent_count] [report_path]")
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
VOCAB = os.path.join(ROOT, 'vocab.json')
HISTORY = os.path.normpath(os.path.join(HERE, '..', 'history.json'))

check_id = sys.argv[1]
issues = int(sys.argv[2])
fixes = int(sys.argv[3]) if len(sys.argv) > 3 else 0
agents = int(sys.argv[4]) if len(sys.argv) > 4 else 0
report = sys.argv[5] if len(sys.argv) > 5 else None

with open(VOCAB, 'rb') as f:
    vh = hashlib.sha256(f.read()).hexdigest()

if os.path.exists(HISTORY):
    with open(HISTORY, 'r', encoding='utf-8') as f:
        h = json.load(f)
else:
    h = {"vocab_hash_current": "", "checks": {}}

import json as _j
with open(VOCAB, 'r', encoding='utf-8') as f:
    data = _j.load(f)

h['vocab_hash_current'] = vh
entry = {
    'last_run': datetime.now().isoformat(timespec='seconds'),
    'vocab_hash': vh,
    'vocab_count': len(data['words']),
    'issues_found': issues,
    'fixes_applied': fixes,
}
if agents: entry['agent_count'] = agents
if report: entry['report'] = report
h['checks'][check_id] = entry

with open(HISTORY, 'w', encoding='utf-8') as f:
    json.dump(h, f, ensure_ascii=False, indent=2)
print(f"✅ 更新 history.json: {check_id}")
