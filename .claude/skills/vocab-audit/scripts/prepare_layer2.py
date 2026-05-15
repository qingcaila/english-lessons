"""切批次 + 印出該派幾個 agent + agent prompt 模板"""
import json, os, sys, io
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
VOCAB = os.path.join(ROOT, 'vocab.json')
PROMPTS = os.path.normpath(os.path.join(HERE, '..', 'prompts'))
BATCHES = os.path.normpath(os.path.join(HERE, '..', 'batches'))

if len(sys.argv) < 2:
    print("用法: python prepare_layer2.py {check_id} [batch_size=500] [agent_count=7]")
    print()
    print("可選 check_id:")
    for f in sorted(os.listdir(PROMPTS)):
        if f.endswith('.md'):
            print(f"  - {f[:-3]}")
    sys.exit(1)

check_id = sys.argv[1]
batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 500
agent_count = int(sys.argv[3]) if len(sys.argv) > 3 else 7

prompt_path = os.path.join(PROMPTS, f'{check_id}.md')
if not os.path.exists(prompt_path):
    print(f"❌ 找不到 prompt: {prompt_path}")
    sys.exit(1)

with open(VOCAB, 'r', encoding='utf-8') as f: data = json.load(f)
words = data['words']

# 切批次
os.makedirs(BATCHES, exist_ok=True)
date = datetime.now().strftime('%Y%m%d')
batch_dir = os.path.join(BATCHES, f'{date}-{check_id}')
os.makedirs(batch_dir, exist_ok=True)

n_batches = (len(words) + batch_size - 1) // batch_size
for i in range(n_batches):
    chunk = words[i*batch_size:(i+1)*batch_size]
    with open(os.path.join(batch_dir, f'batch_{i:02d}.txt'), 'w', encoding='utf-8') as f:
        f.write(f"# 字 {i*batch_size}-{i*batch_size+len(chunk)-1}\n")
        for j, w in enumerate(chunk):
            base = f" base={w['base']}" if 'base' in w else ''
            homo = " [有易混提示]" if 'homophone-note' in w else ''
            f.write(f"{i*batch_size+j:5d} | {w['word']:30s} | {w.get('mean',''):30s} | {w.get('img','?'):8s} | chunks={w.get('chunks')} | py={w.get('py','')} | theme={w.get('theme','')} | stage={w.get('stage')}{base}{homo}\n")

# 切 agent 分組
batches_per_agent = (n_batches + agent_count - 1) // agent_count

with open(prompt_path, 'r', encoding='utf-8') as f:
    prompt_template = f.read()

print(f"✅ 切 {n_batches} 個批次到 {batch_dir}")
print(f"   建議派 {agent_count} 個 agent,每個負責 {batches_per_agent} 批次")
print()
print("="*60)
print("派 agent 指令(複製貼到 Agent tool):")
print("="*60)
for a in range(agent_count):
    start = a * batches_per_agent
    end = min(start + batches_per_agent, n_batches)
    if start >= n_batches: break
    batches = [f'batch_{i:02d}.txt' for i in range(start, end)]
    files_md = '\n'.join(f'- {os.path.join(batch_dir, b)}'.replace('\\','/') for b in batches)
    print(f"\n--- Agent {a+1} (batches {start}-{end-1}) ---")
    print(f"description: {check_id} 審查 batch {start}-{end-1}")
    print(f"prompt:")
    print(prompt_template.replace('{FILES}', files_md))
    print()
