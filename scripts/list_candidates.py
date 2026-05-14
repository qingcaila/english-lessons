"""列出所有「沒 base」的字尾候選 + 中文意思,匯出 JSON"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
OUT = os.path.normpath(os.path.join(HERE, 'candidates.json'))
with open(VOCAB, 'r', encoding='utf-8') as f:
    data = json.load(f)
words = data['words']
word_set = {w['word'] for w in words}
idx = {w['word']: w for w in words}

SUF = ['iest','iness','ation','ition','ution','ment','ness','able','ible','tion','sion',
       'less','ful','ous','ive','ize','ise','ies','ied','ier',
       'ing','ed','est','er','or','ly','al','y','s']

def stems_for(word, suf):
    out = []
    n = len(suf)
    base = word[:-n]
    if not base: return out
    out.append(base)
    if len(base) >= 2 and base[-1] == base[-2] and base[-1] not in 'aeiou':
        out.append(base[:-1])
    out.append(base + 'e')
    if suf in ('ies','ied','ier','iest'):
        if base.endswith('i'):
            out.append(base[:-1] + 'y')
    if suf in ('ation','ition','ution'):
        # creation ← create
        out.append(base + 'e')
    return out

results = []
for w in words:
    if 'base' in w: continue
    word = w['word']
    if len(word) < 4: continue
    for suf in SUF:
        if not word.endswith(suf): continue
        for stem in stems_for(word, suf):
            if stem in word_set and stem != word and len(stem) >= 2:
                results.append({
                    'word': word, 'stem': stem, 'suf': suf,
                    'mean': w.get('mean',''),
                    'stem_mean': idx[stem].get('mean','')
                })
                break
        else:
            continue
        break

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"total: {len(results)}")
import collections
c = collections.Counter(r['suf'] for r in results)
for k,v in sorted(c.items(),key=lambda x:-x[1]):
    print(f"  -{k}: {v}")
