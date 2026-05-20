#!/usr/bin/env python3
"""套用 L2-emoji-fit 結果。"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
VOCAB = ROOT / "vocab.json"
SRC = ROOT / ".claude/skills/vocab-audit/reports/20260520-emoji-fit-MERGED.json"
BACKUP = ROOT / ".claude/skills/vocab-audit/reports/20260520-emoji-fit-PRE-APPLY-BACKUP.json"

data = json.loads(VOCAB.read_text())
by_word = {w["word"]: w for w in data["words"]}
proposals = json.loads(SRC.read_text())

applied, skipped, backup = [], [], {}
for p in proposals:
    word = p.get("word", "").strip().lower()
    sug = p.get("suggested", "").strip()
    if not word or not sug or word not in by_word:
        skipped.append(word); continue
    w = by_word[word]
    if w.get("img", "") == sug:
        skipped.append(word); continue
    backup[word] = w.get("img", "")
    w["img"] = sug
    applied.append({"word": word, "old": backup[word], "new": sug})

VOCAB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
BACKUP.write_text(json.dumps(backup, ensure_ascii=False, indent=2))
print(f"✓ C emoji 套用: {len(applied)} 字 / 跳過 {len(skipped)}")
print(f"💾 備份 → {BACKUP.name}")
