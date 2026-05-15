"""跑全部 Layer 1 機器規則檢查,印報告"""
import json, os, sys, io, hashlib, re
from collections import Counter
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
VOCAB = os.path.join(ROOT, 'vocab.json')
THEMES = os.path.join(ROOT, 'themes.json')
HISTORY = os.path.normpath(os.path.join(HERE, '..', 'history.json'))
REPORTS = os.path.normpath(os.path.join(HERE, '..', 'reports'))

with open(VOCAB, 'r', encoding='utf-8') as f: data = json.load(f)
with open(THEMES, 'r', encoding='utf-8') as f: th = json.load(f)
words = data['words']
word_set = {w['word'] for w in words}
theme_ids = {t['id'] for t in th['themes']}

REQUIRED = ['word','mean','img','chunks','py','split','theme','stage']
SINGLE_CHUNK_OK = {
    'a','I','an','as','at','be','by','do','go','he','if','in','is','it',
    'me','my','no','of','on','or','so','to','up','us','we','am','off','out',
    'one','two','eight','ice','eye','ear','arm','egg','our','hour','knee','knight',
    'know','knife','knew','knock','knot','wrong','wrap','wrote','write','answer',
    'the','you','she','his','her','him','its','was','are','for','not','but','all',
    'can','had','has','did',
}

results = {}

# 1) 必要欄位缺失
miss = {k: [] for k in REQUIRED}
empty = {k: [] for k in REQUIRED}
for w in words:
    for k in REQUIRED:
        if k not in w: miss[k].append(w.get('word','?'))
        elif w[k] in (None,'',[],{}): empty[k].append(w.get('word','?'))
results['L1-fields-missing'] = {k:v for k,v in miss.items() if v}
results['L1-fields-empty'] = {k:v for k,v in empty.items() if v}

# 2) theme 不存在
results['L1-theme-invalid'] = [w['word'] for w in words if w.get('theme') and w['theme'] not in theme_ids]

# 3) stage 不在 0-4
results['L1-stage-invalid'] = [w['word'] for w in words if w.get('stage') not in (0,1,2,3,4)]

# 4) chunks 違規
results['L1-chunks-single'] = [w['word'] for w in words
    if isinstance(w.get('chunks'), list) and len(w['chunks'])<2 and w['word'] not in SINGLE_CHUNK_OK]

# 5) img 預設 📦
results['L1-img-default'] = [w['word'] for w in words if w.get('img') == '📦']

# 6) 注音空 / 過短(<2 不算問題,因為單音字本來就短)
results['L1-pinyin-empty'] = [w['word'] for w in words if not w.get('py')]

# 7) 重複 word
c = Counter(w['word'] for w in words)
results['L1-duplicates'] = [(w,n) for w,n in c.items() if n>1]

# 8) base 斷鏈
results['L1-base-orphan'] = [(w['word'], w['base']) for w in words
    if 'base' in w and w['base'] not in word_set and w['base'] != w['word']]

# 9) mean 含亂符號 []+={}
results['L1-mean-weird-chars'] = [w['word'] for w in words
    if w.get('mean') and re.search(r'[\[\]<>{}@#$%^&*=+|\\]', w['mean'])]

# 10) mean 為純英文
results['L1-mean-pure-en'] = [w['word'] for w in words
    if w.get('mean') and re.fullmatch(r'[a-zA-Z\s\-]+', w['mean'])]

# 11) mean 跟 word 相同
results['L1-mean-equals-word'] = [w['word'] for w in words if w.get('mean') == w.get('word')]

# 12) homophone-note 格式錯(沒以 ⚠️ 開頭)
results['L1-homo-malformed'] = [w['word'] for w in words
    if 'homophone-note' in w and not w['homophone-note'].startswith('⚠️')]

# 13) family-note 沒搭配 base
results['L1-family-note-orphan'] = [w['word'] for w in words
    if 'family-note' in w and 'base' not in w]

# 報告
print("="*60)
print(f"Layer 1 機器規則檢查報告 — {datetime.now().isoformat(timespec='seconds')}")
print("="*60)
total_issues = 0
for check_id, lst in results.items():
    n = len(lst) if isinstance(lst, list) else sum(len(v) for v in lst.values())
    total_issues += n
    status = '✅' if n == 0 else '⚠️'
    print(f"{status} {check_id:30s}: {n}")
    if 0 < n <= 10:
        if isinstance(lst, list):
            for item in lst[:10]:
                print(f"    {item}")
        else:
            for k, v in lst.items():
                print(f"    {k}: {v[:5]}")

print()
print(f"總字數: {len(words)}")
print(f"有 base: {sum(1 for w in words if 'base' in w)}")
print(f"有 homophone: {sum(1 for w in words if 'homophone-note' in w)}")
print(f"總異常: {total_issues}")

# 寫 report
os.makedirs(REPORTS, exist_ok=True)
date = datetime.now().strftime('%Y-%m-%d-%H%M%S')
report_path = os.path.join(REPORTS, f'{date}-L1.md')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(f"# Layer 1 Audit — {datetime.now().isoformat(timespec='seconds')}\n\n")
    f.write(f"- 總字數: {len(words)}\n")
    f.write(f"- 總異常: {total_issues}\n\n")
    f.write("## 結果\n\n")
    for check_id, lst in results.items():
        n = len(lst) if isinstance(lst, list) else sum(len(v) for v in lst.values())
        status = '✅' if n == 0 else '⚠️'
        f.write(f"- {status} **{check_id}**: {n}\n")
        if n > 0 and isinstance(lst, list):
            for item in lst[:30]:
                f.write(f"  - `{item}`\n")
            if len(lst) > 30:
                f.write(f"  - ...還有 {len(lst)-30}\n")
print(f"\nReport: {report_path}")

# 更新 history
def hash_vocab():
    with open(VOCAB, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

if os.path.exists(HISTORY):
    with open(HISTORY, 'r', encoding='utf-8') as f:
        h = json.load(f)
else:
    h = {"vocab_hash_current": "", "checks": {}}

vh = hash_vocab()
h['vocab_hash_current'] = vh
h['checks']['L1-all'] = {
    'last_run': datetime.now().isoformat(timespec='seconds'),
    'vocab_hash': vh,
    'vocab_count': len(words),
    'issues_total': total_issues,
    'report': os.path.relpath(report_path, os.path.dirname(HISTORY)).replace('\\','/'),
}
with open(HISTORY, 'w', encoding='utf-8') as f:
    json.dump(h, f, ensure_ascii=False, indent=2)
print(f"history.json 已更新")
