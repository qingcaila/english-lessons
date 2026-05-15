"""補最後 10 組同音/易混字"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

HOMO = {
    'wrap':       '⚠️ 同音字:wrap 包裹(w 不發音)/ rap 饒舌',
    'read':       '⚠️ 同音字:read 讀(過去式唸 ㄖㄝㄉ,跟 red 同音)/ red 紅色',
    'set':        '⚠️ 易混字:set 設置 / sit 坐 / seat 座位',
    'historic':   '⚠️ 易混字:historic 歷史上重大的(historic moment)/ historical 跟歷史有關的(historical novel)',
    'historical': '⚠️ 易混字:historical 跟歷史有關的 / historic 歷史上重大的',
    'economic':   '⚠️ 易混字:economic 跟經濟有關的 / economical 划算的、節省的',
    'economical': '⚠️ 易混字:economical 划算的、節省的 / economic 跟經濟有關的',
    'classic':    '⚠️ 易混字:classic 經典的、典型的 / classical 古典(音樂、文學)的',
    'classical':  '⚠️ 易混字:classical 古典(音樂、文學)的 / classic 經典的、典型的',
    'continuous': '⚠️ 易混字:continuous 連續不斷(沒停過)/ continual 一直反覆(中間有停)',
    'continual':  '⚠️ 易混字:continual 一直反覆(中間有停)/ continuous 連續不斷(沒停過)',
    'amount':     '⚠️ 易混字:amount 「量」(不可數,amount of water)/ number 「數量」(可數,number of people)',
    'number':     '⚠️ 易混字:number 「數量」(可數,number of people)/ amount 「量」(不可數,amount of water)',
    'loss':       '⚠️ 易混字:loss 損失(名詞)/ lose 失去(動詞)/ loose 鬆的(形容詞)',
    'arise':      '⚠️ 易混字:arise 出現、發生(問題)/ rise 上升(數量、太陽)/ raise 抬起(及物)',
}

n = 0
for word, note in HOMO.items():
    if word in idx and 'homophone-note' not in idx[word]:
        idx[word]['homophone-note'] = note
        n += 1

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"補了 {n} 字")
print(f"總 homophone: {sum(1 for w in words if 'homophone-note' in w)}")
