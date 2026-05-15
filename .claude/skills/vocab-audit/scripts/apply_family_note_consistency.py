"""套用 family-note-consistency 修正"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

# === A 類:假家族線 → 移除 base + family-note ===
REMOVE_BASE = [
    'molest','faction','coalition','paradise','capable','visible','mental',
    'notion','comment','tradition','passive','petition','savor','legible',
    'improvise','pension','caption','pious','rotation','banner','mansion',
    'notable','sober','torment','violation','tension','fury','career',
    'earnest','tender','alive','business','copier','frontier','forgive',
    'fed','endive','wise','prize','promise','bless','hive','seize',
    'cherry','witness',
    # self-base 多義字
    'left','won','wound',
    # base 拼錯但有真 base 的:轉到 FIX_BASE
]

# === B + D 類:重寫 base 或 family-note ===
FIX_FAMILY = {
    # base 拼錯但有真 base
    'productive':    ('produce','「會…的」(+ive 形容詞,從 produce 來)'),
    'operation':     ('operate','這個動作的「結果/事物」(+tion 名詞,從 operate 來)'),
    'donation':      ('donate', '這個動作的「結果/事物」(+ation 名詞,從 donate 來)'),
    'carrier':       ('carry',  '做這件事的人(carry 去 y 變 i + er,運送者)'),
    'animation':     ('animate','這個動作的「結果/事物」(+ion 名詞,從 animate 來)'),
    'action':        ('act',    '這個動作的「結果/事物」(+ion 名詞,從 act 來)'),

    # 詞性錯誤:-ing 名詞化(B 類)
    'shooting':      ('shoot',  '這個動作的「事件/結果」(+ing 名詞化,槍擊事件)'),
    'warning':       ('warn',   '這個動作的「結果」(+ing 名詞化,警告)'),
    'ruling':        ('rule',   '這個動作的「結果」(+ing 名詞化,裁決)'),
    'voting':        ('vote',   '這個動作的「行為」(+ing 動名詞,投票)'),
    'drawing':       ('draw',   '這個動作做出來的東西(+ing 名詞,畫作)'),
    'setting':       ('set',    '這個動作的「結果」(+ing 名詞,場景/設定)'),
    'screening':     ('screen', '這個動作的「結果」(+ing 名詞,放映/篩檢)'),
    'manufacturing': ('manufacture','這個動作的「行業」(+ing 名詞,製造業)'),
    'opening':       ('open',   '這個動作的「事件」(+ing 名詞,開幕)'),
    'closing':       ('close',  '這個動作的「事件」(+ing 名詞,閉幕)'),
    'gathering':     ('gather', '這個動作的「結果」(+ing 名詞,聚會)'),
    'training':      ('train',  '這個動作的「課程」(+ing 名詞,訓練)'),
    'reading':       ('read',   '這個動作當名詞/活動(+ing 動名詞,閱讀)'),
    'writing':       ('write',  '這個動作當名詞/活動(+ing 動名詞,寫作)'),
    'baking':        ('bake',   '這個動作當活動(+ing 動名詞,烘焙)'),
    'booking':       ('book',   '這個動作的「事件」(+ing 名詞,訂位)'),
    'fitting':       ('fit',    '這個動作的「事件」(+ing 名詞,試穿,雙 t)'),
    'healing':       ('heal',   '這個動作的「結果」(+ing 名詞,癒合)'),
    'serving':       ('serve',  '名詞版本(+ing 變名詞,一份/一客)'),
    'offering':      ('offer',  '名詞版本(+ing 變名詞,offer 出去的東西,供品)'),
    'sparkling':     ('sparkle','形容詞版本(+ing 變形容詞,有氣泡的/閃閃發亮的)'),
    'including':     ('include','介系詞「包括」(include + ing)'),
    'considering':   ('consider','連接詞「考慮到」(consider + ing)'),
    'supposing':     ('suppose','連接詞「假設」(suppose + ing)'),
    'provided':      ('provide','連接詞「假如、只要」(provide + ed)'),
    'rating':        ('rate',   '這個動作的「結果」(+ing 名詞,評分)'),

    # 詞性錯誤:-al/-ive 名詞化
    'signal':        ('sign',   '從 sign 衍生的名詞(信號)'),
    'narrative':     ('narrate','從 narrate 衍生的名詞(敘事/故事;也可當形容詞)'),
    'detective':     ('detect', '做這件事的人(detect + ive 當名詞,偵探)'),
    'relative':      ('relate', '有關係的人(relate + ive,親戚)'),
    'executive':     ('execute','執行業務的人(execute + ive,主管)'),
    'archive':       ('arch',   '動詞版本(arch + ive 當動詞用,封存)'),
    'proposal':      ('propose','這個動作的「結果」(+al 名詞,提案/求婚)'),
    'withdrawal':    ('withdraw','這個動作的「結果」(+al 名詞,戒斷/撤回)'),
    'recital':       ('recite', '這個動作的「事件」(+al 名詞,獨奏會)'),
    'betrayal':      ('betray', '這個動作的「結果」(+al 名詞,背叛)'),
    'arrival':       ('arrive', '這個動作的「事件」(+al 名詞,抵達)'),
    'departure':     ('depart', '這個動作的「事件」(+ure 名詞,出發)'),
    'refusal':       ('refuse', '名詞版本(+al,把動詞變名詞,拒絕)'),
    'denial':        ('deny',   '名詞版本(+al 名詞,y 變 i,否認)'),
    'rehearsal':     ('rehearse','名詞版本(+al,把動詞變名詞,排練)'),
    'removal':       ('remove', '名詞版本(+al,把動詞變名詞,移去)'),
    'rental':        ('rent',   '名詞版本(+al,從動詞 rent 變名詞「租金」)'),
    'disposal':      ('dispose','名詞版本(+al,把動詞變名詞,處理)'),
    'musical':       ('music',  '形容詞/名詞(+al,音樂的;當名詞=音樂劇)'),

    # -y 名詞化(店/地方/結果)
    'bakery':        ('bake',   '做這件事的地方(bake + ry 名詞,麵包店)'),
    'grocery':       ('grocer', '賣的東西/店(grocer + y 名詞,雜貨)'),
    'delivery':      ('deliver','這個動作的結果(deliver + y 名詞,配送)'),
    'recovery':      ('recover','這個動作的結果(recover + y 名詞,康復)'),

    # +er 物 vs 人
    'developer':     ('develop','做這件事的人(develop + er,開發程式的人)'),
    'producer':      ('produce','做這件事的人(produc + er,製作節目的人)'),
    'winner':        ('win',    '做這件事的人(win + ner 雙 n,贏的人)'),
    'loser':         ('lose',   '做這件事的人(los + er,輸的人)'),
    'lover':         ('love',   '做這件事的人(lov + er,愛某人的人)'),
    'opener':        ('open',   '做這件事的東西(open + er,打開東西的工具)'),
    'toaster':       ('toast',  '做這件事的東西(toast + er,烤麵包的機器)'),
    'mixer':         ('mix',    '做這件事的東西(mix + er,攪拌的機器)'),
    'freezer':       ('freeze', '做這件事的東西(freez + er,冷凍的設備)'),
    'shaver':        ('shave',  '做這件事的工具(shav + er,刮鬍刀)'),
    'starter':       ('start',  '開頭吃的東西(start + er 名詞,前菜)'),
    'drawer':        ('draw',   '做這件事的東西(draw=拉,+er = 可以拉出來的東西,抽屜)'),

    # 比較級 vs +er 人 混淆
    'closer':        ('close',  '「更…」的版本(比較級,+er 形容詞)'),
    'former':        ('form',   '「以前的/前者」(獨立用法,跟 form 字面動作無關)'),

    # 過去分詞當形容詞
    'moved':         ('move',   '被打動的(過去分詞當形容詞,感動的)'),
    'broken':        ('break',  '壞掉的(過去分詞當形容詞;配 have 時也是完成式)'),
    'drunk':         ('drink',  '喝醉的(過去分詞當形容詞)'),
    'used':          ('use',    '用過的(過去分詞當形容詞,二手的、舊的)'),
    'learned':       ('learn',  '學過很多的(過去分詞當形容詞,博學的)'),
    'promising':     ('promise','「讓人覺得有 promise 的」(+ing 變形容詞,有前景的)'),

    # +less 副詞
    'regardless':    ('regard', '「不管…」的副詞(regard + less,無論)'),

    # 多義字補白話
    'shot':          ('shoot',  'shoot 一下的成果(名詞:一針/一槍/一杯)'),
    'cost':          ('cost',   '名詞「成本」/動詞三態同形「花費」'),
    'split':         ('split',  '原形和過去式長一樣(三態同形 split/split/split)'),
    'thrust':        ('thrust', '原形和過去式長一樣(三態同形)'),
    'forbid':        ('forbid', '原形動詞(過去式 forbade,過去分詞 forbidden,不是同形)'),

    # self-base 三態同形修正
    'let':           ('let',    '三態同形 let/let/let(現在、過去、過去分詞都長一樣)'),
    'shut':          ('shut',   '三態同形 shut/shut/shut'),
    'bet':           ('bet',    '三態同形 bet/bet/bet'),
    'burst':         ('burst',  '三態同形 burst/burst/burst'),
    'quit':          ('quit',   '三態同形 quit/quit/quit'),
    'spread':        ('spread', '三態同形 spread/spread/spread'),
    'put':           ('put',    '三態同形 put/put/put'),
    'cut':           ('cut',    '三態同形 cut/cut/cut'),
    'hit':           ('hit',    '三態同形 hit/hit/hit'),
    'set':           ('set',    '三態同形 set/set/set(動詞);名詞=一組'),
    'hurt':          ('hurt',   '三態同形 hurt/hurt/hurt;也可當形容詞「受傷的」'),
    'cast':          ('cast',   '三態同形 cast/cast/cast;名詞=演員陣容'),
    'bid':           ('bid',    '三態同形 bid/bid/bid;名詞=出價/投標'),
    'read':          ('read',   '三態同形 read/read/read(過去式唸 ㄖㄝㄉ)'),
    'run':           ('run',    '三態 run/ran/run(過去分詞同形)'),
    'beat':          ('beat',   '名詞=拍子/節拍;動詞三態 beat/beat/beaten'),
    'forecast':      ('forecast','名詞=預報;動詞三態同形 forecast/forecast/forecast'),
    'become':        ('become', '三態 become/became/become(過去分詞同形)'),
    'upset':         ('upset',  '形容詞「心煩的」(過去分詞當形容詞);動詞三態同形'),

    # 抽象副詞改白話
    'snowy':         ('snow',   '形容詞版本(+y,下雪的、多雪的)'),
    'foggy':         ('fog',    '形容詞版本(+y,起霧的、多霧的)'),
    'healthy':       ('health', '形容詞版本(+y,健康的)'),
    'juicy':         ('juice',  '形容詞版本(+y,多汁的)'),
    'easy':          ('ease',   '形容詞版本(+y,簡單的;ease=輕鬆狀態)'),
    'funny':         ('fun',    '形容詞版本(+y 雙 n,好笑的;從 fun 樂趣來)'),

    # 副詞/形容詞混合 -ly 補白話
    'daily':         ('day',    '形容詞/副詞版本(+ly,每日的/每天)'),
    'weekly':        ('week',   '形容詞/副詞版本(+ly,每週的/每週)'),
    'monthly':       ('month',  '形容詞/副詞版本(+ly,每月的/每月)'),
    'yearly':        ('year',   '形容詞/副詞版本(+ly,每年的/每年)'),
    'hourly':        ('hour',   '形容詞/副詞版本(+ly,每小時的/每小時)'),
    'lonely':        ('lone',   '形容詞版本(+ly 把 lone 變形容詞,孤單的;這個 -ly 不是副詞)'),
    'friendly':      ('friend', '形容詞版本(+ly 把 friend 變形容詞,友善的;這個 -ly 不是副詞)'),
    'shortly':       ('short',  '副詞版本(+ly,短時間後 → 不久、立刻)'),

    # was/were 補主詞列表
    'was':           ('is',     '「是」的過去版本(I/he/she/it 配 was)'),
    'were':          ('are',    '「是」的過去版本(you/we/they 配 were)'),

    # critical 改用 mean 對齊
    'critical':      ('critic', '形容詞版本(+al,危急的/關鍵的)'),

    # cashier 完全錯改
    'cashier':       ('cash',   '做這件事的人(cash + ier,處理現金的人,收銀員)'),

    # 同義詞橋接
    'banner':        ('ban',    '橫幅 (banner 跟 ban 字源不同,僅同形)'),
}

# === 處理刪除 + 改寫 ===
n_remove = 0
n_fix = 0
not_found = []

for word in REMOVE_BASE:
    if word in idx:
        if 'base' in idx[word]:
            del idx[word]['base']
            n_remove += 1
        if 'family-note' in idx[word]:
            del idx[word]['family-note']
    else:
        not_found.append(word)

for word, (base, note) in FIX_FAMILY.items():
    if word in idx:
        idx[word]['base'] = base
        idx[word]['family-note'] = note
        n_fix += 1
    else:
        not_found.append(word)

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"移除假家族線: {n_remove}")
print(f"修正 family-note: {n_fix}")
print(f"總 base: {sum(1 for w in words if 'base' in w)}")
if not_found: print(f"找不到 ({len(not_found)}): {not_found[:20]}")
