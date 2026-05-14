"""修翻譯品質問題"""
import json, os, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

# 1) 亂符號殘留 — 直接清掉多餘 `[`, `]`, `=`, `+`
WEIRD_FIX = {
    'admit':      '承認、坦承',
    'handful':    '一把、一握',
    'heap':       '堆、堆積',
    'pavement':   '人行道',
    'applicant':  '申請人',
    'assistance': '援助、幫助',
    'brassiere':  '胸罩',
    'confess':    '坦白、承認',
    'verb':       '動詞',
}

# 2) 純英文未翻 — 有意義中文的補,真專有名詞留原文
EN_FIX = {
    'wifi':      'Wi-Fi 無線網路',
    'hi-fi':     'Hi-Fi 高傳真音響',
    'python':    'Python 程式語言',
    'java':      'Java 程式語言',
    'github':    'GitHub 程式碼平台',
    'slack':     'Slack 工作通訊軟體',
    'discord':   'Discord 通訊軟體',
    'zoom':      'Zoom 視訊軟體',
    'instagram': 'Instagram(IG)社群',
    'threads':   'Threads 社群',
    'snapchat':  'Snapchat 社群',
    'youtube':   'YouTube 影音平台',
    'google':    'Google 搜尋引擎',
    'gmail':     'Gmail 電子郵件',
    'vpn':       'VPN 虛擬私人網路',
    'https':     'HTTPS 加密網址',
    'gpt':       'GPT(AI 模型)',
    'dna':       'DNA 去氧核醣核酸',
    'rna':       'RNA 核糖核酸',
}

# 3) p.p. 改白話
TERM_FIX = {
    'eaten': '吃過了(配 have 用)',
}

# 4) 成語沒翻完
IDIOM_FIX = {
    'chip off the old block': '一個模子刻出來的(像爸媽的孩子)',
}

fixed = 0
for d in (WEIRD_FIX, EN_FIX, TERM_FIX, IDIOM_FIX):
    for word, new_mean in d.items():
        if word in idx:
            old = idx[word].get('mean','')
            idx[word]['mean'] = new_mean
            print(f"  {word:30s} | {old:25s} → {new_mean}")
            fixed += 1

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nfixed: {fixed}")
