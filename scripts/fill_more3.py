"""第五輪:殘留高價值真家族線"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB, 'r', encoding='utf-8') as f:
    data = json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

EXTRA = {
    # -er 真家族線
    'podcaster':    ('podcast',    '做這件事的人(podcast + er,Podcast 主)'),
    'officer':      ('office',     '在這裡工作的人(offic + er,官員)'),
    'knitter':      ('knit',       '做這件事的人(knit + ter,編織者,雙 t)'),
    'gamer':        ('game',       '做這件事的人(gam + er,玩家)'),
    'streamer':     ('stream',     '做這件事的人(stream + er,實況主)'),
    'poker':        ('poke',       '做這件事的東西(pok + er,撥火棒)'),
    'trailer':      ('trail',      '做這件事的東西(trail + er,預告片/拖車)'),
    'thriller':     ('thrill',     '會這樣的東西(thrill + er,驚悚片)'),
    'viewer':       ('view',       '做這件事的人(view + er,觀眾)'),
    'spoiler':      ('spoil',      '會這樣的東西(spoil + er,劇透)'),
    'booster':      ('boost',      '做這件事的東西(boost + er,加強物)'),
    'spotter':      ('spot',       '做這件事的人(spot + ter,協助觀察者)'),
    'tracker':      ('track',      '做這件事的東西(track + er,追蹤器)'),
    'shredder':     ('shred',      '做這件事的東西(shred + der,碎紙機)'),
    'stapler':      ('staple',     '做這件事的東西(stapl + er,釘書機)'),
    'highlighter':  ('highlight',  '做這件事的東西(highlight + er,螢光筆)'),
    'reminder':     ('remind',     '做這件事的東西(remind + er,提醒)'),
    'merger':       ('merge',      '這個動作的結果(merg + er,合併)'),
    'subscriber':   ('subscribe',  '做這件事的人(subscrib + er,訂閱者)'),
    'hacker':       ('hack',       '做這件事的人(hack + er,駭客)'),
    'influencer':   ('influence',  '做這件事的人(influenc + er,網紅)'),
    'extinguisher': ('extinguish', '做這件事的東西(extinguish + er,滅火器)'),
    'scammer':      ('scam',       '做這件事的人(scam + mer,詐騙犯,雙 m)'),
    'stalker':      ('stalk',      '做這件事的人(stalk + er,跟蹤狂)'),
    'intruder':     ('intrude',    '做這件事的人(intrud + er,入侵者)'),
    'smuggler':     ('smuggle',    '做這件事的人(smuggl + er,走私者)'),
    'dealer':       ('deal',       '做這件事的人(deal + er,經銷商/毒販)'),
    'kidnapper':    ('kidnap',     '做這件事的人(kidnap + per,綁匪,雙 p)'),
    'prayer':       ('pray',       '這個動作(pray + er,祈禱)'),
    'grinder':      ('grind',      '做這件事的東西(grind + er,研磨機)'),
    'foreigner':    ('foreign',    '從外國來的人(foreign + er)'),
    'prisoner':     ('prison',     '在裡面的人(prison + er,囚犯)'),
    'adviser':      ('advise',     '做這件事的人(advis + er,顧問)'),
    'miner':        ('mine',       '做這件事的人(min + er,礦工)'),
    'robber':       ('rob',        '做這件事的人(rob + ber,搶匪,雙 b)'),
    'commander':    ('command',    '做這件事的人(command + er,司令官)'),
    'locker':       ('lock',       '做這件事的東西(lock + er,置物櫃)'),
    'murderer':     ('murder',     '做這件事的人(murder + er,兇手)'),
    'porter':       ('port',       '做這件事的人(port + er,搬運工)'),
    'researcher':   ('research',   '做這件事的人(research + er,研究員)'),
    'shaver':       ('shave',      '做這件事的東西(shav + er,刮鬍刀)'),
    'advertiser':   ('advertise',  '做這件事的人(advertis + er,廣告主)'),
    'banner':       ('ban',        '橫幅(ban + ner,雙 n)'),
    'batter':       ('bat',        '做這件事的人(bat + ter,打者,雙 t)'),
    'boxer':        ('box',        '做這件事的人(box + er,拳擊手)'),
    'chatter':      ('chat',       '正在閒聊(chat + ter,雙 t)'),
    'commuter':     ('commute',    '做這件事的人(commut + er,通勤族)'),
    'baby-sitter':  ('baby-sit',   '做這件事的人(baby-sit + ter,臨時保姆,雙 t)'),
    'user':         ('use',        '做這件事的人(us + er,使用者)'),
    'lower':        ('low',        '「更低」的版本(比較級,+er)'),
    'tower':        ('tower',      None),  # 跳過,塔本身
    'commuter':     ('commute',    '做這件事的人(commut + er,通勤族)'),
    'wander':       ('wander',     None),  # stem 是自己

    # -or 殘留(真的)
    'actor':        ('act',        '做這件事的人(act + or,演員)'),
    'professor':    ('profess',    '做這件事的人(profess + or,教授)'),
    'governor':     ('govern',     '做這件事的人(govern + or,州長)'),
    'editor':       ('edit',       '做這件事的人(edit + or,編輯)'),
    'director':     ('direct',     '做這件事的人(direct + or,導演)'),
    'inventor':     ('invent',     '做這件事的人(invent + or,發明家)'),
    'investor':     ('invest',     '做這件事的人(invest + or,投資人)'),
    'visitor':      ('visit',      '做這件事的人(visit + or,訪客)'),
    'spectator':    ('spectate',   '做這件事的人(spectat + or,觀眾)'),
    'survivor':     ('survive',    '做這件事的人(surviv + or,倖存者)'),
    'instructor':   ('instruct',   '做這件事的人(instruct + or,教練)'),
    'collector':    ('collect',    '做這件事的人(collect + or,收藏家)'),
    'inspector':    ('inspect',    '做這件事的人(inspect + or,檢查員)'),
    'operator':     ('operate',    '做這件事的人(operat + or,操作員)'),
    'narrator':     ('narrate',    '做這件事的人(narrat + or,敘述者)'),
    'translator':   ('translate',  '做這件事的人(translat + or,翻譯)'),
    'creator':      ('create',     '做這件事的人(creat + or,創造者)'),
    'projector':    ('project',    '做這件事的東西(project + or,投影機)'),
    'protector':    ('protect',    '做這件事的東西/人(protect + or,保護者)'),

    # 比較級/最高級殘留
    'higher':       ('high',       '「更高」的版本(比較級,+er)'),
    'older':        ('old',        '「更老」的版本(比較級,+er)'),
    'younger':      ('young',      '「更年輕」的版本(比較級,+er)'),
    'lighter':      ('light',      '「更輕/做這件事的東西」(比較級 或 打火機)'),
    'darker':       ('dark',       '「更暗」的版本(比較級,+er)'),

    # -ly 副詞補
    'truly':        ('true',       '副詞版本(+ly,真的)'),
    'fully':        ('full',       '副詞版本(+ly,完全)'),
    'hardly':       ('hard',       '副詞版本(+ly,幾乎不)'),
    'merely':       ('mere',       '副詞版本(+ly,僅僅)'),
    'fairly':       ('fair',       '副詞版本(+ly,公平地)'),
    'firmly':       ('firm',       '副詞版本(+ly,堅定地)'),
    'tightly':      ('tight',      '副詞版本(+ly,緊緊地)'),
    'widely':       ('wide',       '副詞版本(+ly,廣泛地)'),
    'closely':      ('close',      '副詞版本(+ly,密切地)'),
    'freely':       ('free',       '副詞版本(+ly,自由地)'),
    'deeply':       ('deep',       '副詞版本(+ly,深深地)'),
    'roughly':      ('rough',      '副詞版本(+ly,粗略地)'),
    'smoothly':     ('smooth',     '副詞版本(+ly,順暢地)'),
    'warmly':       ('warm',       '副詞版本(+ly,溫暖地)'),
    'coldly':       ('cold',       '副詞版本(+ly,冷冷地)'),
    'strongly':     ('strong',     '副詞版本(+ly,強烈地)'),
    'weakly':       ('weak',       '副詞版本(+ly,微弱地)'),
    'richly':       ('rich',       '副詞版本(+ly,豐富地)'),
    'poorly':       ('poor',       '副詞版本(+ly,差勁地)'),
    'shortly':      ('short',      '副詞版本(+ly,不久)'),
    'commonly':     ('common',     '副詞版本(+ly,常見地)'),
    'gradually':    ('gradual',    '副詞版本(+ly,逐漸地)'),
    'occasionally': ('occasional', '副詞版本(+ly,偶爾)'),
    'extremely':    ('extreme',    '副詞版本(+ly,極度地)'),
    'specifically': ('specific',   '副詞版本(+ally,具體地)'),
    'approximately':('approximate','副詞版本(+ly,大約地)'),
    'fortunately':  ('fortunate',  '副詞版本(+ly,幸運的是)'),
    'unfortunately':('unfortunate','副詞版本(+ly,不幸的是)'),
    'thoughtfully': ('thoughtful', '副詞版本(+ly,深思熟慮地)'),
    'thankfully':   ('thankful',   '副詞版本(+ly,謝天謝地)'),
    'painfully':    ('painful',    '副詞版本(+ly,痛苦地)'),
    'powerfully':   ('powerful',   '副詞版本(+ly,有力地)'),
    'cheerfully':   ('cheerful',   '副詞版本(+ly,愉快地)'),
    'hopefully':    ('hopeful',    '副詞版本(+ly,希望地)'),
    'mindfully':    ('mindful',    '副詞版本(+ly,專注地)'),
    'doubtfully':   ('doubtful',   '副詞版本(+ly,懷疑地)'),
    'awfully':      ('awful',      '副詞版本(+ly,非常)'),
    'lovely':       ('love',       '形容詞(+ly,可愛的;這個少數 -ly 是形容詞)'),
    'silently':     ('silent',     '副詞版本(+ly,沉默地)'),
    'patiently':    ('patient',    '副詞版本(+ly,有耐心地)'),
    'impatiently':  ('impatient',  '副詞版本(+ly,不耐煩地)'),
    'briefly':      ('brief',      '副詞版本(+ly,簡短地)'),

    # -y 殘留
    'curly':        ('curl',       '形容詞版本(+y,捲的)'),
    'bumpy':        ('bump',       '形容詞版本(+y,顛簸的)'),
    'lumpy':        ('lump',       '形容詞版本(+y,結塊的)'),
    'grumpy':       ('grump',      '形容詞版本(+y,壞脾氣的)'),
    'jumpy':        ('jump',       '形容詞版本(+y,神經質的)'),
    'rusty':        ('rust',       '形容詞版本(+y,生鏽的)'),
    'crispy':       ('crisp',      '形容詞版本(+y,脆的)'),
    'crusty':       ('crust',      '形容詞版本(+y,有硬皮的)'),
    'fluffy':       ('fluff',      '形容詞版本(+y,毛茸茸的,雙 f)'),
    'sleazy':       ('sleaze',     '形容詞版本(+y,低俗的)'),
    'pricey':       ('price',      '形容詞版本(+y,昂貴的)'),
    'cheesy':       ('cheese',     '形容詞版本(+y,起司多的)'),
    'creamy':       ('cream',      '形容詞版本(+y,奶油般的)'),
    'fruity':       ('fruit',      '形容詞版本(+y,果香的)'),
    'minty':        ('mint',       '形容詞版本(+y,薄荷味的)'),
    'crunchy':      ('crunch',     '形容詞版本(+y,脆的)'),
    'chewy':        ('chew',       '形容詞版本(+y,有嚼勁的)'),
    'stinky':       ('stink',      '形容詞版本(+y,臭的)'),
    'itchy':        ('itch',       '形容詞版本(+y,癢的)'),
    'thorny':       ('thorn',      '形容詞版本(+y,多刺的)'),
    'woody':        ('wood',       '形容詞版本(+y,木質的)'),
    'grassy':       ('grass',      '形容詞版本(+y,草地多的)'),
    'soupy':        ('soup',       '形容詞版本(+y,湯多的)'),
    'sleety':       ('sleet',      '形容詞版本(+y,雨夾雪的)'),
    'pearly':       ('pearl',      '形容詞版本(+y,珍珠般的)'),
    'creepy':       ('creep',      '形容詞版本(+y,毛骨悚然的)'),
    'sneaky':       ('sneak',      '形容詞版本(+y,鬼鬼祟祟的)'),

    # -al 殘留
    'mental':       ('mind',       None),  # mind/mental 並非衍生
    'physical':     ('physic',     None),
    'electrical':   ('electric',   '形容詞版本(+al,電的)'),
    'historical':   ('history',    '形容詞版本(+ical,歷史的)'),
    'biological':   ('biology',    '形容詞版本(+ical,生物的)'),
    'mathematical': ('mathematics','形容詞版本(+al,數學的)'),
    'chemical':     ('chemistry',  None),
    'fictional':    ('fiction',    '形容詞版本(+al,虛構的)'),
    'emotional':    ('emotion',    '形容詞版本(+al,情緒的)'),
    'cultural':     ('culture',    '形容詞版本(+al,文化的)'),
    'traditional':  ('tradition',  '形容詞版本(+al,傳統的)'),
    'environmental':('environment','形容詞版本(+al,環境的)'),
    'industrial':   ('industry',   '形容詞版本(+al,工業的)'),
    'optional':     ('option',     '形容詞版本(+al,可選的)'),
    'occasional':   ('occasion',   '形容詞版本(+al,偶爾的)'),
    'professional': ('profession', '形容詞版本(+al,專業的)'),
    'sensational':  ('sensation',  '形容詞版本(+al,轟動的)'),

    # -ous 殘留
    'tremendous':   ('tremor',     None),  # 不算正規衍生

    # 過去式 / -ed 殘留
    'arrived':      ('arrive',     '已經抵達的版本(過去式,去 e + ed)'),
    'wanted':       ('want',       '已經想要的版本(過去式,+ed)'),
    'needed':       ('need',       '已經需要的版本(過去式,+ed)'),
    'showed':       ('show',       '已經展示過的版本(過去式,+ed)'),
    'allowed':      ('allow',      '已經允許的版本(過去式,+ed)'),
    'pulled':       ('pull',       '已經拉過的版本(過去式,+ed)'),
    'kicked':       ('kick',       '已經踢過的版本(過去式,+ed)'),
    'mixed':        ('mix',        '已經混合的版本(過去式,+ed)'),
    'fixed':        ('fix',        '已經修好的版本(過去式,+ed)'),
    'boxed':        ('box',        '已經裝箱的版本(過去式,+ed)'),
    'taxed':        ('tax',        '已經課稅的版本(過去式,+ed)'),
    'agreed':       ('agree',      '已經同意的版本(過去式,+d)'),
    'tied':         ('tie',        '已經綁過的版本(過去式,去 e + d)'),
    'died':         ('die',        '已經死的版本(過去式,去 e + d)'),
    'lied':         ('lie',        '已經說謊的版本(過去式,去 e + d)'),
    'cried':        ('cry',        '已經哭過的版本(過去式,y 變 i + ed)'),
    'dried':        ('dry',        '已經乾的版本(過去式,y 變 i + ed)'),
    'flied':        ('fly',        '飛過(罕用,通常用 flew/flown)'),
    'spied':        ('spy',        '已經監視的版本(過去式,y 變 i + ed)'),
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
