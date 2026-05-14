"""
審查 vocab.json:
1) 找拼字變化看起來像有 base 但沒標的(-ing / -ed / -er / -est / -ies)
2) 找常見不規則動詞過去式但沒標 base 的
3) 找常見同音字但沒標 homophone-note 的
4) 找 chunks 違規(只有一塊但不在已知不規則白名單)
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))

with open(VOCAB, 'r', encoding='utf-8') as f:
    data = json.load(f)

words = data['words']
word_set = {w['word'] for w in words}
idx = {w['word']: w for w in words}

# ---------- 1) 字尾候選(沒 base 的) ----------
SUFFIX_PATTERNS = [
    ('ing',  '-ing 結尾'),
    ('ed',   '-ed 結尾'),
    ('ies',  '-ies 結尾'),
    ('est',  '-est 結尾'),
    ('er',   '-er 結尾'),
]
# -er / -ing 等也可能是普通字(teacher / king),需要更聰明判斷
# 策略:若去掉字尾後,剩下的字也在 vocab 裡 → 高機率是家族成員

candidates_family = []
for w in words:
    if 'base' in w:
        continue
    word = w['word']
    if len(word) < 4:
        continue
    for suf, label in SUFFIX_PATTERNS:
        if not word.endswith(suf):
            continue
        # 嘗試各種還原
        stems_to_try = []
        if suf == 'ing':
            stems_to_try += [word[:-3]]  # walk+ing
            if len(word) >= 5 and word[-4] == word[-5] and word[-4] not in 'aeiou':
                stems_to_try.append(word[:-4])  # running→run
            stems_to_try.append(word[:-3] + 'e')  # making→make
        elif suf == 'ed':
            stems_to_try += [word[:-2], word[:-1]]  # walked/walk, used/use
            if len(word) >= 5 and word[-3] == word[-4] and word[-3] not in 'aeiou':
                stems_to_try.append(word[:-3])  # stopped→stop
            if word.endswith('ied'):
                stems_to_try.append(word[:-3] + 'y')  # studied→study
        elif suf == 'ies':
            stems_to_try.append(word[:-3] + 'y')  # cities→city
        elif suf == 'est':
            stems_to_try += [word[:-3], word[:-2] + 'e']
            if len(word) >= 5 and word[-4] == word[-5] and word[-4] not in 'aeiou':
                stems_to_try.append(word[:-4])
            if word.endswith('iest'):
                stems_to_try.append(word[:-4] + 'y')
        elif suf == 'er':
            stems_to_try += [word[:-2], word[:-1]]
            if len(word) >= 4 and word[-3] == word[-4] and word[-3] not in 'aeiou':
                stems_to_try.append(word[:-3])
            if word.endswith('ier'):
                stems_to_try.append(word[:-3] + 'y')
        for stem in stems_to_try:
            if stem and stem != word and stem in word_set:
                candidates_family.append((word, stem, label))
                break
        else:
            continue
        break

# ---------- 2) 已知不規則動詞補漏 ----------
KNOWN_IRREGULAR = {
    'sat': 'sit', 'sold': 'sell', 'sank': 'sink', 'sunk': 'sink',
    'spread': 'spread', 'split': 'split', 'cast': 'cast',
    'awoke': 'awake', 'bade': 'bid', 'bid': 'bid',
    'bound': 'bind', 'bred': 'breed', 'chose': 'choose',
    'clung': 'cling', 'crept': 'creep', 'shrank': 'shrink',
    'sprang': 'spring', 'stung': 'sting', 'strung': 'string',
    'sunk': 'sink', 'sworn': 'swear', 'swore': 'swear',
    'thrust': 'thrust', 'wove': 'weave', 'woven': 'weave',
    'wrung': 'wring', 'forbade': 'forbid', 'forgave': 'forgive',
    'forbid': 'forbid',
    # 過去分詞補一些
    'gone': 'go', 'done': 'do', 'seen': 'see', 'been': 'be',
    'taken': 'take', 'given': 'give', 'written': 'write',
    'spoken': 'speak', 'broken': 'break', 'chosen': 'choose',
    'driven': 'drive', 'ridden': 'ride', 'risen': 'rise',
    'fallen': 'fall', 'flown': 'fly', 'grown': 'grow',
    'known': 'know', 'thrown': 'throw', 'shown': 'show',
    'drawn': 'draw', 'worn': 'wear', 'torn': 'tear',
    'born': 'bear', 'beaten': 'beat',
    'began': 'begin', 'begun': 'begin', 'swum': 'swim',
    'sung': 'sing', 'rung': 'ring', 'drunk': 'drink',
    'sank': 'sink',
    # 拼字第三人稱單數
    'cries': 'cry', 'tries': 'try', 'flies': 'fly',
    'plays': 'play', 'goes': 'go', 'does': 'do',
    'has': 'have',
}
irregular_missing = []
for w_word, base in KNOWN_IRREGULAR.items():
    if w_word in idx and 'base' not in idx[w_word]:
        irregular_missing.append((w_word, base))

# ---------- 3) 常見同音字補漏 ----------
KNOWN_HOMOPHONES = [
    # word, twin, note
    ("you're", "your", "⚠️ 易混字:you're 你是(= you are)/ your 你的"),
    ("it's", "its", "⚠️ 易混字:it's 它是(= it is)/ its 牠的(所有格)"),
    ('they\'re', 'their / there', '⚠️ 同音字:they\'re 他們是(= they are)/ their 他們的 / there 在那裡'),
    ('won', 'one', '⚠️ 同音字:won win 的過去式 / one 一'),
    ('I', 'eye', '⚠️ 同音字:I 我 / eye 眼睛'),
    ('flour', 'flower', '⚠️ 同音字:flour 麵粉 / flower 花'),
    ('male', 'mail', '⚠️ 同音字:male 男性 / mail 郵件'),
    ('tale', 'tail', '⚠️ 同音字:tale 故事 / tail 尾巴'),
    ('meet', 'meat', '⚠️ 同音字:meet 見面 / meat 肉'),
    ('peace', 'piece', '⚠️ 同音字:peace 和平 / piece 一片'),
    ('week', 'weak', '⚠️ 同音字:week 一週 / weak 弱的'),
    ('weight', 'wait', '⚠️ 同音字:weight 重量 / wait 等'),
    ('blue', 'blew', '⚠️ 同音字:blue 藍色 / blew blow 的過去式'),
    ('blew', 'blue', '⚠️ 同音字:blew blow 的過去式 / blue 藍色'),
    ('new', 'knew', '⚠️ 同音字:new 新的 / knew know 的過去式(k 不發音)'),
    ('night', 'knight', '⚠️ 同音字:night 夜晚 / knight 騎士(k 不發音)'),
    ('knight', 'night', '⚠️ 同音字:knight 騎士(k 不發音)/ night 夜晚'),
    ('hour', 'our', '⚠️ 同音字:hour 小時(h 不發音)/ our 我們的'),
    ('our', 'hour', '⚠️ 同音字:our 我們的 / hour 小時(h 不發音)'),
    ('road', 'rode', '⚠️ 同音字:road 馬路 / rode ride 的過去式'),
    ('rode', 'road', '⚠️ 同音字:rode ride 的過去式 / road 馬路'),
    ('sail', 'sale', '⚠️ 同音字:sail 帆 / sale 拍賣'),
    ('sale', 'sail', '⚠️ 同音字:sale 拍賣 / sail 帆'),
    ('break', 'brake', '⚠️ 同音字:break 打破、休息 / brake 煞車'),
    ('brake', 'break', '⚠️ 同音字:brake 煞車 / break 打破、休息'),
    ('beat', 'beet', '⚠️ 同音字:beat 打敗 / beet 甜菜根'),
    ('bear', 'bare', '⚠️ 同音字:bear 熊、忍受 / bare 赤裸的'),
    ('bare', 'bear', '⚠️ 同音字:bare 赤裸的 / bear 熊、忍受'),
    ('cell', 'sell', '⚠️ 同音字:cell 細胞 / sell 賣'),
    ('sell', 'cell', '⚠️ 同音字:sell 賣 / cell 細胞'),
    ('whole', 'hole', '⚠️ 同音字:whole 整個 / hole 洞'),
    ('hole', 'whole', '⚠️ 同音字:hole 洞 / whole 整個'),
    ('plane', 'plain', '⚠️ 同音字:plane 飛機 / plain 樸素的、平原'),
    ('plain', 'plane', '⚠️ 同音字:plain 樸素的、平原 / plane 飛機'),
    ('pair', 'pear', '⚠️ 同音字:pair 一對 / pear 梨子'),
    ('pear', 'pair', '⚠️ 同音字:pear 梨子 / pair 一對'),
    ('write', 'right', '⚠️ 同音字:write 寫 / right 對的、右邊'),
    ('quite', 'quiet', '⚠️ 易混字:quite 相當(副詞)/ quiet 安靜的(形容詞)'),
    ('quiet', 'quite', '⚠️ 易混字:quiet 安靜的(形容詞)/ quite 相當(副詞)'),
    ('desert', 'dessert', '⚠️ 易混字:desert 沙漠 / dessert 甜點(雙 s)'),
    ('dessert', 'desert', '⚠️ 易混字:dessert 甜點(雙 s)/ desert 沙漠'),
    ('affect', 'effect', '⚠️ 易混字:affect 影響(動詞)/ effect 影響(名詞、結果)'),
    ('effect', 'affect', '⚠️ 易混字:effect 影響(名詞、結果)/ affect 影響(動詞)'),
    ('accept', 'except', '⚠️ 易混字:accept 接受 / except 除了…之外'),
    ('except', 'accept', '⚠️ 易混字:except 除了…之外 / accept 接受'),
    ('lose', 'loose', '⚠️ 易混字:lose 失去(動詞)/ loose 鬆的(形容詞)'),
    ('loose', 'lose', '⚠️ 易混字:loose 鬆的(形容詞)/ lose 失去(動詞)'),
    ('advice', 'advise', '⚠️ 易混字:advice 建議(名詞)/ advise 建議(動詞)'),
    ('advise', 'advice', '⚠️ 易混字:advise 建議(動詞)/ advice 建議(名詞)'),
    ('principal', 'principle', '⚠️ 易混字:principal 校長、主要的 / principle 原則'),
    ('principle', 'principal', '⚠️ 易混字:principle 原則 / principal 校長、主要的'),
    ('stationary', 'stationery', '⚠️ 易混字:stationary 靜止的 / stationery 文具'),
    ('stationery', 'stationary', '⚠️ 易混字:stationery 文具 / stationary 靜止的'),
    ('weather', 'whether', '⚠️ 易混字:weather 天氣 / whether 是否'),
    ('whether', 'weather', '⚠️ 易混字:whether 是否 / weather 天氣'),
]
homo_missing = []
for w_word, twin, note in KNOWN_HOMOPHONES:
    if w_word in idx and 'homophone-note' not in idx[w_word]:
        homo_missing.append((w_word, twin, note))

# ---------- 4) chunks 違規 ----------
ALLOWED_SINGLE_CHUNKS = {
    'a','I','an','as','at','be','by','do','go','he','if','in','is','it',
    'me','my','no','of','on','or','so','to','up','us','we','am','off','out',
    # 真不規則
    'one','two','eight','ice','eye','ear','arm','egg','our','hour','knee','knight',
    'know','knife','knew','knock','knot','wrong','wrap','wrote','write','answer',
}
chunks_violation = []
for w in words:
    if not isinstance(w.get('chunks'), list):
        continue
    if len(w['chunks']) >= 2:
        continue
    if w['word'] in ALLOWED_SINGLE_CHUNKS:
        continue
    chunks_violation.append(w['word'])

# ---------- 報告 ----------
print(f"=== 1) 拼字變化候選(沒 base 但看起來是衍生字) ===")
print(f"共 {len(candidates_family)} 字")
for w, stem, label in candidates_family[:50]:
    print(f"  {w}  ← {stem}  ({label})")
if len(candidates_family) > 50:
    print(f"  ... 還有 {len(candidates_family)-50} 字")

print(f"\n=== 2) 不規則動詞沒標 base ===")
print(f"共 {len(irregular_missing)} 字")
for w, base in irregular_missing:
    print(f"  {w}  ← {base}")

print(f"\n=== 3) 同音/易混字沒標 homophone-note ===")
print(f"共 {len(homo_missing)} 字")
for w, twin, _ in homo_missing:
    print(f"  {w}  vs  {twin}")

print(f"\n=== 4) chunks 違規(單塊但非白名單) ===")
print(f"共 {len(chunks_violation)} 字")
for w in chunks_violation[:30]:
    print(f"  {w}")
if len(chunks_violation) > 30:
    print(f"  ... 還有 {len(chunks_violation)-30} 字")
