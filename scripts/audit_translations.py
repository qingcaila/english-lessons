"""翻譯品質審查 — 找可疑 / 怪怪的 mean"""
import json, os, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']

# 1) mean 太短(< 2 字)
too_short = [w for w in words if w.get('mean') and len(w['mean']) < 2]

# 2) mean 為純英文(沒翻譯到)
pure_en = [w for w in words if w.get('mean') and re.fullmatch(r'[a-zA-Z\s\-]+', w['mean'])]

# 3) mean 含英文括號註解(可能直接機翻)
has_en_paren = [w for w in words if w.get('mean') and re.search(r'\([a-zA-Z]', w['mean'])]

# 4) mean 太長(> 20 字)— 可能是定義而非翻譯
too_long = [w for w in words if w.get('mean') and len(w['mean']) > 20]

# 5) mean 開頭是「一個」「一種」「某種」(機翻特徵)
generic_start = [w for w in words if w.get('mean','').startswith(('一個','一種','某種','某個','一份','的'))]

# 6) mean 含全形/半形混雜的怪符號
weird_chars = []
for w in words:
    m = w.get('mean','')
    if re.search(r'[\[\]<>{}@#$%^&*=+|\\]', m):
        weird_chars.append(w)

# 7) mean 跟 word 完全一樣(沒翻)
not_translated = [w for w in words if w.get('mean') == w.get('word')]

# 8) mean 看起來是另一個英文字(可能是同義詞而非翻譯)
suspicious_en_only = []
for w in words:
    m = w.get('mean','')
    if m and re.match(r'^[a-zA-Z]+$', m) and len(m) < 15:
        suspicious_en_only.append(w)

# 9) mean 含日文 / 韓文 / 其他亂碼
non_cjk = []
for w in words:
    m = w.get('mean','')
    if re.search(r'[぀-ゟ゠-ヿ가-힯]', m):  # 日文假名 / 韓文
        non_cjk.append(w)

# 10) mean 含逗號分隔的「同義詞列表」可能太繁
many_synonyms = [w for w in words if w.get('mean','').count(',') >= 3 or w.get('mean','').count('，') >= 3]

# 11) mean 有「(過去)」「(現在)」之類但沒搭配 base — 可能漏標家族線
tense_mark = [w for w in words
              if re.search(r'\((過去|過去式|現在|現在式|p\.p\.|進行|複數|比較|最高)\)', w.get('mean',''))
              and 'base' not in w]

# 報告
def show(title, lst, n=20):
    print(f"\n=== {title} ({len(lst)}) ===")
    for w in lst[:n]:
        print(f"  {w['word']:25s} | {w.get('mean','')}")
    if len(lst) > n:
        print(f"  ... 還有 {len(lst)-n} 字")

show("1) mean < 2 字", too_short, 30)
show("2) mean 為純英文(沒翻譯)", pure_en, 30)
show("3) mean 含英文括號註解", has_en_paren, 30)
show("4) mean > 20 字(可能太冗長)", too_long, 30)
show("5) 機翻特徵開頭(一個/一種/某種)", generic_start, 30)
show("6) 含怪符號 []<>{} 等", weird_chars, 30)
show("7) mean = word(沒翻)", not_translated, 30)
show("8) mean 純英文短字(可能同義詞而非翻譯)", suspicious_en_only, 50)
show("9) mean 含日韓文字", non_cjk, 30)
show("10) mean 含 3+ 個逗號分隔", many_synonyms, 30)
show("11) 有時態標記但沒 base(漏家族線)", tense_mark, 50)
