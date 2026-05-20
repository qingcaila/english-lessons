#!/usr/bin/env python3
"""套用 L2-pinyin AI 全字審查結果到 vocab.json。

讀 reports/20260520-pinyin-FILTERED.json,把 suggested py 寫入。
保留原 py 在 reports 內供回滾。
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
VOCAB = ROOT / "vocab.json"
FILTERED = ROOT / ".claude/skills/vocab-audit/reports/20260520-pinyin-FILTERED.json"
BACKUP_PY = ROOT / ".claude/skills/vocab-audit/reports/20260520-pinyin-PRE-APPLY-BACKUP.json"


def main():
    data = json.loads(VOCAB.read_text())
    words = data["words"]
    by_word = {w["word"]: w for w in words}
    proposals = json.loads(FILTERED.read_text())

    applied = []
    skipped = []
    backup = {}  # word -> original py

    for p in proposals:
        word = p.get("word", "").strip().lower()
        sug = p.get("suggested", "").strip()
        if not word or not sug:
            skipped.append((p.get("word", ""), "empty suggested"))
            continue
        if word not in by_word:
            skipped.append((word, "not in vocab"))
            continue
        w = by_word[word]
        old_py = w.get("py", "")
        if old_py == sug:
            skipped.append((word, "already same"))
            continue
        backup[word] = old_py
        w["py"] = sug
        applied.append({
            "word": word,
            "old": old_py,
            "new": sug,
            "type": p.get("type", "?"),
            "reason": p.get("reason", ""),
        })

    # 寫回
    VOCAB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    BACKUP_PY.write_text(json.dumps(backup, ensure_ascii=False, indent=2))

    from collections import Counter
    type_dist = Counter(it["type"] for it in applied)

    print(f"=== 套用結果 ===")
    print(f"✓ 修改 py 欄位: {len(applied)} 字")
    if skipped:
        print(f"⊘ 跳過: {len(skipped)}")
        for w, r in skipped[:5]:
            print(f"    {w}: {r}")
    print()
    print(f"=== 套用類型分佈 ===")
    for t, c in type_dist.most_common():
        print(f"  {t:18s} {c:>4d}")
    print()
    print(f"💾 原 py 備份在 {BACKUP_PY.name}(萬一要回滾用)")


if __name__ == "__main__":
    main()
