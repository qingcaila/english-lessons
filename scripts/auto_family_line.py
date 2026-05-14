"""
自動套用家族線到所有衍生字候選。
策略:
  - 高信心字尾 → 套通用 family-note 模板
  - -er/-ing/-ed/-or → 需 stem 是動詞(查白名單)或常見假陽性黑名單外
  - 危險字尾 -y/-al/-ly/-s → 嚴格黑名單
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
CAND = os.path.normpath(os.path.join(HERE, 'candidates.json'))

with open(VOCAB, 'r', encoding='utf-8') as f:
    data = json.load(f)
with open(CAND, 'r', encoding='utf-8') as f:
    cands = json.load(f)

words = data['words']
idx = {w['word']: w for w in words}

# ========= 黑名單:不是真家族線(stem 跟 word 意義無關)=========
BLACKLIST = {
    # -er 假陽性(stem 不是動詞 / 意義無關)
    'mother','brother','sister','water','paper','weather','summer','winter','fever',
    'never','ever','other','after','over','under','dinner','finger','river','silver',
    'member','number','center','corner','order','letter','matter','butter','better',
    'gather','rather','either','neither','wonder','thunder','spider','tiger','liver',
    'cover','cucumber','cancer','danger','dangerous','soldier','prefer','ginger',
    'shoulder','quarter','hammer','toilet','laughter','daughter','flower','shower',
    'beer','dear','near','clear','wear','tear','year','here','there','where',
    'sweater','engineer','fiber','timber','beaver','glacier','barrier','passenger',
    'character','manager_x','consumer','customer','prisoner','volunteer',
    'composer','painter_x','seed','feet','meet',
    # -y 假陽性
    'family','very','every','many','only','jelly','daddy','mommy','baby','lady',
    'body','holy','copy','july','navy','duty','jury','july','study','story',
    'army','envy','jury','party','enemy','agency','energy','journey','memory','sorry',
    'happy','heavy','lucky','funny','easy','busy','crazy','dirty','empty','hungry',
    'thirsty','silly','pretty','tiny','noisy','sunny','rainy','cloudy','windy',
    'angry','smelly','salty','tasty','sticky','crispy','spicy','bloody',
    # -al 假陽性
    'animal','metal','total','real','meal','seal','deal','goal','equal','final',
    'normal','signal','medal','dial','feel','heel','wheel','steel','school',
    'oval','cereal','original','royal','rural','formal','plural',
    'central','digital','federal','liberal','mineral','musical','national',
    'natural','optical','personal','physical','political','practical','tropical',
    'universal','vertical','classical','critical','electrical','financial',
    'general','global','industrial','informal','internal','external','illegal',
    'legal','local','loyal','mental','moral','nasal','naval','neural','social',
    'spatial','spiritual','technical','typical','verbal','virtual','vital',
    'visual','vocal','crystal','herbal','manual','radical','vertical',
    # -ly 假陽性(不是 adj+ly)
    'family','only','reply','july','rely','apply','imply','supply','holy',
    'fly','sly','ally','rally','silly','jelly',
    # -s 假陽性
    'is','was','has','does','goes',
    # -ing 假陽性
    'evening','thing','king','wing','ring','sing','bring','spring','string',
    'morning','ceiling',
    # -ed 假陽性
    'red','bed','bread','head','dead','feed','need','seed','speed','weed',
    'breed','bleed',
    # -or 假陽性
    'door','floor','poor','color','flavor','honor','humor','mayor','minor',
    'major','tutor','liquor','rumor','for','our','your','their',
    # -able / -ible 假陽性
    'cable','table','stable','liable','viable','mobile','bible','sensible_x',
    # -ous 假陽性
    'previous_x','generous_x',
    # -al, -er 拼錯誤識別
    'forest','best','test','rest','west','nest','quest','priest','guest',
    'modest','honest','protest','contest','arrest','digest','suggest',
    # 不是 -y 而是名詞本身
    'sky','toy','boy','joy','key','play','day','way','say',
    'guy','buy','try','dry','fry','cry','my','by',
    # -er 但 stem 不對(meat≠?)
    'meter','butler','butler',
    # 過去分詞,base 應該不一樣
    'thing','having','being',
    # 介系詞/連接詞家族外
    'unless','useless_x',
}

# ========= -er / -ed / -ing / -or 需要 stem 是動詞的字 =========
# 已知是動詞的 stem(白名單,提高 precision)
VERB_STEMS = {
    'teach','farm','drive','sing','bake','work','wait','paint','design','read',
    'write','speak','play','run','swim','dance','help','lead','manage','own',
    'clean','compute','charge','erase','mark','heat','hang','time','rule',
    'fold','dry','print','print','build','meet','feel','end','begin','open',
    'close','climb','jump','kick','push','pull','catch','throw','reach','rise',
    'fall','stand','sit','walk','talk','watch','want','listen','look','use',
    'love','like','move','live','call','ask','answer','show','give','take',
    'make','come','go','do','see','say','tell','think','know','find','get',
    'have','put','set','let','cut','hit','fit','fix','mix','win','spin',
    'shoot','sleep','eat','drink','cook','wash','dry','clean','iron','sweep',
    'wipe','dust','mop','play','sing','dance','draw','paint','color','cut',
    'glue','tape','wrap','tie','knot','bend','fold','press','stretch','shake',
    'wave','clap','point','grab','hold','catch','throw','kick','pass','dribble',
    'shoot','score','goal','win','lose','tie','beat','fight','hunt','race',
    'jog','train','exercise','stretch','warm','cool','breathe','sweat','sneeze',
    'cough','yawn','laugh','smile','cry','sob','sigh','scream','shout','whisper',
    'mumble','complain','blame','praise','thank','apologize','greet','welcome',
    'farewell','goodbye','accept','reject','agree','disagree','argue','discuss',
    'debate','negotiate','vote','elect','choose','select','pick','prefer','decide',
    'plan','organize','arrange','prepare','cook','bake','grill','fry','boil',
    'steam','toast','heat','warm','cool','freeze','thaw','melt','burn','grow',
    'plant','water','feed','raise','breed','farm','harvest','pick','gather',
    'collect','sort','organize','store','keep','save','spend','waste','share',
    'lend','borrow','owe','pay','buy','sell','trade','exchange','give','receive',
    'send','deliver','mail','call','phone','text','email','write','read','book',
    'sign','stamp','print','scan','copy','paste','cut','delete','edit','save',
    'upload','download','search','browse','click','tap','swipe','scroll','type',
    'log','exit','enter','start','stop','pause','resume','restart','update',
    'install','remove','accept','except','allow','permit','forbid','prevent',
    'protect','defend','attack','invade','escape','flee','rescue','save','help',
    'serve','feed','heal','cure','treat','operate','prescribe','diagnose','test',
    'examine','check','study','learn','teach','train','coach','mentor','tutor',
    'lecture','speak','present','explain','describe','define','translate','interpret',
    'react','respond','reply','answer','ask','question','inquire','wonder',
    'doubt','believe','trust','suspect','accuse','arrest','jail','release','free',
    'fine','punish','warn','threaten','attack','defend','protect','guard','watch',
    'observe','spy','follow','chase','lead','guide','direct','manage','supervise',
    'control','operate','run','own','rent','lease','buy','sell','trade','invest',
    'borrow','lend','save','spend','earn','gain','lose','win','succeed','fail',
    'try','attempt','strive','accomplish','achieve','complete','finish','start',
    'begin','continue','stop','quit','give','retire','resign',
    # 衍生詞根
    'act','accept','adapt','adopt','affect','agree','allow','amaze','amuse','annoy',
    'announce','appear','approve','argue','arrange','arrive','attract','assemble',
    'assist','assume','attach','attend','attract','avoid','bore','calculate','call',
    'care','celebrate','change','collect','communicate','complete','consider',
    'consume','contain','continue','control','create','define','demand','depend',
    'describe','design','destroy','develop','differ','discover','discuss','divide',
    'doubt','educate','elect','employ','encourage','enjoy','enter','establish',
    'examine','exist','expect','explain','explore','express','extend','fail',
    'finance','flow','follow','form','found','frighten','generate','govern','grade',
    'graduate','identify','imagine','impress','improve','include','increase',
    'indicate','inform','injure','insert','inspect','inspire','install','introduce',
    'invent','invest','invite','involve','isolate','judge','launch','locate','manage',
    'manufacture','measure','memorize','mention','obey','observe','obtain','occupy',
    'offer','operate','oppose','organize','perform','permit','persuade','plan',
    'pollute','possess','practice','predict','prefer','prepare','present','prevent',
    'process','produce','progress','project','promise','promote','propose','protect',
    'provide','publish','punish','purchase','quote','realize','recognize','recommend',
    'record','reduce','refer','refuse','regret','reject','relate','release','rely',
    'remember','remove','repeat','replace','reply','represent','require','reserve',
    'resist','respect','respond','rest','result','retire','return','reveal','revise',
    'reward','satisfy','save','search','select','separate','settle','solve','sort',
    'study','succeed','suffer','suggest','supply','support','suppose','surprise',
    'survive','suspect','swear','tease','tend','threaten','train','transfer',
    'transform','translate','transport','travel','treat','trust','try','turn',
    'understand','use','vary','wander','warn','weigh','wonder','wrap','disappoint',
    'pay','say','obey','play','enjoy','employ','annoy','destroy','spray',
}

# ========= family-note 模板 =========
def make_note(suf, stem, word):
    if suf == 'able':
        return f'「可以…的」版本(+able 形容詞,可以被 {stem})'
    if suf == 'ible':
        return f'「可以…的」版本(+ible 形容詞,可以被 {stem})'
    if suf in ('tion','sion','ation','ition','ution'):
        return f'這個動作的「結果/事物」(+{suf} 名詞)'
    if suf == 'ment':
        return f'這個動作的「結果/事物」(+ment 名詞)'
    if suf == 'ness':
        return f'「…的性質」(+ness 把形容詞變名詞)'
    if suf == 'iness':
        return f'「…的性質」(y 變 i + ness)'
    if suf == 'ful':
        return f'「充滿…的」(+ful 形容詞)'
    if suf == 'less':
        return f'「沒…的」(+less 形容詞)'
    if suf == 'ous':
        return f'「有…的」(+ous 形容詞)'
    if suf == 'ive':
        return f'「會…的」(+ive 形容詞)'
    if suf == 'ly':
        return f'副詞版本(+ly 把形容詞變副詞)'
    if suf == 'al':
        return f'形容詞版本(+al)'
    if suf == 'ize' or suf == 'ise':
        return f'動詞版本(+{suf} 把名詞變動詞)'
    if suf == 'er':
        return f'做這件事的人/工具(+er)'
    if suf == 'or':
        return f'做這件事的人(+or)'
    if suf == 'ed':
        return f'已經…過的版本(過去式,+ed)'
    if suf == 'ing':
        return f'正在…的版本(進行式,+ing)'
    if suf == 'est':
        return f'「最…」的版本(最高級,+est)'
    if suf == 'ier':
        return f'「更…」的版本(比較級,y 變 i + er)'
    if suf == 'iest':
        return f'「最…」的版本(最高級,y 變 i + est)'
    if suf == 'ies':
        return f'「很多個」的版本(複數,y 變 ies)'
    if suf == 'y':
        return f'形容詞版本(+y,描述帶有 {stem} 特性的)'
    if suf == 's':
        return f'「很多個」的版本(複數,+s)'
    return f'家族字(+{suf})'

# ========= 套用 =========
CONFIDENT_SUFFIXES = {'able','ible','tion','sion','ation','ition','ution',
                      'ment','ness','iness','ful','less','ous','ive',
                      'ize','ise','est','ier','iest','ies'}
NEED_VERB_STEM = {'er','or','ed','ing'}
RISKY = {'y','al','ly','s'}

applied = 0
skipped_bl = 0
skipped_dup = 0
skipped_verbcheck = 0

for c in cands:
    word = c['word']
    stem = c['stem']
    suf = c['suf']
    if word in BLACKLIST:
        skipped_bl += 1
        continue
    if word not in idx:
        continue
    if 'base' in idx[word]:
        skipped_dup += 1
        continue
    if suf in NEED_VERB_STEM:
        if stem not in VERB_STEMS:
            skipped_verbcheck += 1
            continue
    if suf in RISKY:
        # 嚴格白名單模式:只處理清楚的 -ly / -y / -s / -al
        if suf == 'ly':
            # 形容詞 + ly → 副詞,需 stem 看起來是形容詞
            ADJ_HINT = {'slow','quick','easy','quiet','loud','soft','hard','fast','high','low',
                        'kind','nice','sad','happy','angry','careful','careless','helpful',
                        'painful','useful','beautiful','wonderful','final','clear','bright',
                        'dark','warm','cold','heavy','light','strong','weak','rich','poor',
                        'safe','dangerous','exact','perfect','sudden','recent','usual',
                        'normal','main','total','complete','direct','correct','wrong',
                        'true','false','real','simple','probable','possible','certain',
                        'special','general','natural','social','national','typical','obvious',
                        'absolute','relative','frequent','occasional','immediate','eventual',
                        'gradual','quick','rapid','smooth','rough','firm','tight','loose',
                        'free','open','close','wide','narrow','deep','shallow','full','empty',
                        'thick','thin','wet','dry','clean','dirty','fresh','stale','new','old',
                        'young','active','passive','positive','negative','formal','informal',
                        'public','private','personal','professional','political','economic',
                        'historical','mainly','originally','seriously','simply','clearly',
                        'extreme','rare','common','specific','approximate','exact','strict',
                        'gentle','rude','polite','honest','silent','noisy','calm','nervous',
                        'serious','silly','foolish','wise','clever','stupid','smart','dumb',
                        'brave','cowardly','generous','greedy','selfish','lazy','hard',
                        'careful','careless','thoughtful','thoughtless','mindful','mindless'}
            if stem not in ADJ_HINT:
                skipped_verbcheck += 1
                continue
        elif suf == 'y':
            # 名詞 + y → 形容詞:rain→rainy,sun→sunny
            NOUN_HINT = {'rain','sun','cloud','wind','snow','fog','storm','dust','dirt',
                         'mud','rock','stone','sand','grass','smoke','fire','ice','salt',
                         'sugar','milk','soup','curl','wave','spot','dot','rose','health',
                         'wealth','noise','fun','luck','sleep','speed','greed','need',
                         'risk','shine','sleep','smell','taste','meat','bone','skin','hair',
                         'fur','feather','spike','thorn','sticky'}
            if stem not in NOUN_HINT:
                skipped_verbcheck += 1
                continue
        elif suf == 's':
            # 複數,只給明顯名詞 stem 加
            # 大多數已存在 stem 是名詞時就 ok。但太多假陽性。跳過。
            skipped_verbcheck += 1
            continue
        elif suf == 'al':
            # 名詞 + al → 形容詞:nation→national, music→musical
            NOUN_HINT_AL = {'nation','music','culture','origin','region','medicine','center',
                            'tradition','emotion','profession','industry','agriculture',
                            'environment','accident','center','globe','politic','politics',
                            'season','person','nature','history','geography','science',
                            'logic','magic','poetry','art','race','sex','gender'}
            if stem not in NOUN_HINT_AL:
                skipped_verbcheck += 1
                continue
    # 套用
    idx[word]['base'] = stem
    idx[word]['family-note'] = make_note(suf, stem, word)
    applied += 1

with open(VOCAB, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"已套用:         {applied}")
print(f"略過(黑名單):   {skipped_bl}")
print(f"略過(已有 base):{skipped_dup}")
print(f"略過(動詞檢查): {skipped_verbcheck}")
print(f"總字數:         {len(words)}")
print(f"有 base:        {sum(1 for w in words if 'base' in w)}")
