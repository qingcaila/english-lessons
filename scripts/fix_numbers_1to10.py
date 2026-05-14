"""數字 1-10 + 序數 1st-3rd 統一改純文字"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']

FIX = {
    'zero':   '0',
    'one':    '1',
    'two':    '2',
    'three':  '3',
    'four':   '4',
    'five':   '5',
    'six':    '6',
    'seven':  '7',
    'eight':  '8',
    'nine':   '9',
    'ten':    '10',
    'first':  '1st',
    'second': '2nd',
    'third':  '3rd',
}
n = 0
for w in words:
    if w['word'] in FIX:
        old = w.get('img','')
        w['img'] = FIX[w['word']]
        print(f"  {w['word']:10s} {old:6s} → {w['img']}")
        n += 1

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nfixed: {n}")
