#!/usr/bin/env python3
"""統一套用 E 所有 audit 結果。

優先順序(若多 check 改同欄位,後面蓋前面):
1. modernization (高品質,優先)
2. pos-consistency
3. translation (品質中等,放最後)
"""
import json
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).parent.parent
VOCAB = ROOT / "vocab.json"
REPORTS = ROOT / ".claude/skills/vocab-audit/reports"
BACKUP = REPORTS / "20260520-E-PRE-APPLY-BACKUP.json"

data = json.loads(VOCAB.read_text())
by_word = {w["word"]: w for w in data["words"]}

# 完整備份
backup = {}
def snapshot(word):
    if word not in backup and word in by_word:
        w = by_word[word]
        backup[word] = {k: w.get(k) for k in ['mean', 'theme', 'stage', 'base', 'family-note', 'note']}

stats = Counter()

# 1. modernization
items = json.loads((REPORTS / "20260520-modernization-FULL.json").read_text())
for p in items:
    w = p.get("word", "").strip().lower()
    sug = p.get("suggested", "").strip()
    if w in by_word and sug:
        snapshot(w)
        by_word[w]["mean"] = sug
        stats["modernization"] += 1

# 2. tip-coverage(加 note)
items = json.loads((REPORTS / "20260520-tip-coverage-FULL.json").read_text())
for p in items:
    w = p.get("word", "").strip().lower()
    note = p.get("suggested_note", "").strip()
    if w in by_word and note and "note" not in by_word[w]:
        snapshot(w)
        by_word[w]["note"] = note
        stats["tip-coverage-note"] += 1

# 3. family-note-consistency
items = json.loads((REPORTS / "20260520-family-note-consistency-FULL.json").read_text())
for p in items:
    w = p.get("word", "").strip().lower()
    if w not in by_word: continue
    snapshot(w)
    if p.get("action") == "remove-base":
        by_word[w].pop("base", None)
        by_word[w].pop("family-note", None)
        stats["family-note-remove-fake"] += 1
    else:
        sug_note = p.get("suggested_note", "").strip()
        sug_base = p.get("suggested_base", "").strip()
        if sug_note:
            by_word[w]["family-note"] = sug_note
            stats["family-note-update"] += 1
        if sug_base:
            by_word[w]["base"] = sug_base
            stats["family-base-fix"] += 1

# 4. theme-fit
items = json.loads((REPORTS / "20260520-theme-fit-FULL.json").read_text())
for p in items:
    w = p.get("word", "").strip().lower()
    sug = p.get("suggested", "").strip()
    if w in by_word and sug:
        snapshot(w)
        by_word[w]["theme"] = sug
        stats["theme-fit"] += 1

# 5. stage-fit
for f in ["20260520-stage-fit-agent-1-batch-0-10.json", "20260520-stage-fit-agent-2-batch-11-20.json"]:
    items = json.loads((REPORTS / f).read_text())
    for p in items:
        w = p.get("word", "").strip().lower()
        sug = p.get("suggested_stage")
        if w in by_word and isinstance(sug, int):
            snapshot(w)
            by_word[w]["stage"] = sug
            stats["stage-fit"] += 1

# 6. family-potential(加 base + family-note)
for f in ["20260520-family-potential-agent-1-batch-0-10.json", "20260520-family-potential-agent-2-batch-11-20.json"]:
    items = json.loads((REPORTS / f).read_text())
    for p in items:
        w = p.get("word", "").strip().lower()
        base = p.get("base", "").strip()
        note = p.get("family-note", "").strip()
        if w in by_word and base in by_word and note:
            snapshot(w)
            by_word[w]["base"] = base
            by_word[w]["family-note"] = note
            stats["family-potential-add"] += 1

# 7. pos-consistency(改 mean)
for f in ["20260520-pos-consistency-agent-1-batch-0-10.json", "20260520-pos-consistency-agent-2-batch-11-20.json"]:
    items = json.loads((REPORTS / f).read_text())
    for p in items:
        w = p.get("word", "").strip().lower()
        sug = p.get("suggested_mean", "").strip()
        if w in by_word and sug:
            snapshot(w)
            by_word[w]["mean"] = sug
            stats["pos-consistency"] += 1

# 8. translation(改 mean,放最後)
for f in ["20260520-translation-agent-1-batch-0-6.json", "20260520-translation-agent-2-batch-7-13.json", "20260520-translation-agent-3-batch-14-20.json"]:
    items = json.loads((REPORTS / f).read_text())
    for p in items:
        w = p.get("word", "").strip().lower()
        sug = p.get("suggested", "").strip()
        # 過濾 — 跳過明顯無意義的(suggested 包含「OK」「skip」等)
        reason = p.get("reason", "").lower()
        if not sug or "ok" in reason and "保留" in reason: continue
        if w in by_word and sug != by_word[w].get("mean"):
            snapshot(w)
            by_word[w]["mean"] = sug
            stats["translation"] += 1

# 寫回
VOCAB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
BACKUP.write_text(json.dumps(backup, ensure_ascii=False, indent=2))

print(f"=== E 統一套用結果 ===")
for k, v in stats.most_common():
    print(f"  {k:30s} {v:>5d}")
print(f"  {'總計修改字數':30s} {len(backup):>5d}")
print(f"\n💾 備份 → {BACKUP.name}")
