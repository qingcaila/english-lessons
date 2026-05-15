"""套用 stage-fit 修正 — stage 分級重新校準"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

# word: new_stage
FIXES = {
    # === batch 1:基礎字標太高 / 罕用字標太低 ===
    'museum':1, 'supermarket':1, 'restaurant':1, 'cafe':1, 'bicycle':1, 'church':1,
    'purchase':2, 'refund':2, 'salary':2, 'wage':2, 'injury':2, 'treatment':2,
    'appointment':2, 'painkiller':2, 'infant':2,
    'freight':2, 'acquaintance':2,
    'hostel':1, 'international':2, 'motorcycle':2, 'helicopter':2, 'ambulance':2,
    'adventure':2, 'furious':3, 'compassion':2, 'empathy':2, 'sympathy':2,
    'obviously':1, 'definitely':1,

    # === batch 2:政治 / 性格 / 藝術 / 醫療 ===
    'attorney':3, 'diplomat':3, 'ambassador':3, 'senator':3,
    'hostile':3, 'reserved':3, 'introverted':3, 'extroverted':3,
    'tactful':4, 'diplomatic':3, 'sentimental':2, 'sarcastic':3,
    'articulate':2, 'temperamental':4, 'infatuation':4,
    'vulnerability':2, 'compatibility':2, 'infidelity':4,
    'reconcile':2, 'despise':2, 'loathe':4,
    'alliance':2, 'kinship':4, 'fellowship':2, 'frenemy':4, 'betrayal':2,
    'affection':1, 'figurine':3,
    'mecha':4, 'labyrinth':2, 'trinket':4, 'novelty':2,
    'calligraphy':3, 'acrylic':2, 'fresco':4,
    'impressionism':2, 'surrealism':2,
    'meditation':1, 'karaoke':0, 'taichi':1, 'qigong':2,
    'enthusiast':2, 'fanatic':2,
    'hemorrhage':4, 'anesthetic':2, 'covid':0,
    'schizophrenia':4, 'tuberculosis':2,
    'socialism':1, 'capitalism':1, 'communism':1,

    # === batch 3:政治 / 宗教 / 抽象 ===
    'sos':2, 'cpr':3, 'homicide':3,
    'democrat':2, 'republican':2, 'primeminister':2, 'congress':2,
    'investigation':2, 'evidence':2, 'defense':2, 'justice':2,
    'rights':2, 'innocent':2,
    'christianity':2, 'islam':2, 'muslim':2,
    'buddhism':2, 'buddhist':2, 'jew':2, 'jewish':2,
    'catholic':2, 'christian':2,
    'messiah':4, 'philosophy':2, 'logic':2,
    'thrice':4, 'firstaid':2,
    'analyze':2, 'data':2, 'globe':2, 'input':2,
    'tense':2, 'symbol':2, 'comment':2, 'layer':2,
    'feature':2, 'summary':2, 'paragraph':2,

    # === batch 4:過時詞 / 罕用拼法 / 借詞 ===
    'luncheon':3, 'trousers':2, 'xerox':3, 'confucius':3,
    'cassette':3, 'firewoman':3, 'icebox':3,
    'momma':2, 'cooky':2, 'papa':2, 'pa':2, 'xmas':2,
    'cub':2, 'cowboy':2, 'weigh':2, 'lily':2, 'yucky':2,
    'buck':2, 'shall':2, 'tummy':2, 'chief':2,
    'granddaughter':2, 'grandson':2, 'grandchild':2,
    'downstairs':2, 'upstairs':2,
    'catsup':3, 'disco':3,
    'telephone':1, 'hippopotamus':3, 'loudspeaker':3, 'lullaby':3,
    'typewriter':3, 'vice-president':3,
    'automobile':3, 'baby-sit':3, 'baby-sitter':3, 'crutch':3,
    'bamboo':3, 'brassiere':4,
    'aspirin':2, 'e-mail':2, 'freeway':2,
    'radar':3, 'magnet':3, 'tortoise':3, 'hydrogen':2,

    # === batch 5:基礎字降級 / 過級字降 ===
    'refer':2, 'reflect':2, 'recommend':2, 'theme':2, 'reward':2,
    'split':2, 'ban':2, 'alien':2, 'laser':2, 'logo':2,
    'mode':2, 'surf':2, 'scan':2, 'trim':2, 'flip':2,
    'recommendation':3, 'feedback':3, 'upgrade':3,
    'unlock':2, 'unpack':2, 'undo':2, 'unfold':3,
    'byte':3, 'clone':3, 'awesome':2, 'deadly':3,
    'shed':3, 'trait':3, 'script':3, 'swap':3, 'span':3,
    'mold':3, 'donate':3, 'donation':3, 'liter':2,
    'symptom':3, 'merge':3,
    'boost':3, 'breakdown':3, 'breakthrough':3,
    'epidemic':3, 'dome':3, 'feasible':3, 'defect':3,

    # === batch 6:衍生字 + 罕用動物 + 借詞食物 ===
    'movement':2, 'excitement':2, 'improvement':2, 'enjoyment':2,
    'kindness':2, 'darkness':2, 'weakness':2, 'sweetness':2,
    'squid':2, 'walrus':3, 'falcon':2, 'vulture':3, 'raven':3,
    'chinchilla':4, 'lemur':4, 'orangutan':3, 'baboon':3,
    'platypus':4, 'porcupine':4, 'armadillo':4,
    'mongoose':4, 'meerkat':4,
    'lasagna':3, 'croissant':3, 'jalapeno':4, 'quinoa':4,
    'fettuccine':4, 'mascarpone':4, 'prosciutto':4, 'vinaigrette':4,
    'vulnerable':3, 'vaccine':3, 'vibration':3,
    'variable':3, 'variation':3, 'vocal':3, 'veteran':3,
    'corroborate':4, 'exacerbate':4, 'exonerate':4,
    'juxtapose':4, 'disseminate':4, 'promulgate':4,
    'repudiate':4, 'reconnaissance':4, 'rheumatism':4,
    'obnoxious':4, 'precarious':4, 'barbarous':4,
    'venerate':4, 'plagiarize':4,
}

n = 0
not_found = []
for word, new_stage in FIXES.items():
    if word not in idx:
        not_found.append(word)
        continue
    old = idx[word].get('stage')
    if old == new_stage:
        continue
    idx[word]['stage'] = new_stage
    n += 1

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"已修: {n}")
if not_found: print(f"找不到 ({len(not_found)}): {not_found[:20]}")
