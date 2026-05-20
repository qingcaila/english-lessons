#!/usr/bin/env python3
"""為 vocab.json 加 silent-letter 欄位 — 系統化標記不發音字母。

13 個分類群:
- k (kn-): knife, know
- w (wr-): write, wrong
- b-mb (-mb): lamb, climb
- b-bt (-bt-): debt, doubt
- l: walk, calm
- h: hour, honest
- gh: right, eight
- g (gn-/-gn): gnaw, sign
- t (-stle/-sten): castle, listen
- p (ps-/pn-): psychology
- n (-mn): autumn
- s (isl-): island
- gh-f (gh as /f/, 不規則): cough, enough
"""
import json
import re
from pathlib import Path

VOCAB = Path(__file__).parent.parent / "vocab.json"

# 精準分類規則
SILENT_RULES = [
    ("k",      r"^kn"),                     # kn-
    ("w",      r"^wr"),                     # wr-
    ("b-mb",   r"mb$"),                     # -mb
    ("g",      None,  # 兩種 gn pattern 都是 silent g
        [r"^gn", r"gn$"]),
    ("t",      None,  # -stle + -sten + -ften
        [r"stle", r"(sten|ften)$"]),
    ("p",      r"^(ps|pn|pt)"),            # ps-/pn-/pt-
    ("n",      r"mn$"),                     # -mn (n silent)
    ("b-bt",   r"bt(?:le)?(?:s|ly|ful|ed)?$"),  # bt
    ("s",      r"^(isl|aisl)"),            # isl/aisl
    ("gh",     None,                        # igh/eigh/ough/aught/ought (silent gh only)
        [r"(igh|eigh|aught|ought)", r"ough"]),  # 但 ough 要排除 /f/
]

# l(walk/calm)& h(hour)用 whitelist 避免誤報
WHITELIST = {
    "l": {"walk", "talk", "chalk", "stalk", "calm", "palm", "balm", "psalm",
          "half", "calf", "yolk", "folk", "almond", "salmon", "should", "would", "could"},
    "h": {"hour", "honest", "honor", "honour", "heir", "heirloom", "herb", "rhyme",
          "rhythm", "ghost", "ghastly", "ghetto", "khaki", "vehicle", "shepherd",
          "exhaust", "exhibit", "honestly", "hourly"},
}

# gh-as-f exclude list(這些 gh 唸 /f/,不算 silent)
GH_AS_F_BASES = {"cough", "enough", "rough", "tough", "laugh", "laughter", "trough", "slough"}
def is_gh_as_f(word):
    if word in GH_AS_F_BASES: return True
    for suffix in ["s", "ed", "ing", "ly", "ness", "er", "est"]:
        if word.endswith(suffix) and word[:-len(suffix)] in GH_AS_F_BASES:
            return True
    return False


def categorize(word):
    """回傳 silent-letter 分類 key,或 None"""
    w = word.lower()
    # whitelist 優先
    for key, wl in WHITELIST.items():
        if w in wl: return key

    # gh-as-f 特殊處理
    if is_gh_as_f(w):
        return "gh-f"

    # regex rules
    for entry in SILENT_RULES:
        key = entry[0]
        if len(entry) == 2:
            patterns = [entry[1]]
        else:
            patterns = entry[2]
        for pat in patterns:
            if re.search(pat, w, re.IGNORECASE):
                return key
    return None


def main():
    data = json.loads(VOCAB.read_text())
    words = data["words"]

    stats = {}
    added = 0
    skipped = 0
    for w in words:
        key = categorize(w["word"])
        if key:
            if "silent-letter" in w:
                skipped += 1
            else:
                w["silent-letter"] = key
                added += 1
            stats[key] = stats.get(key, 0) + 1

    VOCAB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    print("=== 寫入結果 ===")
    print(f"✓ 新增 silent-letter 標記: {added}")
    if skipped:
        print(f"⊘ 已有標記: {skipped}")
    print()
    print("=== 分類分佈 ===")
    LABELS = {
        "k":     "🤐 silent k (kn-)",
        "w":     "🤐 silent w (wr-)",
        "b-mb":  "🤐 silent b (-mb)",
        "b-bt":  "🤐 silent b (bt)",
        "l":     "🤐 silent l",
        "h":     "🤐 silent h",
        "gh":    "🤐 silent gh (igh/eigh/ough)",
        "g":     "🤐 silent g (gn)",
        "t":     "🤐 silent t (stle/sten)",
        "p":     "🤐 silent p (ps-/pn-)",
        "n":     "🤐 silent n (-mn)",
        "s":     "🤐 silent s (isl-)",
        "gh-f":  "🔉 gh 發 /f/(不規則)",
    }
    total = 0
    for k in LABELS:
        cnt = stats.get(k, 0)
        total += cnt
        print(f"  {LABELS[k]:35s} {cnt:>4d}")
    print(f"  {'總計':35s} {total:>4d}")


if __name__ == "__main__":
    main()
