"""顯示所有 check 的進度狀態 — 上次跑時間 / vocab 改了沒 / 建議跑哪些"""
import json, os, sys, io, hashlib
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.normpath(os.path.join(HERE, '..'))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
VOCAB = os.path.join(ROOT, 'vocab.json')
HISTORY = os.path.join(SKILL, 'history.json')
PROMPTS = os.path.join(SKILL, 'prompts')

# 所有「該存在」的 check(SKILL.md 定義的完整清單)
ALL_CHECKS = [
    ('L1-all',                       '機器規則 14 項',           '秒級', True),
    ('L1-silent-letter',             '不發音字母規則式偵測',     '秒級', True),
    ('L2-translation',               '翻譯品質',                 '分鐘',  True),
    ('L2-family-potential',          '找漏網家族線',             '分鐘',  True),
    ('L2-homophone-potential',       '找漏網同音/易混字',         '分鐘',  True),
    ('L2-emoji-fit',                 'emoji 配字義',             '分鐘',  True),
    ('L2-theme-fit',                 '主題分類合理性',           '分鐘',  True),
    ('L2-chunks-phonics',            'chunks 拆法符合 phonics',  '分鐘',  True),
    ('L2-pinyin',                    '注音準度',                 '分鐘',  True),
    ('L2-stage-fit',                 'stage 分級合理性',         '分鐘',  True),
    ('L2-pos-consistency',           '詞性一致(形容詞「的」)',  '分鐘',  True),
    ('L2-family-note-consistency',   'family-note 跟 mean/base 一致','分鐘',  True),
    ('L2-modernization',             '中國用語 / 過時詞',        '分鐘',  True),
    ('L2-tip-coverage',              '不規則字漏標 💡',          '分鐘',  True),
]

# 讀當前 hash + history
with open(VOCAB, 'rb') as f:
    current_hash = hashlib.sha256(f.read()).hexdigest()

with open(VOCAB, 'r', encoding='utf-8') as f:
    import json as _j
    current_count = len(_j.load(f)['words'])

if os.path.exists(HISTORY):
    with open(HISTORY, 'r', encoding='utf-8') as f:
        h = json.load(f)
else:
    h = {'checks': {}}

last_recorded_hash = h.get('vocab_hash_current', '')
checks_history = h.get('checks', {})

print("="*70)
print(f"vocab-audit 進度狀態 — {datetime.now().isoformat(timespec='seconds')}")
print("="*70)
print(f"當前 vocab.json:  {current_count} 字 / hash {current_hash[:12]}...")
if last_recorded_hash:
    same = current_hash == last_recorded_hash
    print(f"上次紀錄 hash:    {last_recorded_hash[:12]}... {'✓ 一致' if same else '⚠️  已變動'}")
else:
    print(f"上次紀錄 hash:    (從未跑過)")
print()
print(f"{'Check ID':<35} {'狀態':<12} {'上次跑':<22} {'結果'}")
print("-"*92)

need_rerun = []
never_run = []
for check_id, desc, speed, has_prompt in ALL_CHECKS:
    rec = checks_history.get(check_id)
    if not rec:
        status = '⚪ 從未跑'
        date = '-'
        result = '-'
        if has_prompt:
            never_run.append((check_id, desc))
    else:
        date = rec.get('last_run', '-')[:19]
        issues = rec.get('issues_found', rec.get('issues_total', '?'))
        fixes = rec.get('fixes_applied', 0)
        if rec.get('vocab_hash') == current_hash:
            status = '✅ 仍有效'
            result = f"{issues} issue / 修 {fixes}"
        else:
            status = '🟡 已過期'
            result = f"{issues} issue / 修 {fixes}"
            if has_prompt:
                need_rerun.append((check_id, desc))
    has_p = '' if has_prompt else ' (prompt 未寫)'
    print(f"{check_id:<35} {status:<12} {date:<22} {result}{has_p}")

print()
print("="*70)
print("建議")
print("="*70)
if not last_recorded_hash:
    print("⚠️  從未跑過任何 check,建議先跑 L1-all 看基本狀態")
elif current_hash == last_recorded_hash and not need_rerun and not never_run:
    print("✅ 全部 check 都是最新狀態,vocab 沒變動,不用重跑")
else:
    if need_rerun:
        print(f"🟡 vocab 變動了,以下 check 結果已過期,建議重跑:")
        for cid, desc in need_rerun:
            print(f"   - {cid}  ({desc})")
    if never_run:
        print(f"⚪ 以下 check 從未跑過:")
        for cid, desc in never_run:
            print(f"   - {cid}  ({desc})")

print()
print("觸發語(跟 Claude 講)")
print("-"*70)
print("  - 跑檢查 / 跑 audit  → 走完整流程,我會問你跑哪些")
print("  - 跑 L1 / 跑機器檢查 → 只跑 Layer 1(秒級)")
print("  - 跑家族線檢查       → 只跑 L2-family-potential")
print("  - 跑翻譯檢查         → 只跑 L2-translation")
print("  - 看狀態 / 看紀錄    → 跑這個 script 給你看")
