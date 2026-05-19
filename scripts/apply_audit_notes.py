#!/usr/bin/env python3
"""套用 vocab-audit L2-homophone-potential AI 全字掃描結果。

讀 .claude/skills/vocab-audit/reports/20260519-MERGED.json,
對 vocab.json 內、沒 homophone-note 的字寫入 note。
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
VOCAB = ROOT / "vocab.json"
MERGED = ROOT / ".claude/skills/vocab-audit/reports/20260519-MERGED.json"


def main():
    data = json.loads(VOCAB.read_text())
    words = data["words"]
    by_word = {w["word"]: w for w in words}
    proposals = json.loads(MERGED.read_text())

    added = []
    skipped_existing = []
    not_in_vocab = []
    skipped_empty_note = []

    for p in proposals:
        word = p.get("word", "").strip().lower()
        note = p.get("note", "").strip()
        if not word:
            continue
        if not note:
            skipped_empty_note.append(word)
            continue
        # 確保 note 以 ⚠️ 開頭
        if not note.startswith("⚠️"):
            note = "⚠️ " + note
        if word not in by_word:
            not_in_vocab.append(word)
            continue
        w = by_word[word]
        if "homophone-note" in w:
            skipped_existing.append(word)
            continue
        w["homophone-note"] = note
        added.append(word)

    # 寫回(保持 indent=2 格式)
    VOCAB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    # 報告
    print(f"=== 套用結果 ===")
    print(f"✓ 新增 note: {len(added)} 字")
    print(f"⊘ 跳過(已有 note): {len(skipped_existing)}")
    print(f"⚠ 跳過(不在 vocab): {len(not_in_vocab)}")
    if skipped_empty_note:
        print(f"⚠ 跳過(note 為空): {len(skipped_empty_note)}")
    print()
    if not_in_vocab[:10]:
        print(f"前 10 個不在 vocab 的字: {', '.join(not_in_vocab[:10])}")
    print()
    # 最終總覆蓋率
    total_tagged = sum(1 for w in words if "homophone-note" in w)
    pct = total_tagged / len(words) * 100
    print(f"=== vocab.json 最終 homophone-note 覆蓋 ===")
    print(f"    {total_tagged} / {len(words)} = {pct:.1f}%")


if __name__ == "__main__":
    main()
