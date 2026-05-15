"""套用 pos-consistency 修正 — 詞性一致 / 形容詞「的」/ 真翻錯"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

FIXES = {
    # === batch 0:天氣 / 情緒 形容詞 ===
    'rainy':'多雨的、下雨的', 'snowy':'多雪的、下雪的',
    'windy':'有風的、多風的', 'foggy':'多霧的、起霧的',
    'scared':'害怕的', 'afraid':'害怕的、擔心的', 'worried':'擔心的',
    'relaxed':'放鬆的', 'jealous':'嫉妒的', 'grateful':'感激的、感謝的',
    'fond':'喜愛的', 'recent':'最近的', 'instant':'立即的、瞬間',

    # === batch 1:情緒 / 一般形容詞 ===
    'depressed':'憂鬱的', 'anxious':'焦慮的', 'peaceful':'平靜的',
    'ashamed':'羞愧的', 'guilty':'愧疚的', 'frustrated':'挫敗的',
    'disappointed':'失望的', 'delighted':'開心的', 'thrilled':'興奮的',
    'miserable':'悲慘的', 'gloomy':'陰鬱的', 'heartbroken':'心碎的',
    'nostalgic':'懷舊的', 'curious':'好奇的', 'eager':'渴望的、急切的',
    'enthusiastic':'熱情的', 'passionate':'熱情的', 'moved':'感動的',
    'smart':'聰明的', 'dumb':'笨的', 'brilliant':'傑出的',
    'stupid':'愚蠢的', 'clever':'靈巧的、聰明的', 'wise':'明智的',
    'foolish':'愚蠢的、傻的', 'intelligent':'聰明的',
    'complex':'複雜的', 'complicated':'複雜的',
    'modern':'現代的', 'ancient':'古老的', 'traditional':'傳統的',
    'common':'常見的', 'rare':'罕見的', 'unique':'獨特的',
    'normal':'正常的', 'weird':'奇怪的', 'strange':'奇怪的',
    'ordinary':'普通的', 'perfect':'完美的',
    'sharp':'鋒利的', 'smooth':'光滑的', 'rough':'粗糙的',
    'juicy':'多汁的', 'crispy':'酥脆的', 'tough':'堅韌的',
    'domestic':'國內的', 'international':'國際的',
    'digital':'數位的', 'virtual':'虛擬的',
    'horizontal':'水平的', 'vertical':'垂直的',
    'diagonal':'對角的、斜的', 'parallel':'平行的', 'perpendicular':'垂直的',
    'frankly':'坦白地、坦白說', 'primarily':'主要地', 'mainly':'主要地',
    'ultimately':'最終地、最後', 'savory':'鹹的、鹹香的',
    'noteworthy':'值得注意的',

    # === batch 2:外貌 / 性格 形容詞(大批量) ===
    'slim':'苗條的', 'slender':'纖細的', 'plump':'豐滿的',
    'lean':'精瘦的、傾斜', 'muscular':'肌肉發達的',
    'beefy':'健壯的', 'bulky':'龐大的', 'scrawny':'瘦小的',
    'gaunt':'憔悴的', 'handsome':'英俊的', 'gorgeous':'美艷的',
    'stunning':'驚豔的', 'charming':'迷人的', 'elegant':'優雅的',
    'graceful':'優雅的', 'dapper':'瀟灑的', 'dashing':'瀟灑的',
    'foxy':'性感的', 'sexy':'性感的', 'average':'普通的',
    'bald':'禿頭的', 'tanned':'曬黑的', 'sunburned':'曬傷的',
    'hairy':'多毛的', 'curly':'捲的', 'wavy':'波浪狀的',
    'frizzy':'毛躁的', 'braided':'編成辮子的',
    'mature':'成熟的', 'youthful':'年輕的', 'aged':'年長的',
    'wrinkly':'皺巴巴的', 'smiley':'愛笑的',
    'neat':'整潔的', 'scruffy':'邋遢的', 'shabby':'破舊的',
    'untidy':'凌亂的', 'polished':'精緻的', 'refined':'優雅的',
    'petite':'嬌小的', 'curvy':'曲線玲瓏的',
    'rugged':'粗獷的', 'disheveled':'凌亂的',
    'hardworking':'勤奮的', 'diligent':'勤勉的',
    'determined':'堅定的', 'reserved':'內斂的',
    'outgoing':'外向的', 'introverted':'內向的',
    'extroverted':'外向的', 'distant':'冷淡的', 'aloof':'高傲的',
    'sincere':'真誠的', 'candid':'坦率的', 'blunt':'直白的',
    'diplomatic':'圓滑的', 'loyal':'忠誠的', 'faithful':'忠實的',
    'reliable':'可靠的', 'optimistic':'樂觀的', 'pessimistic':'悲觀的',
    'idealistic':'理想主義的', 'innovative':'創新的',
    'arrogant':'自大的', 'humble':'謙虛的', 'modest':'謙虛的',
    'conceited':'自負的', 'vain':'虛榮的', 'pretentious':'做作的',
    'generous':'慷慨的', 'stingy':'小氣的',
    'selfish':'自私的', 'selfless':'無私的',
    'sensitive':'敏感的', 'romantic':'浪漫的',
    'practical':'務實的', 'rational':'理性的',
    'impulsive':'衝動的', 'reckless':'魯莽的', 'cautious':'謹慎的',
    'naive':'天真的', 'witty':'機智的', 'sarcastic':'愛諷刺的',
    'humorous':'幽默的', 'daring':'大膽的',

    # === batch 3:Mormon / Sikh / largely / immoral ===
    'immoral':'不道德的',
    'mormon':'摩門教徒、摩門教的',
    'sikh':'錫克教徒',
    'largely':'大多、大致上',

    # === batch 4:小修正 ===
    'ease':'輕鬆、緩和', 'quick':'快的、快速的',
    'badly':'嚴重地、糟糕地',
    'complete':'完成、完整的',
    'delightful':'令人愉快的、令人高興的',
    'leisurely':'從容不迫地、悠閒地',

    # === batch 5:真翻錯 + 連寫不通 ===
    'astonish':'使震驚、使吃驚',
    'meditate':'沉思、冥想',
    'morale':'士氣',
    'genetic':'遺傳的、基因的',
    'controversial':'有爭議的、引起爭論的',
    'plight':'困境、苦境',
    'torment':'折磨、使痛苦',
    'torture':'折磨、拷打',
    'fluid':'流體、液體',
    'offering':'供品、祭品、提供物',
    'nourishment':'營養、養分',
    'resolute':'堅決的、堅定的',
    'pollutant':'污染物',
    'barbarian':'野蠻人、野蠻的',
    'dual':'雙重的、二元的',
    'crook':'騙子、彎處',
    'presidency':'總統職位、總統任期',
    'presidential':'總統的',
    'clone':'複製品、複製人',
    'abstraction':'抽象概念',

    # === batch 6:殘留 ===
    'validity':'有效性、正當性',
    'formality':'形式、正式手續',
    'subtlety':'微妙之處',
    'relevance':'相關性、關聯',
    'dominance':'主導地位、優勢',
    'contagion':'傳染、傳染病',
    'languish':'變憔悴、凋零',
    'extremely':'極度地、非常',
}

n = 0
not_found = []
for word, new_mean in FIXES.items():
    if word not in idx:
        not_found.append(word)
        continue
    old = idx[word].get('mean','')
    if old == new_mean:
        continue
    idx[word]['mean'] = new_mean
    n += 1

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"已修: {n}")
if not_found: print(f"找不到 ({len(not_found)}): {not_found[:20]}")
