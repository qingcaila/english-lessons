#!/usr/bin/env python3
"""套用 L2-chunks-phonics 結果。

策略:
- 更新 chunks 欄位
- 同時 regen split 為簡單「chunk1 + chunk2」格式
  (失去原 split 的 (CVC)/(silent-e) 等 phonics 規則註,可後續再 audit 補回)
- 原 chunks + split 都備份
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
VOCAB = ROOT / "vocab.json"
SRC = ROOT / ".claude/skills/vocab-audit/reports/20260520-chunks-phonics-MERGED.json"
BACKUP = ROOT / ".claude/skills/vocab-audit/reports/20260520-chunks-phonics-PRE-APPLY-BACKUP.json"

data = json.loads(VOCAB.read_text())
by_word = {w["word"]: w for w in data["words"]}
proposals = json.loads(SRC.read_text())

applied, skipped, backup = [], [], {}
for p in proposals:
    word = p.get("word", "").strip().lower()
    sug = p.get("suggested", [])
    if not word or not isinstance(sug, list) or not sug or word not in by_word:
        skipped.append(word); continue
    w = by_word[word]
    if w.get("chunks") == sug:
        skipped.append(word); continue
    backup[word] = {"chunks": w.get("chunks"), "split": w.get("split", "")}
    w["chunks"] = sug
    # Regen split:簡單 "chunk1 + chunk2"
    w["split"] = " + ".join(sug)
    applied.append({"word": word, "chunks_old": backup[word]["chunks"],
                    "chunks_new": sug, "split_old": backup[word]["split"]})

VOCAB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
BACKUP.write_text(json.dumps(backup, ensure_ascii=False, indent=2))
print(f"✓ D chunks 套用: {len(applied)} 字 / 跳過 {len(skipped)}")
print(f"⚠️  split 同步 regen 為簡單格式(失去 phonics 規則註)")
print(f"💾 備份 → {BACKUP.name}")
