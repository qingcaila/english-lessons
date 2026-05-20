"""L1-silent-letter:規則式偵測不發音字母漏標。

用法:
  python run_silent_letter.py            # detect-only,印報告 + 寫 reports/
  python run_silent_letter.py --apply    # detect + 寫入 vocab.json + update history

設計:
- 13 個 silent letter 分類群(k/w/b-mb/b-bt/l/h/gh/g/t/p/n/s/gh-f)
- 用 regex + whitelist 抓候選
- 已有 silent-letter 欄位的字一律跳過
- 漏標字寫成報告供 review
"""
import json, os, sys, io, re, hashlib
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.normpath(os.path.join(HERE, '..'))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
VOCAB = os.path.join(ROOT, 'vocab.json')
HISTORY = os.path.join(SKILL, 'history.json')
REPORTS = os.path.join(SKILL, 'reports')

# ── 偵測規則 ────────────────────────────────────────
SILENT_RULES = [
    ("k",      [r"^kn"]),                                     # kn-
    ("w",      [r"^wr"]),                                     # wr-
    ("b-mb",   [r"mb$"]),                                     # -mb
    ("g",      [r"^gn", r"gn$"]),                             # gn-/-gn
    ("t",      [r"stle", r"(sten|ften)$"]),                   # -stle/-sten/-ften
    ("p",      [r"^(ps|pn|pt)"]),                             # ps-/pn-/pt-
    ("n",      [r"mn$"]),                                     # -mn
    ("b-bt",   [r"bt(?:le)?(?:s|ly|ful|ed)?$"]),              # bt
    ("s",      [r"^(isl|aisl)"]),                             # isl/aisl
    ("gh",     [r"(igh|eigh|aught|ought)", r"ough"]),         # 但 ough/augh 有發 /f/ 的要排除
]

WHITELIST = {
    "l": {"walk", "talk", "chalk", "stalk", "calm", "palm", "balm", "psalm",
          "half", "calf", "yolk", "folk", "almond", "salmon", "should", "would", "could"},
    "h": {"hour", "honest", "honor", "honour", "heir", "heirloom", "herb", "rhyme",
          "rhythm", "ghost", "ghastly", "ghetto", "khaki", "vehicle", "shepherd",
          "exhaust", "exhibit", "honestly", "hourly"},
}

GH_AS_F_BASES = {"cough", "enough", "rough", "tough", "laugh", "laughter", "trough", "slough"}
def _is_gh_as_f(word):
    if word in GH_AS_F_BASES: return True
    for suffix in ["s", "ed", "ing", "ly", "ness", "er", "est"]:
        if word.endswith(suffix) and word[:-len(suffix)] in GH_AS_F_BASES:
            return True
    return False


def categorize(word):
    w = word.lower()
    for key, wl in WHITELIST.items():
        if w in wl: return key
    if _is_gh_as_f(w):
        return "gh-f"
    for key, patterns in SILENT_RULES:
        for pat in patterns:
            if re.search(pat, w, re.IGNORECASE):
                return key
    return None


LABELS = {
    "k":    "silent k (kn-)",
    "w":    "silent w (wr-)",
    "b-mb": "silent b (-mb)",
    "b-bt": "silent b (bt)",
    "l":    "silent l",
    "h":    "silent h",
    "gh":   "silent gh (igh/eigh/ough)",
    "g":    "silent g (gn)",
    "t":    "silent t (stle/sten)",
    "p":    "silent p (ps-/pn-)",
    "n":    "silent n (-mn)",
    "s":    "silent s (isl-)",
    "gh-f": "gh 唸 /f/ (不規則)",
}


def main():
    apply_mode = "--apply" in sys.argv

    with open(VOCAB, 'r', encoding='utf-8') as f:
        data = json.load(f)
    words = data['words']

    missing = []     # {word, mean, suggested_key}
    already = []
    correct = []     # 已標且符合規則
    mismatch = []    # 已標但跟規則不符 (人工或之前手動標的)

    for w in words:
        word = w['word']
        existing = w.get('silent-letter')
        suggested = categorize(word)
        if existing and suggested:
            if existing == suggested:
                correct.append(word)
            else:
                mismatch.append({'word': word, 'mean': w.get('mean', ''),
                                 'existing': existing, 'suggested': suggested})
        elif existing and not suggested:
            already.append({'word': word, 'mean': w.get('mean', ''), 'existing': existing})
        elif not existing and suggested:
            missing.append({'word': word, 'mean': w.get('mean', ''), 'suggested': suggested})

    # 報告
    print("="*70)
    print(f"L1-silent-letter — {datetime.now().isoformat(timespec='seconds')}")
    print("="*70)
    print(f"已正確標記:  {len(correct)} 字")
    print(f"漏標(待補): {len(missing)} 字 ← 主要 issue")
    print(f"已標但規則沒抓到: {len(already)} 字(可能是人工特例)")
    print(f"既有標籤跟規則不符: {len(mismatch)} 字")
    print()

    if missing:
        print("=== 漏標清單 ===")
        from collections import defaultdict
        by_key = defaultdict(list)
        for m in missing: by_key[m['suggested']].append(m)
        for key in LABELS:
            items = by_key.get(key, [])
            if items:
                print(f"\n[{LABELS[key]}] {len(items)} 字")
                for m in items[:10]:
                    print(f"  {m['word']:20s} {m['mean']}")
                if len(items) > 10:
                    print(f"  ... 另 {len(items)-10} 字")

    if mismatch:
        print("\n=== 標籤跟規則不符(可能誤標)===")
        for m in mismatch[:15]:
            print(f"  {m['word']:20s} 標 '{m['existing']}' 但規則建議 '{m['suggested']}'")

    # 寫 report
    os.makedirs(REPORTS, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    report_path = os.path.join(REPORTS, f"{today}-L1-silent-letter.json")
    report = {
        'check': 'L1-silent-letter',
        'run_at': datetime.now().isoformat(timespec='seconds'),
        'stats': {
            'correct': len(correct),
            'missing': len(missing),
            'already_unrule': len(already),
            'mismatch': len(mismatch),
        },
        'missing': missing,
        'mismatch': mismatch,
    }
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📄 報告已寫到 {report_path}")

    # Apply mode
    if apply_mode and missing:
        by_word = {w['word']: w for w in words}
        for m in missing:
            by_word[m['word']]['silent-letter'] = m['suggested']
        with open(VOCAB, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f"\n✅ Apply 模式:寫入 {len(missing)} 條 silent-letter 標籤到 vocab.json")
    elif missing:
        print(f"\n💡 要套用:python {os.path.basename(__file__)} --apply")
    else:
        print(f"\n✓ 沒有漏標,無需 apply。")

    # 不論有沒有 missing,只要跑了 detect 就更新 history
    # (這樣 show_status 可以看到 check 跑過 + vocab hash 對齊)
    if apply_mode or not missing:
        with open(VOCAB, 'rb') as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()
        if os.path.exists(HISTORY):
            with open(HISTORY, 'r', encoding='utf-8') as f:
                h = json.load(f)
        else:
            h = {'vocab_hash_current': '', 'checks': {}}
        h['vocab_hash_current'] = current_hash
        h['checks']['L1-silent-letter'] = {
            'last_run': datetime.now().isoformat(timespec='seconds'),
            'vocab_hash': current_hash,
            'issues_found': len(missing),
            'fixes_applied': len(missing) if apply_mode else 0,
            'tagged_total': len(correct) + (len(missing) if apply_mode else 0),
            'report': f"reports/{today}-L1-silent-letter.json",
        }
        with open(HISTORY, 'w', encoding='utf-8') as f:
            json.dump(h, f, ensure_ascii=False, indent=2)
        print(f"✅ history.json 更新")


if __name__ == "__main__":
    main()
