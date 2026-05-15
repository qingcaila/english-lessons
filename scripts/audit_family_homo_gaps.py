"""深度審查家族線與易混提示的覆蓋率,找漏網的"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']
idx = {w['word']: w for w in words}
word_set = set(idx.keys())

# =============================================================================
# 1) 家族線 — 常見不規則動詞(過去式 / 過去分詞)清單
# =============================================================================
KNOWN_IRREGULAR = {
    # 基本款
    'awoke':'awake', 'awoken':'awake', 'bore':'bear', 'borne':'bear',
    'beat':'beat', 'beaten':'beat', 'become':'become', 'become':'become',
    'begun':'begin', 'bent':'bend', 'bet':'bet', 'bound':'bind',
    'bitten':'bite', 'bit':'bite', 'bled':'bleed',
    'blown':'blow', 'broadcast':'broadcast', 'built':'build', 'burnt':'burn',
    'burst':'burst', 'cast':'cast', 'caught':'catch', 'chosen':'choose',
    'clung':'cling', 'cost':'cost', 'crept':'creep', 'cut':'cut',
    'dealt':'deal', 'dug':'dig', 'dived':'dive', 'drawn':'draw',
    'dreamt':'dream', 'driven':'drive', 'drunk':'drink', 'eaten':'eat',
    'fallen':'fall', 'fed':'feed', 'felt':'feel', 'fought':'fight',
    'flown':'fly', 'forbidden':'forbid', 'forecast':'forecast',
    'forgot':'forget', 'forgotten':'forget', 'forgave':'forgive',
    'forgiven':'forgive', 'frozen':'freeze', 'gotten':'get',
    'given':'give', 'gone':'go', 'ground':'grind', 'grown':'grow',
    'hung':'hang', 'heard':'hear', 'hidden':'hide', 'hid':'hide',
    'held':'hold', 'hurt':'hurt', 'kept':'keep', 'knelt':'kneel',
    'knew':'know', 'known':'know', 'laid':'lay', 'led':'lead',
    'lent':'lend', 'let':'let', 'lay':'lie', 'lain':'lie',
    'lit':'light', 'lost':'lose', 'made':'make', 'meant':'mean',
    'met':'meet', 'paid':'pay', 'put':'put', 'read':'read',
    'ridden':'ride', 'rode':'ride', 'rang':'ring', 'rung':'ring',
    'risen':'rise', 'rose':'rise', 'run':'run', 'said':'say',
    'sold':'sell', 'sent':'send', 'shaken':'shake', 'shook':'shake',
    'shone':'shine', 'shot':'shoot', 'shown':'show', 'shrunk':'shrink',
    'shrank':'shrink', 'shut':'shut', 'sung':'sing', 'sang':'sing',
    'sunk':'sink', 'sank':'sink', 'sat':'sit', 'slept':'sleep',
    'slid':'slide', 'sown':'sow', 'spoken':'speak', 'spoke':'speak',
    'sped':'speed', 'spelt':'spell', 'spent':'spend', 'spilt':'spill',
    'spat':'spit', 'split':'split', 'spread':'spread', 'sprang':'spring',
    'sprung':'spring', 'stood':'stand', 'stolen':'steal', 'stole':'steal',
    'stuck':'stick', 'stung':'sting', 'struck':'strike', 'sworn':'swear',
    'swore':'swear', 'swept':'sweep', 'swum':'swim', 'swam':'swim',
    'swung':'swing', 'taken':'take', 'taught':'teach', 'torn':'tear',
    'tore':'tear', 'told':'tell', 'thought':'think', 'thrown':'throw',
    'threw':'throw', 'thrust':'thrust', 'trodden':'tread', 'understood':'understand',
    'undertaken':'undertake', 'undid':'undo', 'undone':'undo',
    'upset':'upset', 'woken':'wake', 'woke':'wake', 'worn':'wear',
    'wept':'weep', 'won':'win', 'wound':'wind', 'wrung':'wring',
    'written':'write', 'wrote':'write', 'arose':'arise', 'arisen':'arise',
    'foresaw':'foresee', 'foreseen':'foresee', 'foretold':'foretell',
}

missing_irr = []
for past, base in KNOWN_IRREGULAR.items():
    if past in idx and base in idx and 'base' not in idx[past]:
        missing_irr.append((past, base))

# =============================================================================
# 2) 常見同音/易混字組合(完整版)
# =============================================================================
HOMOPHONE_PAIRS = [
    # 高頻陷阱
    ('there','their','they\'re'),
    ('to','too','two'),
    ('your','you\'re'),
    ('its','it\'s'),
    ('then','than'),
    ('lose','loose'),
    ('whose','who\'s'),
    ('weather','whether'),
    ('affect','effect'),
    ('accept','except'),
    ('advice','advise'),
    ('principal','principle'),
    ('stationary','stationery'),
    ('quite','quiet'),
    ('desert','dessert'),
    ('breath','breathe'),
    ('cloth','clothe'),
    ('bath','bathe'),
    # 同音
    ('see','sea'),
    ('hear','here'),
    ('hour','our'),
    ('know','no'),
    ('night','knight'),
    ('write','right'),
    ('one','won'),
    ('two','too','to'),
    ('eye','I'),
    ('flower','flour'),
    ('mail','male'),
    ('tail','tale'),
    ('meat','meet'),
    ('peace','piece'),
    ('weak','week'),
    ('wait','weight'),
    ('blue','blew'),
    ('new','knew'),
    ('road','rode'),
    ('sail','sale'),
    ('break','brake'),
    ('beat','beet'),
    ('bear','bare'),
    ('cell','sell'),
    ('whole','hole'),
    ('plane','plain'),
    ('pair','pear'),
    ('made','maid'),
    ('threw','through'),
    ('flew','flu'),
    ('bored','board'),
    ('be','bee'),
    ('eight','ate'),
    ('hare','hair'),
    ('heel','heal'),
    ('hi','high'),
    ('it','it\'s'),
    ('him','hymn'),
    ('miner','minor'),
    ('mist','missed'),
    ('moose','mousse'),
    ('nose','knows'),
    ('not','knot'),
    ('oar','or','ore'),
    ('peek','peak'),
    ('plain','plane'),
    ('pray','prey'),
    ('rain','reign','rein'),
    ('raise','rays','raze'),
    ('rap','wrap'),
    ('red','read'),
    ('role','roll'),
    ('rose','rows'),
    ('sea','see'),
    ('seam','seem'),
    ('seen','scene'),
    ('sew','so','sow'),
    ('shoe','shoo'),
    ('side','sighed'),
    ('soar','sore'),
    ('some','sum'),
    ('son','sun'),
    ('stair','stare'),
    ('steal','steel'),
    ('sweet','suite'),
    ('tea','tee'),
    ('toe','tow'),
    ('vain','vein','vane'),
    ('wear','where'),
    ('which','witch'),
    ('whine','wine'),
    ('would','wood'),
    # 易混
    ('lay','lie'),
    ('rise','raise'),
    ('sit','set'),
    ('sit','seat'),
    ('lend','borrow'),
    ('teach','learn'),
    ('bring','take'),
    ('say','tell'),
    ('say','speak'),
    ('hope','wish'),
    ('few','little'),
    ('many','much'),
    ('among','between'),
    ('beside','besides'),
    ('used to','use to'),
    ('further','farther'),
    ('alone','lonely'),
    ('ago','before'),
    ('almost','nearly'),
    ('imply','infer'),
    ('comprise','compose'),
    ('elicit','illicit'),
    ('eminent','imminent'),
    ('compliment','complement'),
    ('council','counsel'),
    ('emigrate','immigrate'),
    ('precede','proceed'),
    ('disinterested','uninterested'),
    ('flaunt','flout'),
    ('flammable','inflammable'),
    ('historic','historical'),
    ('economic','economical'),
    ('classic','classical'),
    ('continuous','continual'),
    ('beside','besides'),
    ('amount','number'),
    ('lose','loss'),
    ('rise','arise'),
]

# 找哪些字「在 vocab 中存在,但沒標 homophone-note」
missing_homo = []
for pair in HOMOPHONE_PAIRS:
    in_vocab = [w for w in pair if w in word_set]
    if len(in_vocab) < 2:
        continue
    no_note = [w for w in in_vocab if 'homophone-note' not in idx[w]]
    if no_note:
        missing_homo.append((pair, in_vocab, no_note))

# =============================================================================
# 3) 已知衍生詞型但漏 base 的(用更廣字典)
# =============================================================================
# 簡單只列高價值的:常見職業/形容詞/副詞
KNOWN_DERIVATIVE = {
    # -er 職業
    'singer':'sing','dancer':'dance','runner':'run','swimmer':'swim',
    'teacher':'teach','writer':'write','reader':'read','speaker':'speak',
    'baker':'bake','farmer':'farm','worker':'work','driver':'drive',
    'rider':'ride','helper':'help','leader':'lead','manager':'manage',
    'owner':'own','painter':'paint','designer':'design','engineer':'engine',
    'cleaner':'clean','waiter':'wait','reporter':'report','observer':'observe',
    'researcher':'research','traveler':'travel','employer':'employ',
    'gardener':'garden','sailor':'sail','actor':'act',
    'director':'direct','editor':'edit','professor':'profess',
    'inventor':'invent','investor':'invest','visitor':'visit',
    # -ly 副詞
    'quickly':'quick','slowly':'slow','happily':'happy','sadly':'sad',
    'carefully':'careful','badly':'bad','easily':'easy','suddenly':'sudden',
    'really':'real','finally':'final','usually':'usual','clearly':'clear',
    # -tion 名詞
    'creation':'create','discussion':'discuss','reservation':'reserve',
    'decision':'decide','education':'educate','translation':'translate',
    'production':'produce','reduction':'reduce','protection':'protect',
    # -ment 名詞
    'agreement':'agree','movement':'move','statement':'state',
    'government':'govern','development':'develop','treatment':'treat',
    'announcement':'announce','arrangement':'arrange',
    # -able / -ible
    'comfortable':'comfort','acceptable':'accept','enjoyable':'enjoy',
    'breakable':'break','washable':'wash','readable':'read',
    'flexible':'flex','sensible':'sense','visible':'vision',
    # -ness
    'happiness':'happy','kindness':'kind','darkness':'dark','sadness':'sad',
    'weakness':'weak','sickness':'sick','illness':'ill',
    # -ful / -less
    'helpful':'help','useful':'use','careful':'care','peaceful':'peace',
    'beautiful':'beauty','wonderful':'wonder','painful':'pain',
    'powerful':'power','colorful':'color','cheerful':'cheer',
    'useless':'use','careless':'care','hopeless':'hope','helpless':'help',
    'endless':'end','homeless':'home','restless':'rest',
}

missing_deriv = []
for d, base in KNOWN_DERIVATIVE.items():
    if d in idx and base in idx and 'base' not in idx[d]:
        missing_deriv.append((d, base))

# =============================================================================
# 報告
# =============================================================================
print("="*60)
print("家族線(base)覆蓋率審查")
print("="*60)
total = len(words)
with_base = sum(1 for w in words if 'base' in w)
print(f"總字數: {total}")
print(f"已標 base: {with_base} ({with_base/total*100:.1f}%)")
print()
print(f"=== 1) 不規則動詞遺漏 base: {len(missing_irr)} ===")
for past, base in missing_irr[:50]:
    print(f"  {past:20s} ← {base}")
print()
print(f"=== 2) 已知衍生詞遺漏 base: {len(missing_deriv)} ===")
for d, base in missing_deriv[:50]:
    print(f"  {d:25s} ← {base}")
print()
print("="*60)
print("易混提示(homophone-note)覆蓋率審查")
print("="*60)
with_homo = sum(1 for w in words if 'homophone-note' in w)
print(f"已標 homophone-note: {with_homo}")
print()
print(f"=== 3) 同音/易混組合遺漏: {len(missing_homo)} 組 ===")
for pair, in_vocab, no_note in missing_homo[:60]:
    print(f"  {'/'.join(pair):30s}  vocab中: {in_vocab}  漏標: {no_note}")
