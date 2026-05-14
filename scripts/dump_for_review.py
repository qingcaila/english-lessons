"""把 vocab 切成 500 字一檔的 word|mean|theme 對照表"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
OUTDIR = os.path.normpath(os.path.join(HERE, 'review'))
os.makedirs(OUTDIR, exist_ok=True)
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']

BATCH = 500
for i in range(0, len(words), BATCH):
    chunk = words[i:i+BATCH]
    path = os.path.join(OUTDIR, f'batch_{i//BATCH:02d}.txt')
    with open(path,'w',encoding='utf-8') as f:
        f.write(f"# 字 {i} - {i+len(chunk)-1} 共 {len(chunk)} 筆\n")
        for j, w in enumerate(chunk):
            f.write(f"{i+j:5d} | {w['word']:30s} | {w.get('mean',''):30s} | {w.get('theme','')}\n")
print(f"dumped {len(words)} words into {len(words)//BATCH + 1} batches")
print(f"output: {OUTDIR}")
