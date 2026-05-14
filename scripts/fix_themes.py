"""修主題標錯的字(從 agent 翻譯品質審查回報彙整)"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
THEMES = os.path.normpath(os.path.join(HERE, '..', 'themes.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
with open(THEMES,'r',encoding='utf-8') as f: th=json.load(f)
words = data['words']
idx = {w['word']: w for w in words}
theme_ids = {t['id'] for t in th['themes']}

# 主題標錯修正(word: 應該的 theme)
THEME_FIX = {
    # 動詞被標形容詞
    'finish':    'actions',
    'drive':     'actions',
    'receive':   'actions',
    'deceive':   'actions',
    'resent':    'actions',
    'lament':    'actions',
    'flourish':  'actions',
    'thrive':    'actions',
    'commute':   'actions',
    'impress':   'actions',
    'represent': 'actions',
    'conclude':  'actions',
    'compose':   'actions',

    # 名詞 / 動詞被亂分主題
    'join':      'actions',       # 原 numbers
    'lily':      'nature',        # 原 numbers(百合花)
    'queen':     'people-jobs',   # 原 actions
    'speed':     'actions',       # 原 numbers
    'relieve':   'actions',       # 原 numbers
    'increase':  'actions',
    'lengthen':  'actions',
    'rid':       'actions',
    'relief':    'emotions',
    'cure':      'health',        # 原 law
    'dive':      'sports',        # 原 drinks
    'spit':      'actions',       # 原 drinks
    'spray':     'actions',       # 原 drinks
    'sweat':     'body',          # 原 drinks
    'pool':      'places',        # 原 drinks(游泳池)
    'dam':       'nature',        # 原 drinks(水壩)
    'ditch':     'places',        # 原 drinks(水溝)
    'catsup':    'food',          # 原 fruits

    # animals 主題的非動物
    'hook':      'tools',
    'impression':'academic-words',
    'motor':     'technology',
    'image':     'academic-words',
    'clue':      'academic-words',

    # actions 主題的非動作名詞
    'goods':     'business',
    'horizon':   'nature',

    # 其他
    'anything':  'sight-words',   # 原 directions
    'bloom':     'actions',       # 原 nature(開花是動詞)

    # 食物分類錯
    'honeydew':  'fruits',
    'yam':       'vegetables',
    'yuzu':      'fruits',
    'calamansi': 'fruits',

    # phonics-compound 但其實是普通字 — 略

    # 數字附近的雜字(從 batch_12 看到的)
    'loaf':      'food',
    'dime':      'money',
    'gallon':    'numbers',  # 度量單位,留 numbers
    'penny':     'money',
    'glance':    'actions',
    'handful':   'numbers',  # 一把,算數量詞
    'millionaire':'jobs',
    'someday':   'time',
    'sometime':  'time',
    'secondary': 'sight-words',
    'together':  'sight-words',
    'bang':      'actions',
}

applied = 0
not_found = []
bad_theme = []
for word, new_theme in THEME_FIX.items():
    if word not in idx:
        not_found.append(word)
        continue
    if new_theme not in theme_ids:
        bad_theme.append((word, new_theme))
        continue
    old = idx[word].get('theme','')
    if old == new_theme:
        continue
    idx[word]['theme'] = new_theme
    print(f"  {word:18s} {old:18s} → {new_theme}")
    applied += 1

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n已修: {applied}")
if not_found: print(f"找不到: {not_found}")
if bad_theme: print(f"主題不存在: {bad_theme}")
