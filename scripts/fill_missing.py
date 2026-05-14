"""
補漏:
1) 32 個不規則動詞遺漏 base
2) 48 個同音/易混字遺漏 homophone-note
3) 真家族線(精挑職業 -er / 情緒 -ing/-ed)
4) chunks 違規:the
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))

with open(VOCAB, 'r', encoding='utf-8') as f:
    data = json.load(f)

words = data['words']
idx = {w['word']: w for w in words}

# 1) 不規則動詞 (過去分詞 + 漏掉的過去式)
IRREGULAR_MORE = {
    # 過去分詞 (p.p.) — 配合 have / has / had 用
    'gone':    ('go',     '已經去了的版本(過去分詞,配 have 用)'),
    'done':    ('do',     '已經做完的版本(過去分詞,配 have 用)'),
    'seen':    ('see',    '已經看過的版本(過去分詞,配 have 用)'),
    'been':    ('be',     '已經當過的版本(過去分詞,配 have 用)'),
    'taken':   ('take',   '已經拿過的版本(過去分詞,配 have 用)'),
    'given':   ('give',   '已經給過的版本(過去分詞,配 have 用)'),
    'written': ('write',  '已經寫過的版本(過去分詞,配 have 用)'),
    'spoken':  ('speak',  '已經說過的版本(過去分詞,配 have 用)'),
    'broken':  ('break',  '已經打破的版本(過去分詞,配 have 用)'),
    'chosen':  ('choose', '已經選過的版本(過去分詞,配 have 用)'),
    'driven':  ('drive',  '已經開過車的版本(過去分詞,配 have 用)'),
    'ridden':  ('ride',   '已經騎過的版本(過去分詞,配 have 用)'),
    'risen':   ('rise',   '已經升起的版本(過去分詞,配 have 用)'),
    'flown':   ('fly',    '已經飛過的版本(過去分詞,配 have 用)'),
    'grown':   ('grow',   '已經長大的版本(過去分詞,配 have 用)'),
    'known':   ('know',   '已經知道的版本(過去分詞,配 have 用)'),
    'thrown':  ('throw',  '已經丟過的版本(過去分詞,配 have 用)'),
    'drawn':   ('draw',   '已經畫過的版本(過去分詞,配 have 用)'),
    'born':    ('bear',   '已經出生的版本(過去分詞;bear 也指生育)'),
    'drunk':   ('drink',  '已經喝過的版本(過去分詞,配 have 用)'),
    # 漏掉的過去式
    'swore':   ('swear',  '已經發誓過的版本(過去式)'),
    'clung':   ('cling',  '已經緊抓住的版本(過去式)'),
    'crept':   ('creep',  '已經悄悄爬過的版本(過去式)'),
    'bound':   ('bind',   '已經綁過的版本(過去式)'),
    'spread':  ('spread', '已經散開的版本(過去式同形)'),
    'split':   ('split',  '已經分開的版本(過去式同形)'),
    'cast':    ('cast',   '已經投擲過的版本(過去式同形)'),
    'thrust':  ('thrust', '已經猛推過的版本(過去式同形)'),
    'bid':     ('bid',    '出價(過去式同形)'),
    'forbid':  ('forbid', '禁止(過去式同形)'),
    # 第三人稱單數
    'does':    ('do',     '第三人稱單數(他/她/它做)'),
    'has':     ('have',   '第三人稱單數(他/她/它有)'),
}

# 2) 同音/易混字
HOMOPHONES_MORE = {
    'won':     '⚠️ 同音字:won win 的過去式 / one 一',
    'flour':   '⚠️ 同音字:flour 麵粉 / flower 花',
    'male':    '⚠️ 同音字:male 男性 / mail 郵件',
    'tale':    '⚠️ 同音字:tale 故事 / tail 尾巴',
    'meet':    '⚠️ 同音字:meet 見面 / meat 肉',
    'peace':   '⚠️ 同音字:peace 和平 / piece 一片',
    'week':    '⚠️ 同音字:week 一週 / weak 弱的',
    'weight':  '⚠️ 同音字:weight 重量 / wait 等',
    'blue':    '⚠️ 同音字:blue 藍色 / blew blow 的過去式',
    'blew':    '⚠️ 同音字:blew blow 的過去式 / blue 藍色',
    'new':     '⚠️ 同音字:new 新的 / knew know 的過去式(k 不發音)',
    'night':   '⚠️ 同音字:night 夜晚 / knight 騎士(k 不發音)',
    'knight':  '⚠️ 同音字:knight 騎士(k 不發音)/ night 夜晚',
    'hour':    '⚠️ 同音字:hour 小時(h 不發音)/ our 我們的',
    'our':     '⚠️ 同音字:our 我們的 / hour 小時(h 不發音)',
    'road':    '⚠️ 同音字:road 馬路 / rode ride 的過去式',
    'rode':    '⚠️ 同音字:rode ride 的過去式 / road 馬路',
    'sail':    '⚠️ 同音字:sail 帆 / sale 拍賣',
    'sale':    '⚠️ 同音字:sale 拍賣 / sail 帆',
    'break':   '⚠️ 同音字:break 打破、休息 / brake 煞車',
    'brake':   '⚠️ 同音字:brake 煞車 / break 打破、休息',
    'beat':    '⚠️ 同音字:beat 打敗 / beet 甜菜根',
    'bear':    '⚠️ 同音字:bear 熊、忍受 / bare 赤裸的',
    'bare':    '⚠️ 同音字:bare 赤裸的 / bear 熊、忍受',
    'cell':    '⚠️ 同音字:cell 細胞 / sell 賣',
    'sell':    '⚠️ 同音字:sell 賣 / cell 細胞',
    'whole':   '⚠️ 同音字:whole 整個 / hole 洞',
    'hole':    '⚠️ 同音字:hole 洞 / whole 整個',
    'plane':   '⚠️ 同音字:plane 飛機 / plain 樸素的、平原',
    'plain':   '⚠️ 同音字:plain 樸素的、平原 / plane 飛機',
    'pair':    '⚠️ 同音字:pair 一對 / pear 梨子',
    'pear':    '⚠️ 同音字:pear 梨子 / pair 一對',
    'quite':   '⚠️ 易混字:quite 相當(副詞)/ quiet 安靜的(形容詞)',
    'quiet':   '⚠️ 易混字:quiet 安靜的(形容詞)/ quite 相當(副詞)',
    'desert':  '⚠️ 易混字:desert 沙漠 / dessert 甜點(雙 s)',
    'dessert': '⚠️ 易混字:dessert 甜點(雙 s)/ desert 沙漠',
    'affect':  '⚠️ 易混字:affect 影響(動詞)/ effect 影響(名詞、結果)',
    'effect':  '⚠️ 易混字:effect 影響(名詞、結果)/ affect 影響(動詞)',
    'accept':  '⚠️ 易混字:accept 接受 / except 除了…之外',
    'except':  '⚠️ 易混字:except 除了…之外 / accept 接受',
    'advice':  '⚠️ 易混字:advice 建議(名詞)/ advise 建議(動詞)',
    'advise':  '⚠️ 易混字:advise 建議(動詞)/ advice 建議(名詞)',
    'principal':  '⚠️ 易混字:principal 校長、主要的 / principle 原則',
    'principle':  '⚠️ 易混字:principle 原則 / principal 校長、主要的',
    'stationary': '⚠️ 易混字:stationary 靜止的 / stationery 文具',
    'stationery': '⚠️ 易混字:stationery 文具 / stationary 靜止的',
    'weather':    '⚠️ 易混字:weather 天氣 / whether 是否',
    'whether':    '⚠️ 易混字:whether 是否 / weather 天氣',
}

# 3) 真家族線 — 衍生字精挑(意義直接相關才標)
# -er 職業 / 工具 / 物品
DERIVATIVE_FAMILY = {
    # 職業 / 做某事的人
    'teacher':  ('teach',   '做這件事的人(teach + er,教書的人)'),
    'farmer':   ('farm',    '做這件事的人(farm + er,務農的人)'),
    'driver':   ('drive',   '做這件事的人(drive + r,開車的人)'),
    'singer':   ('sing',    '做這件事的人(sing + er,唱歌的人)'),
    'baker':    ('bake',    '做這件事的人(bake + r,烤麵包的人)'),
    'worker':   ('work',    '做這件事的人(work + er,做工的人)'),
    'waiter':   ('wait',    '做這件事的人(wait + er,服務生)'),
    'painter':  ('paint',   '做這件事的人(paint + er,畫畫/油漆工)'),
    'designer': ('design',  '做這件事的人(design + er,設計師)'),
    'engineer': ('engine',  '懂引擎的人(engine + er,工程師)'),
    'reader':   ('read',    '做這件事的人(read + er,讀者)'),
    'writer':   ('write',   '做這件事的人(writ + er,作家)'),
    'speaker':  ('speak',   '做這件事的人(speak + er,演講者)'),
    'player':   ('play',    '做這件事的人(play + er,玩家/球員)'),
    'runner':   ('run',     '做這件事的人(run + ner,跑者)'),
    'swimmer':  ('swim',    '做這件事的人(swim + mer,游泳者)'),
    'dancer':   ('dance',   '做這件事的人(danc + er,舞者)'),
    'helper':   ('help',    '做這件事的人(help + er,幫忙的人)'),
    'leader':   ('lead',    '做這件事的人(lead + er,領導者)'),
    'manager':  ('manage',  '做這件事的人(manag + er,經理)'),
    'owner':    ('own',     '做這件事的人(own + er,擁有者)'),
    'cleaner':  ('clean',   '做這件事的人(clean + er,清潔工)'),
    'singer2': None,  # placeholder

    # -er 工具 / 物品
    'computer': ('compute', '做這件事的東西(compute + er,計算的機器)'),
    'charger':  ('charge',  '做這件事的東西(charg + er,充電器)'),
    'eraser':   ('erase',   '做這件事的東西(eras + er,擦除工具)'),
    'marker':   ('mark',    '做這件事的東西(mark + er,做記號的筆)'),
    'heater':   ('heat',    '做這件事的東西(heat + er,加熱器)'),
    'hanger':   ('hang',    '做這件事的東西(hang + er,掛東西的工具)'),
    'timer':    ('time',    '做這件事的東西(tim + er,計時器)'),
    'ruler':    ('rule',    '做這件事的東西(rul + er,量尺)'),
    'folder':   ('fold',    '做這件事的東西(fold + er,資料夾)'),
    'dryer':    ('dry',     '做這件事的東西(dry + er,烘乾機)'),
    'cleaner_obj': None,

    # -ing 情緒形容詞:讓「事物」覺得怎樣
    'boring':       ('bore',     '讓人覺得無聊的(描述事物,+ing 形容詞)'),
    'interesting':  ('interest', '讓人覺得有趣的(描述事物,+ing 形容詞)'),
    'amazing':      ('amaze',    '讓人覺得驚奇的(描述事物,+ing 形容詞)'),
    'freezing':     ('freeze',   '冷到讓人結凍的(描述事物,+ing 形容詞)'),
    'exciting':     ('excite',   '讓人覺得興奮的(描述事物,+ing 形容詞)'),
    'tiring':       ('tire',     '讓人覺得累的(描述事物,+ing 形容詞)'),
    'relaxing':     ('relax',    '讓人覺得放鬆的(描述事物,+ing 形容詞)'),
    'confusing':    ('confuse',  '讓人覺得困惑的(描述事物,+ing 形容詞)'),
    'surprising':   ('surprise', '讓人覺得驚訝的(描述事物,+ing 形容詞)'),
    'shocking':     ('shock',    '讓人覺得震驚的(描述事物,+ing 形容詞)'),
    'embarrassing': ('embarrass','讓人覺得尷尬的(描述事物,+ing 形容詞)'),
    'annoying':     ('annoy',    '讓人覺得煩的(描述事物,+ing 形容詞)'),
    'disappointing':('disappoint','讓人覺得失望的(描述事物,+ing 形容詞)'),
    'frightening':  ('frighten', '讓人覺得害怕的(描述事物,+ing 形容詞)'),

    # -ed 情緒形容詞:「人」覺得怎樣
    'bored':       ('bore',     '人覺得無聊的(描述人,+ed 形容詞)'),
    'interested':  ('interest', '人覺得有興趣的(描述人,+ed 形容詞)'),
    'amazed':      ('amaze',    '人覺得驚奇的(描述人,+ed 形容詞)'),
    'excited':     ('excite',   '人覺得興奮的(描述人,+ed 形容詞)'),
    'tired':       ('tire',     '人覺得累的(描述人,+ed 形容詞)'),
    'relaxed':     ('relax',    '人覺得放鬆的(描述人,+ed 形容詞)'),
    'confused':    ('confuse',  '人覺得困惑的(描述人,+ed 形容詞)'),
    'surprised':   ('surprise', '人覺得驚訝的(描述人,+ed 形容詞)'),
    'shocked':     ('shock',    '人覺得震驚的(描述人,+ed 形容詞)'),
    'embarrassed': ('embarrass','人覺得尷尬的(描述人,+ed 形容詞)'),
    'annoyed':     ('annoy',    '人覺得煩的(描述人,+ed 形容詞)'),
    'scared':      ('scare',    '人覺得害怕的(描述人,+ed 形容詞)'),
    'frightened':  ('frighten', '人覺得害怕的(描述人,+ed 形容詞)'),
    'worried':     ('worry',    '人覺得擔心的(描述人,+ed 形容詞,y 變 i)'),
    'disappointed':('disappoint','人覺得失望的(描述人,+ed 形容詞)'),

    # -er / -est 已在第一批處理(smaller / biggest 等),這裡補一些
    'older':    ('old',  '「更老/更舊」的版本(比較級,+er)'),
    'oldest':   ('old',  '「最老/最舊」的版本(最高級,+est)'),
    'younger':  ('young','「更年輕」的版本(比較級,+er)'),
    'youngest': ('young','「最年輕」的版本(最高級,+est)'),
    'longer':   ('long', '「更長」的版本(比較級,+er)'),
    'longest':  ('long', '「最長」的版本(最高級,+est)'),
    'shorter':  ('short','「更短」的版本(比較級,+er)'),
    'shortest': ('short','「最短」的版本(最高級,+est)'),
    'better':   ('good', '「更好」的版本(不規則比較級)'),
    'best':     ('good', '「最好」的版本(不規則最高級)'),
    'worse':    ('bad',  '「更壞」的版本(不規則比較級)'),
    'worst':    ('bad',  '「最壞」的版本(不規則最高級)'),
    'more':     ('many', '「更多」的版本(不規則比較級;也用於 much)'),
    'most':     ('many', '「最多」的版本(不規則最高級;也用於 much)'),

    # 名詞 -ing(動作 → 事物)
    'painting': ('paint',  '這個動作做出來的東西(paint + ing,畫作)'),
    'building': ('build',  '這個動作做出來的東西(build + ing,建築物)'),
    'meeting':  ('meet',   '這個動作的場合(meet + ing,會議)'),
    'feeling':  ('feel',   '這個動作的結果(feel + ing,感覺)'),
    'ending':   ('end',    '這個動作的結果(end + ing,結局)'),
    'beginning':('begin',  '這個動作的時刻(begin + ning,開始,雙 n)'),

    # 複數 -s 不規則(已在 vocab 的就標)
    'children': ('child',  '「很多個」的版本(複數,不規則:child → children)'),
    'feet':     ('foot',   '「很多個」的版本(複數,不規則:foot → feet)'),
    'teeth':    ('tooth',  '「很多個」的版本(複數,不規則:tooth → teeth)'),
    'men':      ('man',    '「很多個」的版本(複數,不規則:man → men)'),
    'women':    ('woman',  '「很多個」的版本(複數,不規則:woman → women)'),
    'people':   ('person', '「很多個」的版本(複數,不規則:person → people)'),
    'mice':     ('mouse',  '「很多個」的版本(複數,不規則:mouse → mice)'),
    'geese':    ('goose',  '「很多個」的版本(複數,不規則:goose → geese)'),
    'leaves':   ('leaf',   '「很多個」的版本(複數,f 變 ves:leaf → leaves)'),
    'lives':    ('life',   '「很多個」的版本(複數,fe 變 ves:life → lives)'),
    'knives':   ('knife',  '「很多個」的版本(複數,fe 變 ves:knife → knives)'),
    'wives':    ('wife',   '「很多個」的版本(複數,fe 變 ves:wife → wives)'),
    'wolves':   ('wolf',   '「很多個」的版本(複數,f 變 ves:wolf → wolves)'),
}
DERIVATIVE_FAMILY = {k: v for k, v in DERIVATIVE_FAMILY.items() if v is not None}

updated_irr = 0
updated_homo = 0
updated_deriv = 0
skipped = 0

for w_word, (base, note) in IRREGULAR_MORE.items():
    if w_word in idx and 'base' not in idx[w_word]:
        idx[w_word]['base'] = base
        idx[w_word]['family-note'] = note
        updated_irr += 1
    else:
        skipped += 1

for w_word, note in HOMOPHONES_MORE.items():
    if w_word in idx and 'homophone-note' not in idx[w_word]:
        idx[w_word]['homophone-note'] = note
        updated_homo += 1
    else:
        skipped += 1

for w_word, (base, note) in DERIVATIVE_FAMILY.items():
    if w_word in idx:
        if 'base' in idx[w_word]:
            skipped += 1
            continue
        idx[w_word]['base'] = base
        idx[w_word]['family-note'] = note
        updated_deriv += 1
    else:
        skipped += 1

# 4) chunks 違規 the
if 'the' in idx and idx['the'].get('chunks') == ['the']:
    idx['the']['chunks'] = ['th', 'e']
    if 'split' not in idx['the'] or idx['the'].get('split') == 'the':
        idx['the']['split'] = 'th + e'

# 寫回
with open(VOCAB, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"不規則動詞補:   {updated_irr}")
print(f"同音字補:       {updated_homo}")
print(f"衍生字家族補:   {updated_deriv}")
print(f"略過(已標/不存在):{skipped}")
print(f"總字數:         {len(words)}")
print(f"有 base:        {sum(1 for w in words if 'base' in w)}")
print(f"有 homophone:   {sum(1 for w in words if 'homophone-note' in w)}")
