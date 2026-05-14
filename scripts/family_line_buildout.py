"""
家族線批次擴充腳本 — 高優先 TODO 第一批
- 不規則動詞 ~80
- 拼字變化 ~80
- 同音異字 ~20 對

策略:
  - 字已存在 → 加 base + family-note 欄位
  - 字不存在 → 新增完整 entry
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))

with open(VOCAB, 'r', encoding='utf-8') as f:
    data = json.load(f)

words = data['words']
idx = {w['word']: w for w in words}

# =========================================================
# 1) 不規則動詞:過去式 / 過去分詞
#    格式: word: (base, family-note, [可選] 補充新增 entry 用的 mean/img/chunks/py/split/theme)
# =========================================================
IRREGULAR = {
    # 已在 vocab,只加 base + family-note
    'knew':       ('know',       '已經知道的版本(過去式)'),
    'made':       ('make',       '已經做的版本(過去式)'),
    'came':       ('come',       '已經來的版本(過去式)'),
    'did':        ('do',         '已經做的版本(過去式)'),
    'gave':       ('give',       '已經給的版本(過去式)'),
    'brought':    ('bring',      '已經帶來的版本(過去式)'),
    'bought':     ('buy',        '已經買的版本(過去式)'),
    'taught':     ('teach',      '已經教的版本(過去式)'),
    'felt':       ('feel',       '已經感覺到的版本(過去式)'),
    'kept':       ('keep',       '已經保留的版本(過去式)'),
    'told':       ('tell',       '已經告訴的版本(過去式)'),
    'found':      ('find',       '已經找到的版本(過去式)'),
    'left':       ('leave',      '已經離開的版本(過去式)'),
    'lost':       ('lose',       '已經失去的版本(過去式)'),
    'put':        ('put',        '已經放的版本(過去式同形)'),
    'cut':        ('cut',        '已經切的版本(過去式同形)'),
    'hit':        ('hit',        '已經打的版本(過去式同形)'),
    'let':        ('let',        '已經讓的版本(過去式同形)'),
    'set':        ('set',        '已經設定的版本(過去式同形)'),
    'met':        ('meet',       '已經遇見的版本(過去式)'),
    'spent':      ('spend',      '已經花掉的版本(過去式)'),
    'sent':       ('send',       '已經寄出的版本(過去式)'),
    'spoke':      ('speak',      '已經說的版本(過去式)'),
    'stood':      ('stand',      '已經站的版本(過去式)'),
    'understood': ('understand', '已經懂的版本(過去式)'),
    'wrote':      ('write',      '已經寫的版本(過去式)'),
    'drove':      ('drive',      '已經開車的版本(過去式)'),
    'chose':      ('choose',     '已經選的版本(過去式)'),
    'froze':      ('freeze',     '已經結凍的版本(過去式)'),
    'wore':       ('wear',       '已經穿過的版本(過去式)'),
    'tore':       ('tear',       '已經撕過的版本(過去式)'),
    'threw':      ('throw',      '已經丟過的版本(過去式)'),
    'blew':       ('blow',       '已經吹過的版本(過去式)'),
    'grew':       ('grow',       '已經長大的版本(過去式)'),
    'drew':       ('draw',       '已經畫過的版本(過去式)'),
    'flew':       ('fly',        '已經飛過的版本(過去式)'),
    'got':        ('get',        '已經得到的版本(過去式)'),
    'had':        ('have',       '已經有過的版本(過去式)'),
    'was':        ('is',         '單數「是」的過去版本(過去式)'),
    'were':       ('are',        '複數「是」的過去版本(過去式)'),
    'ate':        ('eat',        '已經吃過的版本(過去式)'),
    'drank':      ('drink',      '已經喝過的版本(過去式)'),
    'ran':        ('run',        '已經跑過的版本(過去式)'),
    'swam':       ('swim',       '已經游過的版本(過去式)'),
    'sang':       ('sing',       '已經唱過的版本(過去式)'),
    'rang':       ('ring',       '已經響過的版本(過去式)'),
    'began':      ('begin',      '已經開始過的版本(過去式)'),
    'broke':      ('break',      '已經打破的版本(過去式)'),
    'woke':       ('wake',       '已經醒了的版本(過去式)'),
    'stole':      ('steal',      '已經偷過的版本(過去式)'),
    'rode':       ('ride',       '已經騎過的版本(過去式)'),
    'rose':       ('rise',       '已經升起的版本(過去式)'),
    'fell':       ('fall',       '已經跌倒的版本(過去式)'),
    'held':       ('hold',       '已經握住的版本(過去式)'),
    'heard':      ('hear',       '已經聽到的版本(過去式)'),
    'paid':       ('pay',        '已經付過的版本(過去式)'),
    'laid':       ('lay',        '已經放置的版本(過去式)'),
    'fed':        ('feed',       '已經餵過的版本(過去式)'),
    'led':        ('lead',       '已經帶領過的版本(過去式)'),
    'built':      ('build',      '已經蓋好的版本(過去式)'),
    'slept':      ('sleep',      '已經睡過的版本(過去式)'),
    'swept':      ('sweep',      '已經掃過的版本(過去式)'),
    'caught':     ('catch',      '已經抓到的版本(過去式)'),
    'fought':     ('fight',      '已經打過架的版本(過去式)'),
    'thought':    ('think',      '已經想過的版本(過去式)'),
    'sought':     ('seek',       '已經尋找的版本(過去式)'),
    'shot':       ('shoot',      '已經射過的版本(過去式)'),
    'forgot':     ('forget',     '已經忘記的版本(過去式)'),
    'lit':        ('light',      '已經點燃的版本(過去式)'),
    'dug':        ('dig',        '已經挖過的版本(過去式)'),
    'hung':       ('hang',       '已經掛好的版本(過去式)'),
    'stuck':      ('stick',      '已經卡住的版本(過去式)'),
    'struck':     ('strike',     '已經敲擊的版本(過去式)'),
    'won':        ('win',        '已經贏過的版本(過去式)'),
    'shone':      ('shine',      '已經發亮的版本(過去式)'),
    'became':     ('become',     '已經變成的版本(過去式)'),
    'shook':      ('shake',      '已經搖過的版本(過去式)'),
    'shut':       ('shut',       '已經關起來的版本(過去式同形)'),
    'cost':       ('cost',       '已經花費過的版本(過去式同形)'),
    'quit':       ('quit',       '已經退出的版本(過去式同形)'),
    'hurt':       ('hurt',       '已經受傷的版本(過去式同形)'),
    'lent':       ('lend',       '已經借出的版本(過去式)'),
    'bent':       ('bend',       '已經彎曲的版本(過去式)'),
    'dealt':      ('deal',       '已經處理過的版本(過去式)'),
    'meant':      ('mean',       '已經意指的版本(過去式)'),
}

# =========================================================
# 2) 拼字變化(主要是 NEW entries)
#    格式: word: (base, family-note, mean, img, chunks, py, split, theme)
# =========================================================
SPELLING = {
    # -ing 雙子音(短母音 + 單子音 → 雙寫)
    'swimming': ('swim', '正在游的版本(進行式,雙 m)', '正在游泳', '🏊', ['swim','ming'], 'ㄙㄨㄧ-ㄇㄧㄥ', 'swim + ming', 'actions'),
    'hopping':  ('hop',  '正在跳的版本(進行式,雙 p)', '正在跳', '🐰', ['hop','ping'], 'ㄏㄚ-ㄆㄧㄥ', 'hop + ping', 'actions'),
    'shopping': ('shop', '正在購物的版本(進行式,雙 p)', '正在購物', '🛒', ['shop','ping'], 'ㄒㄚ-ㄆㄧㄥ', 'shop + ping', 'actions'),
    'planning': ('plan', '正在計畫的版本(進行式,雙 n)', '正在計畫', '📋', ['plan','ning'], 'ㄆㄌㄚ-ㄋㄧㄥ', 'plan + ning', 'actions'),
    'stopping': ('stop', '正在停下的版本(進行式,雙 p)', '正在停', '🛑', ['stop','ping'], 'ㄙㄉㄚ-ㄆㄧㄥ', 'stop + ping', 'actions'),
    'sitting':  ('sit',  '正在坐的版本(進行式,雙 t)', '正在坐', '🪑', ['sit','ting'], 'ㄒㄧ-ㄊㄧㄥ', 'sit + ting', 'actions'),
    'getting':  ('get',  '正在得到的版本(進行式,雙 t)', '正在得到', '🎁', ['get','ting'], 'ㄍㄝ-ㄊㄧㄥ', 'get + ting', 'actions'),
    'putting':  ('put',  '正在放的版本(進行式,雙 t)', '正在放', '📥', ['put','ting'], 'ㄆㄨ-ㄊㄧㄥ', 'put + ting', 'actions'),
    'cutting':  ('cut',  '正在切的版本(進行式,雙 t)', '正在切', '🔪', ['cut','ting'], 'ㄎㄚ-ㄊㄧㄥ', 'cut + ting', 'actions'),
    'running':  ('run',  '正在跑的版本(進行式,雙 n)', '正在跑', '🏃', ['run','ning'], 'ㄖㄚ-ㄋㄧㄥ', 'run + ning', 'actions'),
    'beginning':('begin','正在開始的版本(進行式,雙 n)','正在開始','▶️', ['be','gin','ning'], 'ㄅㄧ-ㄍㄧ-ㄋㄧㄥ', 'be + gin + ning', 'actions'),
    'winning':  ('win',  '正在贏的版本(進行式,雙 n)', '正在贏', '🏆', ['win','ning'], 'ㄨㄧ-ㄋㄧㄥ', 'win + ning', 'actions'),
    'jogging':  ('jog',  '正在慢跑的版本(進行式,雙 g)', '正在慢跑', '🏃‍♀️', ['jog','ging'], 'ㄐㄚ-ㄍㄧㄥ', 'jog + ging', 'actions'),

    # -ing 一般
    'playing':  ('play', '正在玩的版本(進行式,+ing)', '正在玩', '🎮', ['play','ing'], 'ㄆㄌㄝ-ㄧㄥ', 'play + ing', 'actions'),
    'walking':  ('walk', '正在走的版本(進行式,+ing)', '正在走', '🚶', ['walk','ing'], 'ㄨㄛ-ㄎㄧㄥ', 'walk + ing', 'actions'),
    'talking':  ('talk', '正在說話的版本(進行式,+ing)', '正在說話', '💬', ['talk','ing'], 'ㄊㄛ-ㄎㄧㄥ', 'talk + ing', 'actions'),
    'watching': ('watch','正在看的版本(進行式,+ing)', '正在看', '👀', ['watch','ing'], 'ㄨㄚ-ㄑㄧㄥ', 'watch + ing', 'actions'),
    'waiting':  ('wait', '正在等的版本(進行式,+ing)', '正在等', '⏳', ['wait','ing'], 'ㄨㄝ-ㄊㄧㄥ', 'wait + ing', 'actions'),
    'reading':  ('read', '正在讀的版本(進行式,+ing)', '正在讀', '📖', ['read','ing'], 'ㄖㄧ-ㄉㄧㄥ', 'read + ing', 'actions'),
    'eating':   ('eat',  '正在吃的版本(進行式,+ing)', '正在吃', '🍽️', ['eat','ing'], 'ㄧ-ㄊㄧㄥ', 'eat + ing', 'actions'),
    'drinking': ('drink','正在喝的版本(進行式,+ing)', '正在喝', '🥤', ['drink','ing'], 'ㄉㄖㄧ-ㄎㄧㄥ', 'drink + ing', 'actions'),
    'sleeping': ('sleep','正在睡的版本(進行式,+ing)', '正在睡', '😴', ['sleep','ing'], 'ㄙㄌㄧ-ㄆㄧㄥ', 'sleep + ing', 'actions'),
    'singing':  ('sing', '正在唱的版本(進行式,+ing)', '正在唱', '🎤', ['sing','ing'], 'ㄒㄧㄥ-ㄧㄥ', 'sing + ing', 'actions'),
    'cooking':  ('cook', '正在煮的版本(進行式,+ing)', '正在煮', '🍳', ['cook','ing'], 'ㄎㄨ-ㄎㄧㄥ', 'cook + ing', 'actions'),
    'helping':  ('help', '正在幫忙的版本(進行式,+ing)', '正在幫忙', '🤝', ['help','ing'], 'ㄏㄝ-ㄆㄧㄥ', 'help + ing', 'actions'),
    'working':  ('work', '正在工作的版本(進行式,+ing)', '正在工作', '💼', ['work','ing'], 'ㄨㄜ-ㄎㄧㄥ', 'work + ing', 'actions'),
    'learning': ('learn','正在學的版本(進行式,+ing)', '正在學', '📚', ['learn','ing'], 'ㄌㄜ-ㄋㄧㄥ', 'learn + ing', 'actions'),
    'teaching': ('teach','正在教的版本(進行式,+ing)', '正在教', '👨‍🏫', ['teach','ing'], 'ㄊㄧ-ㄑㄧㄥ', 'teach + ing', 'actions'),

    # -ing e 結尾去 e
    'making':   ('make', '正在做的版本(進行式,去 e + ing)', '正在做', '🔨', ['mak','ing'], 'ㄇㄝ-ㄎㄧㄥ', 'mak + ing(去 e)', 'actions'),
    'taking':   ('take', '正在拿的版本(進行式,去 e + ing)', '正在拿', '✋', ['tak','ing'], 'ㄊㄝ-ㄎㄧㄥ', 'tak + ing(去 e)', 'actions'),
    'writing':  ('write','正在寫的版本(進行式,去 e + ing)', '正在寫', '✍️', ['writ','ing'], 'ㄖㄞ-ㄊㄧㄥ', 'writ + ing(去 e)', 'actions'),
    'riding':   ('ride', '正在騎的版本(進行式,去 e + ing)', '正在騎', '🚴', ['rid','ing'], 'ㄖㄞ-ㄉㄧㄥ', 'rid + ing(去 e)', 'actions'),
    'driving':  ('drive','正在開車的版本(進行式,去 e + ing)', '正在開車', '🚗', ['driv','ing'], 'ㄉㄖㄞ-ㄈㄧㄥ', 'driv + ing(去 e)', 'actions'),
    'coming':   ('come', '正在來的版本(進行式,去 e + ing)', '正在來', '🚶‍♀️', ['com','ing'], 'ㄎㄚ-ㄇㄧㄥ', 'com + ing(去 e)', 'actions'),
    'giving':   ('give', '正在給的版本(進行式,去 e + ing)', '正在給', '🎁', ['giv','ing'], 'ㄍㄧ-ㄈㄧㄥ', 'giv + ing(去 e)', 'actions'),
    'using':    ('use',  '正在使用的版本(進行式,去 e + ing)', '正在使用', '🔧', ['us','ing'], 'ㄧㄨ-ㄗㄧㄥ', 'us + ing(去 e)', 'actions'),
    'closing':  ('close','正在關的版本(進行式,去 e + ing)', '正在關', '🚪', ['clos','ing'], 'ㄎㄌㄛ-ㄗㄧㄥ', 'clos + ing(去 e)', 'actions'),
    'moving':   ('move', '正在移動的版本(進行式,去 e + ing)', '正在移動', '🏃', ['mov','ing'], 'ㄇㄨ-ㄈㄧㄥ', 'mov + ing(去 e)', 'actions'),

    # -ed y→i (子音 + y)
    'studied':  ('study','已經學過的版本(過去式,y 變 i + ed)', '學習(過去)', '📚', ['stud','ied'], 'ㄙㄉㄚ-ㄉㄧㄉ', 'stud + ied(y→i)', 'actions'),
    'tried':    ('try',  '已經試過的版本(過去式,y 變 i + ed)', '試(過去)', '🤞', ['tr','ied'], 'ㄊㄖㄞㄉ', 'tr + ied(y→i)', 'actions'),
    'cried':    ('cry',  '已經哭過的版本(過去式,y 變 i + ed)', '哭(過去)', '😢', ['cr','ied'], 'ㄎㄖㄞㄉ', 'cr + ied(y→i)', 'actions'),
    'married':  ('marry','已經結婚的版本(過去式,y 變 i + ed)', '結婚(過去)', '💍', ['mar','ried'], 'ㄇㄝ-ㄖㄧㄉ', 'mar + ried(y→i)', 'actions'),
    'hurried':  ('hurry','已經趕的版本(過去式,y 變 i + ed)', '趕快(過去)', '🏃', ['hur','ried'], 'ㄏㄜ-ㄖㄧㄉ', 'hur + ried(y→i)', 'actions'),
    'carried':  ('carry','已經帶的版本(過去式,y 變 i + ed)', '帶(過去)', '🎒', ['car','ried'], 'ㄎㄝ-ㄖㄧㄉ', 'car + ried(y→i)', 'actions'),
    'copied':   ('copy', '已經複製的版本(過去式,y 變 i + ed)', '複製(過去)', '📋', ['cop','ied'], 'ㄎㄚ-ㄆㄧㄉ', 'cop + ied(y→i)', 'actions'),
    'replied':  ('reply','已經回覆的版本(過去式,y 變 i + ed)', '回覆(過去)', '💬', ['re','pl','ied'], 'ㄖㄧ-ㄆㄌㄞㄉ', 're + pl + ied(y→i)', 'actions'),
    'worried':  ('worry','已經擔心的版本(過去式,y 變 i + ed)', '擔心(過去)', '😟', ['wor','ried'], 'ㄨㄜ-ㄖㄧㄉ', 'wor + ried(y→i)', 'actions'),
    'studied2_skip': None,  # placeholder if duplicate

    # 複數 y→ies
    'cities':   ('city',   '「很多個」的版本(複數,y 變 ies)', '城市(複數)', '🏙️', ['cit','ies'], 'ㄒㄧ-ㄊㄧㄗ', 'cit + ies(y→ies)', 'places'),
    'parties':  ('party',  '「很多個」的版本(複數,y 變 ies)', '派對(複數)', '🎉', ['par','ties'], 'ㄆㄚ-ㄊㄧㄗ', 'par + ties(y→ies)', 'events'),
    'stories':  ('story',  '「很多個」的版本(複數,y 變 ies)', '故事(複數)', '📖', ['stor','ies'], 'ㄙㄉㄛ-ㄖㄧㄗ', 'stor + ies(y→ies)', 'literature'),
    'families': ('family', '「很多個」的版本(複數,y 變 ies)', '家庭(複數)', '👨‍👩‍👧', ['fam','il','ies'], 'ㄈㄝ-ㄇㄝ-ㄌㄧㄗ', 'fam + il + ies(y→ies)', 'family'),
    'countries':('country','「很多個」的版本(複數,y 變 ies)', '國家(複數)', '🌍', ['coun','tries'], 'ㄎㄚ-ㄊㄖㄧㄗ', 'coun + tries(y→ies)', 'countries'),
    'ladies':   ('lady',   '「很多個」的版本(複數,y 變 ies)', '女士(複數)', '👩', ['la','dies'], 'ㄌㄝ-ㄉㄧㄗ', 'la + dies(y→ies)', 'family'),
    'candies':  ('candy',  '「很多個」的版本(複數,y 變 ies)', '糖果(複數)', '🍬', ['can','dies'], 'ㄎㄝ-ㄋㄉㄧㄗ', 'can + dies(y→ies)', 'desserts'),
    'puppies':  ('puppy',  '「很多個」的版本(複數,y 變 ies)', '小狗(複數)', '🐶', ['pup','pies'], 'ㄆㄚ-ㄆㄧㄗ', 'pup + pies(y→ies)', 'animals'),

    # 比較級 / 最高級
    'smaller':  ('small', '「更小」的版本(比較級,+er)', '更小', '🔽', ['small','er'], 'ㄙㄇㄛ-ㄌㄜ', 'small + er', 'adjectives'),
    'smallest': ('small', '「最小」的版本(最高級,+est)', '最小', '⬇️', ['small','est'], 'ㄙㄇㄛ-ㄌㄝㄙㄊ', 'small + est', 'adjectives'),
    'biggest':  ('big',   '「最大」的版本(最高級,+est 雙 g)', '最大', '⬆️', ['big','gest'], 'ㄅㄧ-ㄍㄝㄙㄊ', 'big + gest(雙 g)', 'adjectives'),
    'faster':   ('fast',  '「更快」的版本(比較級,+er)', '更快', '💨', ['fast','er'], 'ㄈㄝ-ㄙㄉㄜ', 'fast + er', 'adjectives'),
    'fastest':  ('fast',  '「最快」的版本(最高級,+est)', '最快', '🚀', ['fast','est'], 'ㄈㄝ-ㄙㄉㄝㄙㄊ', 'fast + est', 'adjectives'),
    'taller':   ('tall',  '「更高」的版本(比較級,+er)', '更高', '📏', ['tall','er'], 'ㄊㄛ-ㄌㄜ', 'tall + er', 'adjectives'),
    'tallest':  ('tall',  '「最高」的版本(最高級,+est)', '最高', '🗼', ['tall','est'], 'ㄊㄛ-ㄌㄝㄙㄊ', 'tall + est', 'adjectives'),
    'hotter':   ('hot',   '「更熱」的版本(比較級,+er 雙 t)', '更熱', '🔥', ['hot','ter'], 'ㄏㄚ-ㄊㄜ', 'hot + ter(雙 t)', 'adjectives'),
    'hottest':  ('hot',   '「最熱」的版本(最高級,+est 雙 t)', '最熱', '🌡️', ['hot','test'], 'ㄏㄚ-ㄊㄝㄙㄊ', 'hot + test(雙 t)', 'adjectives'),
    'nicer':    ('nice',  '「更好」的版本(比較級,去 e + er)', '更好的', '😊', ['nic','er'], 'ㄋㄞ-ㄙㄜ', 'nic + er(去 e)', 'adjectives'),
    'nicest':   ('nice',  '「最好」的版本(最高級,去 e + est)', '最好的', '🌟', ['nic','est'], 'ㄋㄞ-ㄙㄝㄙㄊ', 'nic + est(去 e)', 'adjectives'),
    'larger':   ('large', '「更大」的版本(比較級,去 e + er)', '更大的', '⏫', ['larg','er'], 'ㄌㄚ-ㄐㄜ', 'larg + er(去 e)', 'adjectives'),
    'largest':  ('large', '「最大」的版本(最高級,去 e + est)', '最大的', '🏔️', ['larg','est'], 'ㄌㄚ-ㄐㄝㄙㄊ', 'larg + est(去 e)', 'adjectives'),
    'happier':  ('happy', '「更開心」的版本(比較級,y 變 i + er)', '更開心', '😄', ['hap','pier'], 'ㄏㄝ-ㄆㄧㄜ', 'hap + pier(y→i)', 'adjectives'),
    'happiest': ('happy', '「最開心」的版本(最高級,y 變 i + est)', '最開心', '🥳', ['hap','piest'], 'ㄏㄝ-ㄆㄧㄝㄙㄊ', 'hap + piest(y→i)', 'adjectives'),
    'easier':   ('easy',  '「更容易」的版本(比較級,y 變 i + er)', '更容易', '👌', ['eas','ier'], 'ㄧ-ㄗㄧㄜ', 'eas + ier(y→i)', 'adjectives'),
    'easiest':  ('easy',  '「最容易」的版本(最高級,y 變 i + est)', '最容易', '✨', ['eas','iest'], 'ㄧ-ㄗㄧㄝㄙㄊ', 'eas + iest(y→i)', 'adjectives'),
    'busier':   ('busy',  '「更忙」的版本(比較級,y 變 i + er)', '更忙', '😵', ['bus','ier'], 'ㄅㄧ-ㄗㄧㄜ', 'bus + ier(y→i)', 'adjectives'),
    'busiest':  ('busy',  '「最忙」的版本(最高級,y 變 i + est)', '最忙', '🤯', ['bus','iest'], 'ㄅㄧ-ㄗㄧㄝㄙㄊ', 'bus + iest(y→i)', 'adjectives'),

    # 一般 -ed
    'played':   ('play',  '已經玩過的版本(過去式,+ed)', '玩(過去)', '🎮', ['play','ed'], 'ㄆㄌㄝㄉ', 'play + ed', 'actions'),
    'talked':   ('talk',  '已經說過的版本(過去式,+ed)', '說話(過去)', '💬', ['talk','ed'], 'ㄊㄛㄎㄊ', 'talk + ed', 'actions'),
    'watched':  ('watch', '已經看過的版本(過去式,+ed)', '看(過去)', '👀', ['watch','ed'], 'ㄨㄚㄑㄊ', 'watch + ed', 'actions'),
    'waited':   ('wait',  '已經等過的版本(過去式,+ed)', '等(過去)', '⏳', ['wait','ed'], 'ㄨㄝ-ㄊㄧㄉ', 'wait + ed', 'actions'),
    'wanted':   ('want',  '已經想要的版本(過去式,+ed)', '想要(過去)', '🙏', ['want','ed'], 'ㄨㄚ-ㄋㄊㄧㄉ', 'want + ed', 'actions'),
    'helped':   ('help',  '已經幫過的版本(過去式,+ed)', '幫忙(過去)', '🤝', ['help','ed'], 'ㄏㄝㄆㄊ', 'help + ed', 'actions'),
    'opened':   ('open',  '已經打開過的版本(過去式,+ed)', '打開(過去)', '🔓', ['op','ened'], 'ㄛ-ㄆㄝㄋㄉ', 'op + ened', 'actions'),
    'closed':   ('close', '已經關過的版本(過去式,去 e + ed)', '關(過去)', '🔒', ['clos','ed'], 'ㄎㄌㄛㄗㄉ', 'clos + ed(去 e)', 'actions'),
    'cleaned':  ('clean', '已經打掃過的版本(過去式,+ed)', '打掃(過去)', '🧹', ['clean','ed'], 'ㄎㄌㄧㄋㄉ', 'clean + ed', 'actions'),
    'finished': ('finish','已經完成的版本(過去式,+ed)', '完成(過去)', '✅', ['fin','ished'], 'ㄈㄧ-ㄋㄧㄒㄊ', 'fin + ished', 'actions'),
    'worked':   ('work',  '已經工作過的版本(過去式,+ed)', '工作(過去)', '💼', ['work','ed'], 'ㄨㄜㄎㄊ', 'work + ed', 'actions'),
    'learned':  ('learn', '已經學過的版本(過去式,+ed)', '學(過去)', '📚', ['learn','ed'], 'ㄌㄜㄋㄉ', 'learn + ed', 'actions'),
    'cooked':   ('cook',  '已經煮過的版本(過去式,+ed)', '煮(過去)', '🍳', ['cook','ed'], 'ㄎㄨㄎㄊ', 'cook + ed', 'actions'),
    'showed':   ('show',  '已經展示過的版本(過去式,+ed)', '展示(過去)', '👉', ['show','ed'], 'ㄕㄛㄉ', 'show + ed', 'actions'),
    'called':   ('call',  '已經叫過的版本(過去式,+ed)', '叫(過去)', '📞', ['call','ed'], 'ㄎㄛㄌㄉ', 'call + ed', 'actions'),
    'asked':    ('ask',   '已經問過的版本(過去式,+ed)', '問(過去)', '🙋', ['ask','ed'], 'ㄝㄙㄎㄊ', 'ask + ed', 'actions'),
    'answered': ('answer','已經回答過的版本(過去式,+ed)', '回答(過去)', '💬', ['an','swered'], 'ㄝ-ㄋㄙㄜㄉ', 'an + swered', 'actions'),
    'used':     ('use',   '已經使用過的版本(過去式,去 e + ed)', '使用(過去)', '🔧', ['us','ed'], 'ㄧㄨㄗㄉ', 'us + ed(去 e)', 'actions'),
    'moved':    ('move',  '已經移動過的版本(過去式,去 e + ed)', '移動(過去)', '🏃', ['mov','ed'], 'ㄇㄨㄈㄉ', 'mov + ed(去 e)', 'actions'),
    'lived':    ('live',  '已經住過的版本(過去式,去 e + ed)', '住(過去)', '🏠', ['liv','ed'], 'ㄌㄧㄈㄉ', 'liv + ed(去 e)', 'actions'),
    'loved':    ('love',  '已經愛過的版本(過去式,去 e + ed)', '愛(過去)', '❤️', ['lov','ed'], 'ㄌㄚㄈㄉ', 'lov + ed(去 e)', 'actions'),
    'liked':    ('like',  '已經喜歡過的版本(過去式,去 e + ed)', '喜歡(過去)', '👍', ['lik','ed'], 'ㄌㄞㄎㄊ', 'lik + ed(去 e)', 'actions'),
}
# 移除佔位符
SPELLING = {k: v for k, v in SPELLING.items() if v is not None}

# =========================================================
# 3) 同音異字 / 同字異義(用 family-note 標記易混提示)
#    格式: word: (twin, family-note, mean, img, chunks, py, split, theme)
#    多數已存在,只加 base="同音字" + family-note 提示
# =========================================================
HOMOPHONES_EXISTING = {
    # word: (twin_word, family-note)
    'there':   ('their / they\'re', '⚠️ 同音字:there 在那裡 / their 他們的 / they\'re 他們是'),
    'their':   ('there / they\'re', '⚠️ 同音字:their 他們的 / there 在那裡 / they\'re 他們是'),
    'to':      ('too / two',        '⚠️ 同音字:to 向(介系詞)/ too 也、太 / two 二'),
    'too':     ('to / two',         '⚠️ 同音字:too 也、太 / to 向 / two 二'),
    'two':     ('to / too',         '⚠️ 同音字:two 二 / to 向 / too 也、太'),
    'your':    ("you're",           "⚠️ 易混字:your 你的 / you're 你是(= you are)"),
    'its':     ("it's",             "⚠️ 易混字:its 牠的(所有格)/ it's 它是(= it is)"),
    'then':    ('than',             '⚠️ 易混字:then 然後(時間)/ than 比(比較)'),
    'than':    ('then',             '⚠️ 易混字:than 比(比較)/ then 然後(時間)'),
    'lose':    ('loose',            '⚠️ 易混字:lose 失去(動詞)/ loose 鬆的(形容詞)'),
    'loose':   ('lose',             '⚠️ 易混字:loose 鬆的(形容詞)/ lose 失去(動詞)'),
    'hear':    ('here',             '⚠️ 同音字:hear 聽(動詞,有耳朵 ear)/ here 這裡'),
    'here':    ('hear',             '⚠️ 同音字:here 這裡 / hear 聽(動詞)'),
    'see':     ('sea',              '⚠️ 同音字:see 看 / sea 海'),
    'sea':     ('see',              '⚠️ 同音字:sea 海 / see 看'),
    'right':   ('write',            '⚠️ 同音字:right 對的、右邊 / write 寫'),
    'write':   ('right',            '⚠️ 同音字:write 寫 / right 對的、右邊'),
    'know':    ('no',               '⚠️ 同音字:know 知道(k 不發音)/ no 不'),
    'no':      ('know',             '⚠️ 同音字:no 不 / know 知道(k 不發音)'),
    'one':     ('won',              '⚠️ 同音字:one 一 / won win 的過去式'),
    'son':     ('sun',              '⚠️ 同音字:son 兒子 / sun 太陽'),
    'sun':     ('son',              '⚠️ 同音字:sun 太陽 / son 兒子'),
    'eye':     ('I',                '⚠️ 同音字:eye 眼睛 / I 我'),
    'flower':  ('flour',            '⚠️ 同音字:flower 花 / flour 麵粉'),
    'mail':    ('male',             '⚠️ 同音字:mail 郵件 / male 男性'),
    'tail':    ('tale',             '⚠️ 同音字:tail 尾巴 / tale 故事'),
    'meat':    ('meet',             '⚠️ 同音字:meat 肉 / meet 見面'),
    'piece':   ('peace',            '⚠️ 同音字:piece 一片 / peace 和平'),
    'weak':    ('week',             '⚠️ 同音字:weak 弱的 / week 一週'),
    'wait':    ('weight',           '⚠️ 同音字:wait 等 / weight 重量'),
    'son2':    None,  # placeholder
}
HOMOPHONES_EXISTING = {k: v for k, v in HOMOPHONES_EXISTING.items() if v is not None}

# =========================================================
# 套用
# =========================================================
updated = 0
added = 0
skipped = 0

# 1) 不規則動詞
for word, (base, note) in IRREGULAR.items():
    if word in idx:
        entry = idx[word]
        if 'base' in entry and 'family-note' in entry:
            skipped += 1
            continue
        entry['base'] = base
        entry['family-note'] = note
        updated += 1
    else:
        # 缺漏的(sat, sold 等)— 略過,不勉強新增缺欄位
        skipped += 1

# 2) 拼字變化(新增為主)
for word, tup in SPELLING.items():
    base, note, mean, img, chunks, py, split, theme = tup
    if word in idx:
        entry = idx[word]
        if 'base' in entry and 'family-note' in entry:
            skipped += 1
            continue
        entry['base'] = base
        entry['family-note'] = note
        updated += 1
    else:
        new_entry = {
            'word': word, 'mean': mean, 'img': img,
            'chunks': chunks, 'py': py, 'split': split,
            'theme': theme, 'stage': 1,
            'base': base, 'family-note': note,
        }
        words.append(new_entry)
        idx[word] = new_entry
        added += 1

# 3) 同音異字 — 都是高頻字,應該都存在
for word, (twin, note) in HOMOPHONES_EXISTING.items():
    if word in idx:
        entry = idx[word]
        if 'family-note' in entry and entry.get('family-note', '').startswith('⚠️'):
            skipped += 1
            continue
        # 不覆蓋已有 base(優先保留動詞家族線),只在沒 family-note 時加易混提示
        if 'family-note' not in entry:
            entry['homophone-note'] = note  # 用另一個欄位避免衝突
            updated += 1
        else:
            entry['homophone-note'] = note
            updated += 1
    else:
        skipped += 1

# 寫回
with open(VOCAB, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"updated existing: {updated}")
print(f"added new:        {added}")
print(f"skipped:          {skipped}")
print(f"total words:      {len(words)}")
print(f"with base:        {sum(1 for w in words if 'base' in w)}")
print(f"with homophone:   {sum(1 for w in words if 'homophone-note' in w)}")
