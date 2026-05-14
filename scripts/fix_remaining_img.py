"""修剩下 10 個還是 📦 的字"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']

FIX = {
    'thing':     '🔵',
    'package':   '📮',
    'parcel':    '📮',
    'stock':     '📊',
    'product':   '🏷️',
    'supply':    '🚛',
    'move in':   '🏠',
    'move out':  '🚪',
    'cardboard': '🟫',
    'ample':     '🌊',
}
n = 0
for w in words:
    if w['word'] in FIX and w.get('img') == '📦':
        w['img'] = FIX[w['word']]
        n += 1

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"fixed: {n}")
