"""套用 modernization 修正 — 中國用語 / 過時詞改成台灣用語"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

FIXES = {
    'data':          '資料',
    'identity':      '身分',
    'identitytheft': '身分盜用',
    'cassette':      '卡式錄音帶',
    'disco':         '迪斯可舞廳',
    'missile':       '飛彈',
    'feedback':      '回饋',
    'eq':            '情緒商數(EQ)',
    'subway':        '捷運',
    'podcaster':     'Podcast 主持人',
    'preworkout':    '運動前補給品',
    'postworkout':   '運動後補給品',
    'framerate':     '畫面更新率',
    'css':           '階層樣式表',
    'repository':    '程式儲存庫',
    'repo':          '程式儲存庫',
    'tiktok':        'TikTok',
    'cyclist':       '騎腳踏車的人',
    'username':      '使用者名稱',
    'mudslide':      '土石流',
}

n = 0
not_found = []
for word, new_mean in FIXES.items():
    if word not in idx:
        not_found.append(word)
        continue
    old = idx[word].get('mean','')
    if old == new_mean:
        continue
    idx[word]['mean'] = new_mean
    print(f"  {word:18s} | {old:25s} → {new_mean}")
    n += 1

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n已修: {n}")
if not_found: print(f"找不到: {not_found}")
