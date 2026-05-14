"""數字主題:2+ 位數改用純數字文字,清楚易讀"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']

NUMBER_FIX = {
    # 10-19
    'eleven':    '11',
    'twelve':    '12',
    'thirteen':  '13',
    'fourteen':  '14',
    'fifteen':   '15',
    'sixteen':   '16',
    'seventeen': '17',
    'eighteen':  '18',
    'nineteen':  '19',
    # 20-90
    'twenty':    '20',
    'thirty':    '30',
    'forty':     '40',
    'fifty':     '50',
    'sixty':     '60',
    'seventy':   '70',
    'eighty':    '80',
    'ninety':    '90',
    # 大數字
    'hundred':   '100',
    'thousand':  '1,000',
    'million':   '100萬',
    'billion':   '10億',
    # 序數(4th 起)
    'fourth':    '4th',
    'fifth':     '5th',
    'sixth':     '6th',
    'seventh':   '7th',
    'eighth':    '8th',
    'ninth':     '9th',
    'tenth':     '10th',
    # 倍數
    'double':    '×2',
    'triple':    '×3',
    'half':      '½',
    'quarter':   '¼',
}

n = 0
for w in words:
    if w['word'] in NUMBER_FIX:
        old = w.get('img','')
        w['img'] = NUMBER_FIX[w['word']]
        print(f"  {w['word']:12s} {old:8s} → {w['img']}")
        n += 1

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nfixed: {n}")
