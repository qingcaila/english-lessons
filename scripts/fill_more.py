"""第三輪:從審查殘留挑真家族線,擴充動詞白名單再跑一次"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB, 'r', encoding='utf-8') as f:
    data = json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

# 補一波:真家族線(從審查殘留挑)
EXTRA = {
    # -er 職業 / 工具(stem 是動詞)
    'photographer': ('photograph', '做這件事的人(photograph + er,攝影師)'),
    'sailor':       ('sail',       '做這件事的人(sail + or,水手)'),
    'banker':       ('bank',       '在這裡工作的人(bank + er,銀行家)'),
    'programmer':   ('program',    '做這件事的人(program + mer,程式設計師,雙 m)'),
    'gardener':     ('garden',     '做這件事的人(garden + er,園丁)'),
    'rapper':       ('rap',        '做這件事的人(rap + per,饒舌歌手,雙 p)'),
    'composer':     ('compose',    '做這件事的人(compos + er,作曲家)'),
    'conductor':    ('conduct',    '做這件事的人(conduct + or,指揮)'),
    'synthesizer':  ('synthesize', '做這件事的東西(synthesiz + er,合成器)'),
    'peeler':       ('peel',       '做這件事的東西(peel + er,削皮刀)'),
    'strainer':     ('strain',     '做這件事的東西(strain + er,濾網)'),
    'pitcher':      ('pitch',      '做這件事的人/東西(pitch + er,投手)'),
    'blender':      ('blend',      '做這件事的東西(blend + er,果汁機)'),
    'juicer':       ('juice',      '做這件事的東西(juic + er,榨汁機)'),
    'conditioner':  ('condition',  '做這件事的東西(condition + er,潤髮乳)'),
    'plunger':      ('plunge',     '做這件事的東西(plung + er,通馬桶器)'),
    'dispenser':    ('dispense',   '做這件事的東西(dispens + er,給皂器)'),
    'glider':       ('glide',      '做這件事的東西(glid + er,滑翔機)'),
    'stroller':     ('stroll',     '做這件事的東西(stroll + er,嬰兒推車)'),
    'diner':        ('dine',       '做這件事的地方(din + er,小餐廳)'),
    'rubber':       ('rub',        '做這件事的東西(rub + ber,橡皮擦,雙 b)'),
    'backpacker':   ('backpack',   '做這件事的人(backpack + er,背包客)'),
    'vendor':       ('vend',       '做這件事的人(vend + or,小販)'),
    'caterer':      ('cater',      '做這件事的人(cater + er,外燴業者)'),
    'router':       ('route',      '做這件事的東西(rout + er,路由器)'),
    'widower':      ('widow',      '男版的 widow(widow + er,鰥夫)'),
    'stranger':     ('strange',    '陌生的人(strange + r)'),
    'reporter':     ('report',     '做這件事的人(report + er,記者)'),
    'observer':     ('observe',    '做這件事的人(observ + er,觀察者)'),
    'producer':     ('produce',    '做這件事的人(produc + er,製作人)'),
    'consumer':     ('consume',    '做這件事的人(consum + er,消費者)'),
    'manager':      ('manage',     '做這件事的人(manag + er,經理)'),
    'visitor':      ('visit',      '做這件事的人(visit + or,訪客)'),
    'editor':       ('edit',       '做這件事的人(edit + or,編輯)'),
    'director':     ('direct',     '做這件事的人(direct + or,導演)'),
    'inventor':     ('invent',     '做這件事的人(invent + or,發明家)'),
    'investor':     ('invest',     '做這件事的人(invest + or,投資人)'),
    'protector':    ('protect',    '做這件事的人(protect + or,保護者)'),
    'projector':    ('project',    '做這件事的東西(project + or,投影機)'),
    'operator':     ('operate',    '做這件事的人(operat + or,操作員)'),
    'translator':   ('translate',  '做這件事的人(translat + or,翻譯)'),
    'creator':      ('create',     '做這件事的人(creat + or,創造者)'),
    'narrator':     ('narrate',    '做這件事的人(narrat + or,敘述者)'),
    'spectator':    ('spectate',   '做這件事的人(spectat + or,觀眾)'),
    'survivor':     ('survive',    '做這件事的人(surviv + or,倖存者)'),
    'governor':     ('govern',     '做這件事的人(govern + or,州長)'),
    'instructor':   ('instruct',   '做這件事的人(instruct + or,教練)'),
    'collector':    ('collect',    '做這件事的人(collect + or,收藏家)'),
    'inspector':    ('inspect',    '做這件事的人(inspect + or,檢查員)'),
    'investor':     ('invest',     '做這件事的人(invest + or,投資人)'),
    'sculptor':     ('sculpt',     '做這件事的人(sculpt + or,雕刻家)'),
    'predator':     ('prey',       '掠食動物(predat + or)'),
    'translator':   ('translate',  '做這件事的人(translat + or,翻譯)'),
    'distributor':  ('distribute', '做這件事的人(distribut + or,經銷商)'),
    'mediator':     ('mediate',    '做這件事的人(mediat + or,調解人)'),
    'navigator':    ('navigate',   '做這件事的人(navigat + or,導航員)'),
    'radiator':     ('radiate',    '做這件事的東西(radiat + or,暖氣)'),

    # 一些 -ing / -ed 補(stem 不在白名單)
    'fishing':      ('fish',       '正在釣魚的版本(進行式,+ing)'),
    'shopping':     ('shop',       '正在購物的版本(進行式,雙 p)'),
    'browsing':     ('browse',     '正在瀏覽的版本(進行式,去 e + ing)'),
    'browning':     ('brown',      '正在變褐色(進行式,+ing)'),

    # -ly 副詞補
    'mostly':       ('most',       '副詞版本(+ly,大多)'),
    'really':       ('real',       '副詞版本(+ly,真的)'),
    'finally':      ('final',      '副詞版本(+ly,終於)'),
    'usually':      ('usual',      '副詞版本(+ly,通常)'),
    'actually':     ('actual',     '副詞版本(+ly,實際上)'),
    'totally':      ('total',      '副詞版本(+ly,完全)'),
    'naturally':    ('natural',    '副詞版本(+ly,自然地)'),
    'normally':     ('normal',     '副詞版本(+ly,正常地)'),
    'especially':   ('especial',   '副詞版本(+ly,尤其)'),
    'definitely':   ('definite',   '副詞版本(+ly,絕對)'),
    'absolutely':   ('absolute',   '副詞版本(+ly,完全)'),
    'completely':   ('complete',   '副詞版本(+ly,完全)'),
    'directly':     ('direct',     '副詞版本(+ly,直接)'),
    'exactly':      ('exact',      '副詞版本(+ly,精確地)'),
    'mainly':       ('main',       '副詞版本(+ly,主要)'),
    'nearly':       ('near',       '副詞版本(+ly,幾乎)'),
    'recently':     ('recent',     '副詞版本(+ly,最近)'),
    'currently':    ('current',    '副詞版本(+ly,目前)'),
    'eventually':   ('eventual',   '副詞版本(+ly,最終)'),
    'frequently':   ('frequent',   '副詞版本(+ly,經常)'),
    'immediately':  ('immediate',  '副詞版本(+ly,立刻)'),
    'originally':   ('original',   '副詞版本(+ly,原本)'),
    'particularly': ('particular', '副詞版本(+ly,特別是)'),
    'probably':     ('probable',   '副詞版本(+ly,可能)'),
    'simply':       ('simple',     '副詞版本(+ly,單純)'),
    'suddenly':     ('sudden',     '副詞版本(+ly,突然)'),
    'finally':      ('final',      '副詞版本(+ly,終於)'),
    'lately':       ('late',       '副詞版本(+ly,最近)'),
    'mostly':       ('most',       '副詞版本(+ly,大多)'),
    'easily':       ('easy',       '副詞版本(y 變 i + ly,容易地)'),
    'happily':      ('happy',      '副詞版本(y 變 i + ly,開心地)'),
    'angrily':      ('angry',      '副詞版本(y 變 i + ly,生氣地)'),
    'busily':       ('busy',       '副詞版本(y 變 i + ly,忙碌地)'),
    'noisily':      ('noisy',      '副詞版本(y 變 i + ly,大聲地)'),
    'hungrily':     ('hungry',     '副詞版本(y 變 i + ly,飢餓地)'),

    # -y 形容詞補(更全)
    'rainy':        ('rain',       '形容詞版本(+y,下雨的)'),
    'sunny':        ('sun',        '形容詞版本(+y,晴朗的,雙 n)'),
    'cloudy':       ('cloud',      '形容詞版本(+y,多雲的)'),
    'windy':        ('wind',       '形容詞版本(+y,有風的)'),
    'snowy':        ('snow',       '形容詞版本(+y,下雪的)'),
    'foggy':        ('fog',        '形容詞版本(+y,起霧的,雙 g)'),
    'rocky':        ('rock',       '形容詞版本(+y,多石的)'),
    'sandy':        ('sand',       '形容詞版本(+y,沙質的)'),
    'dusty':        ('dust',       '形容詞版本(+y,有灰塵的)'),
    'muddy':        ('mud',        '形容詞版本(+y,泥濘的,雙 d)'),
    'smoky':        ('smoke',      '形容詞版本(+y,煙霧瀰漫的)'),
    'icy':          ('ice',        '形容詞版本(+y,結冰的)'),
    'salty':        ('salt',       '形容詞版本(+y,鹹的)'),
    'tasty':        ('taste',      '形容詞版本(+y,好吃的)'),
    'sticky':       ('stick',      '形容詞版本(+y,黏的)'),
    'spicy':        ('spice',      '形容詞版本(+y,辣的)'),
    'fluffy':       ('fluff',      '形容詞版本(+y,毛茸茸的,雙 f)'),
    'crispy':       ('crisp',      '形容詞版本(+y,脆的)'),
    'creamy':       ('cream',      '形容詞版本(+y,奶油般的)'),
    'cheesy':       ('cheese',     '形容詞版本(+y,起司多的)'),
    'noisy':        ('noise',      '形容詞版本(+y,吵的)'),
    'shiny':        ('shine',      '形容詞版本(+y,發亮的)'),
    'fishy':        ('fish',       '形容詞版本(+y,腥的)'),
    'meaty':        ('meat',       '形容詞版本(+y,肉多的)'),
    'leafy':        ('leaf',       '形容詞版本(+y,葉子多的)'),
    'thirsty':      ('thirst',     '形容詞版本(+y,口渴的)'),
    'wealthy':      ('wealth',     '形容詞版本(+y,富有的)'),
    'healthy':      ('health',     '形容詞版本(+y,健康的)'),

    # -al 形容詞補
    'musical':      ('music',      '形容詞版本(+al,音樂的)'),
    'cultural':     ('culture',    '形容詞版本(+al,文化的)'),
    'natural':      ('nature',     '形容詞版本(+al,自然的)'),
    'national':     ('nation',     '形容詞版本(+al,國家的)'),
    'central':      ('center',     '形容詞版本(+al,中心的)'),
    'medical':      ('medicine',   '形容詞版本(+al,醫療的)'),
    'historical':   ('history',    '形容詞版本(+al,歷史的)'),
    'logical':      ('logic',      '形容詞版本(+al,合邏輯的)'),
    'magical':      ('magic',      '形容詞版本(+al,魔法的)'),
    'tropical':     ('tropic',     '形容詞版本(+al,熱帶的)'),
    'environmental':('environment','形容詞版本(+al,環境的)'),
    'accidental':   ('accident',   '形容詞版本(+al,意外的)'),
    'emotional':    ('emotion',    '形容詞版本(+al,情緒的)'),
    'traditional':  ('tradition',  '形容詞版本(+al,傳統的)'),
    'professional': ('profession', '形容詞版本(+al,專業的)'),
    'industrial':   ('industry',   '形容詞版本(+al,工業的)'),
    'global':       ('globe',      '形容詞版本(+al,全球的)'),
    'political':    ('politics',   '形容詞版本(+al,政治的)'),
    'seasonal':     ('season',     '形容詞版本(+al,季節的)'),
    'personal':     ('person',     '形容詞版本(+al,個人的)'),
    'sexual':       ('sex',        '形容詞版本(+al,性別的)'),

    # 一些 -s 複數補(明顯名詞)
    # 跳過,太多假陽性

    # 比較級 -ier
    'happier':      ('happy',      '「更開心」的版本(比較級,y 變 i + er)'),
    'easier':       ('easy',       '「更容易」的版本(比較級,y 變 i + er)'),
    'busier':       ('busy',       '「更忙」的版本(比較級,y 變 i + er)'),
    'prettier':     ('pretty',     '「更漂亮」的版本(比較級,y 變 i + er)'),
    'angrier':      ('angry',      '「更生氣」的版本(比較級,y 變 i + er)'),
    'funnier':      ('funny',      '「更好笑」的版本(比較級,y 變 i + er)'),
    'crazier':      ('crazy',      '「更瘋狂」的版本(比較級,y 變 i + er)'),
    'dirtier':      ('dirty',      '「更髒」的版本(比較級,y 變 i + er)'),
    'sillier':      ('silly',      '「更傻」的版本(比較級,y 變 i + er)'),

    # 拼字變化:第三人稱單數的特殊形
    'cries':        ('cry',        '第三人稱單數(他哭,y 變 ies)'),
    'tries':        ('try',        '第三人稱單數(他試,y 變 ies)'),
    'flies':        ('fly',        '第三人稱單數 / 蒼蠅複數(y 變 ies)'),
    'fries':        ('fry',        '第三人稱單數 / 薯條(y 變 ies)'),

    # -or 補
    'tutor':        ('tutor',      None),  # 跳過(stem 是自己)
    'mayor':        None,  # may 不是 stem
    'tailor':       None,  # tail 不是 stem
}
EXTRA = {k: v for k, v in EXTRA.items() if v is not None and v[1] is not None}

applied = 0
skipped = 0
for word, (base, note) in EXTRA.items():
    if word not in idx:
        skipped += 1
        continue
    if 'base' in idx[word]:
        skipped += 1
        continue
    idx[word]['base'] = base
    idx[word]['family-note'] = note
    applied += 1

with open(VOCAB, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"applied: {applied}")
print(f"skipped: {skipped}")
print(f"total with base: {sum(1 for w in words if 'base' in w)}")
