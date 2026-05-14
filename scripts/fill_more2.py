"""第四輪:從剩 643 字精挑真家族線"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB, 'r', encoding='utf-8') as f:
    data = json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

EXTRA = {
    # -ing 運動 / 活動
    'boxing':       ('box',       '這個動作當運動(box + ing,拳擊)'),
    'wrestling':    ('wrestle',   '這個動作當運動(wrestl + ing,摔角)'),
    'fencing':      ('fence',     '這個動作當運動(fenc + ing,擊劍)'),
    'cycling':      ('cycle',     '這個動作當運動(cycl + ing,騎自行車)'),
    'surfing':      ('surf',      '這個動作當運動(surf + ing,衝浪)'),
    'diving':       ('dive',      '這個動作當運動(div + ing,潛水)'),
    'skiing':       ('ski',       '這個動作當運動(ski + ing,滑雪)'),
    'hiking':       ('hike',      '這個動作當運動(hik + ing,健行)'),
    'camping':      ('camp',      '這個動作當活動(camp + ing,露營)'),
    'rowing':       ('row',       '這個動作當運動(row + ing,划船)'),
    'sailing':      ('sail',      '這個動作當運動(sail + ing,航行)'),
    'bowling':      ('bowl',      '這個動作當運動(bowl + ing,保齡球)'),
    # -ing 興趣
    'gardening':    ('garden',    '這個動作當興趣(garden + ing,園藝)'),
    'knitting':     ('knit',      '正在編織(進行式,雙 t)'),
    'sewing':       ('sew',       '正在縫紉(進行式,+ing)'),
    'quilting':     ('quilt',     '正在做拼布(進行式,+ing)'),
    'scrapbooking': ('scrapbook', '正在做剪貼簿(進行式,+ing)'),
    'journaling':   ('journal',   '正在寫日誌(進行式,+ing)'),
    'crafting':     ('craft',     '正在手作(進行式,+ing)'),
    'brewing':      ('brew',      '正在釀造(進行式,+ing)'),
    'birding':      ('bird',      '正在賞鳥(進行式,+ing)'),
    'composting':   ('compost',   '正在堆肥(進行式,+ing)'),
    'hoarding':     ('hoard',     '正在囤積(進行式,+ing)'),
    'weaving':      ('weave',     '正在編織(進行式,去 e + ing)'),
    'doodling':     ('doodle',    '正在塗鴉(進行式,去 e + ing)'),
    # -ing 約會 / 關係
    'dating':       ('date',      '正在約會(進行式,去 e + ing)'),
    'flirting':     ('flirt',     '正在調情(進行式,+ing)'),
    'cheating':     ('cheat',     '正在偷情/作弊(進行式,+ing)'),
    'ghosting':     ('ghost',     '突然消失不聯絡(進行式,+ing)'),
    # -ing 介系詞 / 物品
    'wedding':      ('wed',       '結婚的場合(wed + ding,婚禮)'),
    'icing':        ('ice',       '蛋糕上的(ic + ing,糖霜)'),
    'frosting':     ('frost',     '蛋糕上的(frost + ing,糖霜)'),
    'boarding':     ('board',     '上機/上船(board + ing,登機)'),
    'shipping':     ('ship',      '寄送(ship + ping,運費,雙 p)'),
    'sparkling':    ('sparkle',   '正在閃亮(進行式,去 e + ing)'),
    'casting':      ('cast',      '正在選角(進行式,+ing)'),
    'rating':       ('rate',      '正在評分(進行式,去 e + ing)'),
    'screening':    ('screen',    '正在篩選(進行式,+ing)'),
    'shredding':    ('shred',     '正在切碎(進行式,雙 d)'),
    'swelling':     ('swell',     '腫脹(swell + ing,+ing 名詞)'),
    'regarding':    ('regard',    '介系詞「關於」(regard + ing)'),
    'concerning':   ('concern',   '介系詞「關於」(concern + ing)'),
    'excluding':    ('exclude',   '介系詞「不包括」(exclud + ing)'),
    'including':    ('include',   '介系詞「包括」(includ + ing)'),
    'stunning':     ('stun',      '令人驚艷的(stun + ning 形容詞,雙 n)'),
    'charming':     ('charm',     '迷人的(charm + ing 形容詞)'),
    'dashing':      ('dash',      '帥氣的(dash + ing 形容詞)'),
    'daring':       ('dare',      '大膽的(dar + ing 形容詞)'),

    # -ed 補(stem 是動詞但漏掉)
    'finished':     ('finish',    '已經完成的版本(過去式,+ed)'),
    'reached':      ('reach',     '已經抵達的版本(過去式,+ed)'),
    'passed':       ('pass',      '已經通過的版本(過去式,+ed)'),
    'missed':       ('miss',      '已經錯過的版本(過去式,+ed)'),
    'kissed':       ('kiss',      '已經親過的版本(過去式,+ed)'),
    'pressed':      ('press',     '已經按過的版本(過去式,+ed)'),
    'dressed':      ('dress',     '已經穿上的版本(過去式,+ed)'),
    'crossed':      ('cross',     '已經越過的版本(過去式,+ed)'),
    'crashed':      ('crash',     '已經撞到的版本(過去式,+ed)'),
    'pushed':       ('push',      '已經推過的版本(過去式,+ed)'),
    'rushed':       ('rush',      '已經趕過的版本(過去式,+ed)'),
    'washed':       ('wash',      '已經洗過的版本(過去式,+ed)'),
    'brushed':      ('brush',     '已經刷過的版本(過去式,+ed)'),
    'fished':       ('fish',      '已經釣過的版本(過去式,+ed)'),
    'wished':       ('wish',      '已經希望過的版本(過去式,+ed)'),
    'pulled':       ('pull',      '已經拉過的版本(過去式,+ed)'),
    'jumped':       ('jump',      '已經跳過的版本(過去式,+ed)'),
    'kicked':       ('kick',      '已經踢過的版本(過去式,+ed)'),
    'climbed':      ('climb',     '已經爬過的版本(過去式,+ed)'),
    'laughed':      ('laugh',     '已經笑過的版本(過去式,+ed)'),
    'cried':        ('cry',       '已經哭過的版本(過去式,y 變 i + ed)'),
    'changed':      ('change',    '已經變過的版本(過去式,去 e + ed)'),
    'created':      ('create',    '已經創造的版本(過去式,去 e + ed)'),
    'arrived':      ('arrive',    '已經抵達的版本(過去式,去 e + ed)'),

    # -er 殘留
    'reporter':     ('report',    '做這件事的人(report + er,記者)'),
    'observer':     ('observe',   '做這件事的人(observ + er,觀察者)'),
    'consumer':     ('consume',   '做這件事的人(consum + er,消費者)'),
    'employer':     ('employ',    '做這件事的人(employ + er,雇主)'),
    'employee':     ('employ',    '被這件事影響的人(employ + ee,員工)'),
    'trainer':      ('train',     '做這件事的人(train + er,教練)'),
    'traveler':     ('travel',    '做這件事的人(travel + er,旅人)'),
    'designer':     ('design',    '做這件事的人(design + er,設計師)'),
    'volunteer':    ('volunteer', None),  # stem 是自己
    'speaker':      ('speak',     '做這件事的人/工具(speak + er,演講者/喇叭)'),
    'lighter':      ('light',     '做這件事的東西(light + er,打火機)'),
    'opener':       ('open',      '做這件事的東西(open + er,開瓶器)'),

    # -ly 殘留
    'slowly':       ('slow',      '副詞版本(+ly,慢慢地)'),
    'quickly':      ('quick',     '副詞版本(+ly,快快地)'),
    'loudly':       ('loud',      '副詞版本(+ly,大聲地)'),
    'softly':       ('soft',      '副詞版本(+ly,輕輕地)'),
    'quietly':      ('quiet',     '副詞版本(+ly,安靜地)'),
    'kindly':       ('kind',      '副詞版本(+ly,親切地)'),
    'badly':        ('bad',       '副詞版本(+ly,糟糕地)'),
    'sadly':        ('sad',       '副詞版本(+ly,難過地)'),
    'gladly':       ('glad',      '副詞版本(+ly,樂意地)'),
    'safely':       ('safe',      '副詞版本(+ly,安全地)'),
    'rudely':       ('rude',      '副詞版本(+ly,粗魯地)'),
    'politely':     ('polite',    '副詞版本(+ly,有禮貌地)'),
    'honestly':     ('honest',    '副詞版本(+ly,老實說)'),
    'seriously':    ('serious',   '副詞版本(+ly,認真地)'),
    'clearly':      ('clear',     '副詞版本(+ly,清楚地)'),
    'carefully':    ('careful',   '副詞版本(+ly,小心地)'),
    'carelessly':   ('careless',  '副詞版本(+ly,粗心地)'),
    'beautifully':  ('beautiful', '副詞版本(+ly,漂亮地)'),
    'wonderfully':  ('wonderful', '副詞版本(+ly,精彩地)'),
    'painfully':    ('painful',   '副詞版本(+ly,痛苦地)'),
    'helpfully':    ('helpful',   '副詞版本(+ly,有幫助地)'),
    'usefully':     ('useful',    '副詞版本(+ly,有用地)'),
    'perfectly':    ('perfect',   '副詞版本(+ly,完美地)'),
    'gently':       ('gentle',    '副詞版本(+ly,溫柔地)'),
    'simply':       ('simple',    '副詞版本(+ly,單純地)'),
    'rarely':       ('rare',      '副詞版本(+ly,很少)'),
    'commonly':     ('common',    '副詞版本(+ly,常見地)'),
    'briefly':      ('brief',     '副詞版本(+ly,簡短地)'),
    'newly':        ('new',       '副詞版本(+ly,新近)'),
    'highly':       ('high',      '副詞版本(+ly,高度地)'),
    'lowly':        ('low',       '副詞版本(+ly,謙卑地)'),

    # -y 殘留
    'rocky':        ('rock',      '形容詞版本(+y,多石的)'),
    'curly':        ('curl',      '形容詞版本(+y,捲的)'),
    'wavy':         ('wave',      '形容詞版本(+y,波浪狀的)'),
    'lucky':        ('luck',      '形容詞版本(+y,幸運的)'),
    'speedy':       ('speed',     '形容詞版本(+y,迅速的)'),
    'greedy':       ('greed',     '形容詞版本(+y,貪心的)'),
    'needy':        ('need',      '形容詞版本(+y,需要幫助的)'),
    'risky':        ('risk',      '形容詞版本(+y,有風險的)'),
    'shiny':        ('shine',     '形容詞版本(+y,發亮的)'),
    'sleepy':       ('sleep',     '形容詞版本(+y,愛睏的)'),
    'smelly':       ('smell',     '形容詞版本(+y,臭的)'),
    'bony':         ('bone',      '形容詞版本(+y,瘦巴巴的)'),
    'hairy':        ('hair',      '形容詞版本(+y,毛茸茸的)'),
    'starry':       ('star',      '形容詞版本(+y,星光燦爛的,雙 r)'),
    'fiery':        ('fire',      '形容詞版本(+y,火熱的)'),
    'sugary':       ('sugar',     '形容詞版本(+y,甜的)'),
    'milky':        ('milk',      '形容詞版本(+y,奶白色的)'),
    'soupy':        ('soup',      '形容詞版本(+y,湯多的)'),
    'spotty':       ('spot',      '形容詞版本(+y,有斑點的,雙 t)'),
    'dotty':        ('dot',       '形容詞版本(+y,有點的,雙 t)'),
    'rosy':         ('rose',      '形容詞版本(+y,玫瑰色的)'),
    'stormy':       ('storm',     '形容詞版本(+y,暴風雨的)'),
    'breezy':       ('breeze',    '形容詞版本(+y,涼爽的)'),
    'misty':        ('mist',      '形容詞版本(+y,有霧的)'),
    'frosty':       ('frost',     '形容詞版本(+y,結霜的)'),
    'gloomy':       ('gloom',     '形容詞版本(+y,陰暗的)'),
    'icy':          ('ice',       '形容詞版本(+y,結冰的)'),
    'dirty':        ('dirt',      '形容詞版本(+y,髒的)'),
    'fishy':        ('fish',      '形容詞版本(+y,腥的/可疑的)'),
    'guilty':       ('guilt',     '形容詞版本(+y,內疚的)'),
    'wormy':        ('worm',      '形容詞版本(+y,蟲多的)'),
    'tasty':        ('taste',     '形容詞版本(+y,好吃的)'),
    'thirsty':      ('thirst',    '形容詞版本(+y,口渴的)'),
    'curly':        ('curl',      '形容詞版本(+y,捲的)'),
    'meaty':        ('meat',      '形容詞版本(+y,肉多的)'),
    'leafy':        ('leaf',      '形容詞版本(+y,葉子多的)'),
    'crunchy':      ('crunch',    '形容詞版本(+y,脆的)'),

    # -al 殘留
    'biological':   ('biology',   '形容詞版本(+ical,生物的)'),
    'biochemical':  ('biochemistry', None),
    'electrical':   ('electric',  '形容詞版本(+al,電的)'),
    'critical':     ('critic',    '形容詞版本(+al,批判的)'),
    'classical':    ('classic',   '形容詞版本(+al,古典的)'),
    'practical':    ('practice',  '形容詞版本(+al,實用的)'),
    'typical':      ('type',      '形容詞版本(+ical,典型的)'),
    'physical':     ('physics',   '形容詞版本(+al,身體的/物理的)'),
    'optical':      ('optic',     '形容詞版本(+al,視覺的)'),
    'mental':       ('mind',      '形容詞版本(+al,心理的)'),
    'verbal':       ('verb',      '形容詞版本(+al,口頭的)'),
    'final':        ('finish',    None),  # 跳過,並非衍生
    'fictional':    ('fiction',   '形容詞版本(+al,虛構的)'),

    # -or
    'tutor':        None,
    'donor':        ('donate',    '做這件事的人(don + or,捐贈者)'),
    'actor':        ('act',       '做這件事的人(act + or,演員)'),
    'actress':      ('act',       '做這件事的女性(act + ress,女演員)'),
    'doctor':       ('doctor',    None),  # stem 跟自己一樣
    'professor':    ('profess',   '做這件事的人(profess + or,教授)'),
    'sponsor':      ('sponsor',   None),
    'governor':     ('govern',    '做這件事的人(govern + or,州長)'),

    # 比較級 / 最高級
    'highest':      ('high',      '「最高」的版本(最高級,+est)'),
    'lowest':       ('low',       '「最低」的版本(最高級,+est)'),
    'newest':       ('new',       '「最新」的版本(最高級,+est)'),
    'coolest':      ('cool',      '「最酷」的版本(最高級,+est)'),

    # -ous / -able / -ible 殘留
    'incredible':   ('incredibly',None),
    'flexible':     ('flex',      '形容詞版本(+ible,可彎曲的)'),
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
