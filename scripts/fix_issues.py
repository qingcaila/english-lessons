"""修正全面審查發現的問題"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']

# ============ 1) 合併重複字 went/saw/said/took ============
# 邏輯:保留 sight-words 版本,把家族線資料合過去,刪掉後加的 actions 版本
DUP_KEEP_SIGHT = {'went','saw','said','took'}
to_remove = []
sight_idx = {}
actions_idx = {}
for i, w in enumerate(words):
    if w['word'] in DUP_KEEP_SIGHT:
        if w.get('theme') == 'sight-words':
            sight_idx[w['word']] = (i, w)
        elif w.get('theme') == 'actions':
            actions_idx[w['word']] = (i, w)

merged = 0
for word, (si, sw) in sight_idx.items():
    if word in actions_idx:
        ai, aw = actions_idx[word]
        # 把 actions 的 base/family-note 合到 sight-words
        if 'base' in aw:
            sw['base'] = aw['base']
            sw['family-note'] = aw.get('family-note','')
        to_remove.append(ai)
        merged += 1

# ============ 2) 修 base 指向不存在的字 ============
word_set = {w['word'] for w in words}
BAD_BASE_FIX = {
    'excited':    ('excite', None),   # excite 應該存在?如果沒,改 base 拿掉
    'professor':  ('profess', None),
    'especially': ('especial', None),
    'tore':       ('tear', None),
    'spectator':  ('spectate', None),
}
# 對於 base 指向不存在的,選項:
# A) 補上 base 字本身為新 vocab entry
# B) 把家族線 base 改成最接近的存在字 / 拿掉
# 簡單做法:新增 base 字

ADD_BASES = {
    'excite':    {'word':'excite','mean':'使興奮','img':'🤩','chunks':['ex','cite'],'py':'ㄧㄎ-ㄙㄞㄊ','split':'ex + cite','theme':'actions','stage':2},
    'profess':   {'word':'profess','mean':'公開承認、聲稱','img':'📢','chunks':['pro','fess'],'py':'ㄆㄖㄜ-ㄈㄝㄙ','split':'pro + fess','theme':'actions','stage':3},
    'especial':  {'word':'especial','mean':'特別的','img':'⭐','chunks':['e','spec','ial'],'py':'ㄧ-ㄙㄆㄝ-ㄒㄜ','split':'e + spec + ial','theme':'adjectives','stage':3},
    'tear':      {'word':'tear','mean':'撕 / 眼淚','img':'😢','chunks':['t','ear'],'py':'ㄊㄝ / ㄊㄧㄜ','split':'t + ear(兩義不同唸)','theme':'actions','stage':1},
    'spectate':  {'word':'spectate','mean':'觀看(運動賽事)','img':'👁️','chunks':['spec','tate'],'py':'ㄙㄆㄝㄎ-ㄊㄝㄊ','split':'spec + tate','theme':'actions','stage':3},
}
bases_added = 0
for w_name, entry in ADD_BASES.items():
    if w_name not in word_set:
        words.append(entry)
        bases_added += 1

# ============ 3) 修 預設 📦 emoji ============
IMG_FIX = {
    'bring':'🤲','empty':'🫙','thing':'🔵','stuff':'🧳','object':'🔷',
    'material':'🧱','package':'📦','deliver':'🚚','shipping':'🚛','parcel':'📦',
    'inventory':'📋','stock':'📦','wholesale':'🏭','itself':'🪞','brought':'🤲',
    'collecting':'🗃️','hoarding':'🗄️','archive':'🗄️','product':'📦','supply':'📦',
    'commodity':'💱','repository':'🗄️','repo':'🗄️','distribute':'📤','capacity':'🪣',
    'entity':'🏛️','comprise':'🔗','drop off':'📥','move in':'📦','move out':'📦',
}
# 還要加 2 個
imgs_fixed = 0
for w in words:
    if w.get('img') == '📦' and w['word'] in IMG_FIX:
        w['img'] = IMG_FIX[w['word']]
        imgs_fixed += 1

# ============ 4) 補短注音 ============
PY_FIX = {
    'eye': 'ㄞ',
    'a':   'ㄜ / ㄝ',
    'an':  'ㄢ / ㄝㄋ',
    'oh':  'ㄛ',
    'ah':  'ㄚ',
}
py_fixed = 0
for w in words:
    if w['word'] in PY_FIX:
        w['py'] = PY_FIX[w['word']]
        py_fixed += 1

# ============ 5) 真正刪除重複(從尾巴往前刪以保持索引)============
for i in sorted(to_remove, reverse=True):
    del words[i]

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"重複合併:    {merged} 組")
print(f"補 base 字:  {bases_added} 字")
print(f"修預設 img:  {imgs_fixed} 字")
print(f"修短注音:    {py_fixed} 字")
print(f"總字數:      {len(words)}")
