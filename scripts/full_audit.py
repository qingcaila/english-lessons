"""全面審查 vocab.json 資料完整性"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
THEMES = os.path.normpath(os.path.join(HERE, '..', 'themes.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
with open(THEMES,'r',encoding='utf-8') as f: th=json.load(f)
words=data['words']
theme_ids={t['id'] for t in th['themes']}

# 1) 必要欄位缺失
REQUIRED = ['word','mean','img','chunks','py','split','theme','stage']
missing = {k:[] for k in REQUIRED}
empty = {k:[] for k in REQUIRED}
for w in words:
    for k in REQUIRED:
        if k not in w:
            missing[k].append(w.get('word','?'))
        elif w[k] in (None,'',[],{}):
            empty[k].append(w.get('word','?'))

print("=== 1) 必要欄位缺失 ===")
for k,v in missing.items():
    if v: print(f"  缺 {k}: {len(v)} 字 — 前 10: {v[:10]}")
print("=== 必要欄位空值 ===")
for k,v in empty.items():
    if v: print(f"  空 {k}: {len(v)} 字 — 前 10: {v[:10]}")

# 2) theme 不存在於 themes.json
bad_theme = [w['word'] for w in words if w.get('theme') and w['theme'] not in theme_ids]
print(f"\n=== 2) theme 不在 themes.json: {len(bad_theme)} 字 ===")
if bad_theme: print(f"  {bad_theme[:20]}")

# 3) stage 不在 0-4
bad_stage = [w['word'] for w in words if w.get('stage') not in (0,1,2,3,4)]
print(f"\n=== 3) stage 不在 0-4: {len(bad_stage)} 字 ===")
if bad_stage: print(f"  {bad_stage[:20]}")

# 4) chunks 違規(單塊但不在白名單)
SINGLE_OK = {'a','I','an','as','at','be','by','do','go','he','if','in','is','it',
    'me','my','no','of','on','or','so','to','up','us','we','am','off','out',
    'one','two','eight','ice','eye','ear','arm','egg','our','hour','knee','knight',
    'know','knife','knew','knock','knot','wrong','wrap','wrote','write','answer',
    'the','you','she','his','her','him','its','was','are','for','not','but','all',
    'can','had','has','did'}
chunks_bad = [w['word'] for w in words
              if isinstance(w.get('chunks'),list) and len(w['chunks'])<2
              and w['word'] not in SINGLE_OK]
print(f"\n=== 4) chunks 單塊但非白名單: {len(chunks_bad)} 字 ===")
if chunks_bad: print(f"  {chunks_bad[:30]}")

# 5) img 用 📦 預設值(沒挑對應 emoji)
default_img = [w['word'] for w in words if w.get('img')=='📦']
print(f"\n=== 5) img 仍是預設 📦: {len(default_img)} 字 ===")
if default_img: print(f"  前 30: {default_img[:30]}")

# 6) py 注音空 / 太短
short_py = [w['word'] for w in words if not w.get('py') or len(w.get('py',''))<2]
print(f"\n=== 6) 注音空或過短: {len(short_py)} 字 ===")
if short_py: print(f"  前 20: {short_py[:20]}")

# 7) 重複的 word
from collections import Counter
c = Counter(w['word'] for w in words)
dups = [(w,n) for w,n in c.items() if n>1]
print(f"\n=== 7) 重複 word: {len(dups)} 組 ===")
if dups: print(f"  {dups[:20]}")

# 8) base 指向不存在的字
bad_base = []
word_set = {w['word'] for w in words}
for w in words:
    if 'base' in w and w['base'] not in word_set and w['base']!=w['word']:
        bad_base.append((w['word'], w['base']))
print(f"\n=== 8) base 指向不存在的字: {len(bad_base)} 字 ===")
if bad_base: print(f"  {bad_base[:20]}")

# 9) 統計
print(f"\n=== 統計 ===")
print(f"總字數:      {len(words)}")
print(f"有 base:     {sum(1 for w in words if 'base' in w)}")
print(f"有 homophone:{sum(1 for w in words if 'homophone-note' in w)}")
# stage 分布
from collections import Counter
sc = Counter(w.get('stage') for w in words)
for s in sorted(sc): print(f"  stage {s}: {sc[s]}")
# theme 分布
tc = Counter(w.get('theme') for w in words)
print(f"\nTop 10 主題字數:")
for t,n in tc.most_common(10):
    print(f"  {t}: {n}")
print(f"\n字數最少的主題(可能要補):")
for t,n in sorted(tc.items(), key=lambda x:x[1])[:15]:
    print(f"  {t}: {n}")
