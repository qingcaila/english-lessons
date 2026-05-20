#!/usr/bin/env python3
"""還原 D 過度合併的 chunks(把單塊還原成原本的多塊)。

D 的 AI 過度套用「單音節用 vowel team 該整塊」,結果像
three/four/snow/play 這種教學常用字都被改成單塊,失去 phonics
教學價值。從 PRE-APPLY-BACKUP.json 還原。
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
VOCAB = ROOT / "vocab.json"
BACKUP = ROOT / ".claude/skills/vocab-audit/reports/20260520-chunks-phonics-PRE-APPLY-BACKUP.json"

# 不規則白名單(L1-chunks-single 認可的單塊)
SINGLE_OK = {
    'a','I','an','as','at','be','by','do','go','he','if','in','is','it',
    'me','my','no','of','on','or','so','to','up','us','we','am','off','out',
    'one','two','eight','ice','eye','ear','arm','egg','our','hour','knee','knight',
    'know','knife','knew','knock','knot','wrong','wrap','wrote','write','answer',
    'the','you','she','his','her','him','its','was','are','for','not','but','all',
    'can','had','has','did',
}

vocab = json.loads(VOCAB.read_text())
backup = json.loads(BACKUP.read_text())
by_w = {w['word']: w for w in vocab['words']}

restored = []
for word, w in by_w.items():
    if len(w.get('chunks', [])) > 1: continue
    if word in SINGLE_OK: continue
    if word not in backup: continue
    bk = backup[word]
    if len(bk.get('chunks', [])) > 1:
        w['chunks'] = bk['chunks']
        w['split'] = bk['split']
        restored.append(word)

VOCAB.write_text(json.dumps(vocab, ensure_ascii=False, indent=2) + '\n')
print(f"✓ 還原 {len(restored)} 字回多塊 chunks + 原 split 規則註")
print(f"\n範例: {', '.join(restored[:15])}")
