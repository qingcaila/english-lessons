#!/usr/bin/env python3
"""套用 L2-pinyin R2(無 cap)結果到 vocab.json。"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
VOCAB = ROOT / "vocab.json"
SRC = ROOT / ".claude/skills/vocab-audit/reports/20260520-pinyin-R2-MERGED.json"
BACKUP = ROOT / ".claude/skills/vocab-audit/reports/20260520-pinyin-R2-PRE-APPLY-BACKUP.json"


def main():
    data = json.loads(VOCAB.read_text())
    words = data["words"]
    by_word = {w["word"]: w for w in words}
    proposals = json.loads(SRC.read_text())

    applied = []
    skipped = []
    backup = {}
    for p in proposals:
        word = p["word"].strip().lower()
        sug = p["suggested"].strip()
        if not word or not sug or word not in by_word:
            skipped.append((p.get("word"), "missing"))
            continue
        w = by_word[word]
        if w.get("py", "") == sug:
            skipped.append((word, "same"))
            continue
        backup[word] = w.get("py", "")
        w["py"] = sug
        applied.append({"word": word, "old": backup[word], "new": sug, "type": p.get("type")})

    VOCAB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    BACKUP.write_text(json.dumps(backup, ensure_ascii=False, indent=2))

    from collections import Counter
    types = Counter(a["type"] for a in applied)
    print(f"✓ R2 套用: {len(applied)} 字")
    print(f"⊘ 跳過: {len(skipped)}")
    print(f"\n類型: {dict(types.most_common())}")
    print(f"\n💾 R2 備份 → {BACKUP.name}")


if __name__ == "__main__":
    main()
