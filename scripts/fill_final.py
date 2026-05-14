"""最終批次:-ly 副詞 / -al 形容詞 / -y 形容詞剩餘真家族線"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB, 'r', encoding='utf-8') as f:
    data = json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

# -ly 副詞(超多真家族線)
LY = {
    'lonely':'lone','friendly':'friend','weekly':'week','monthly':'month',
    'yearly':'year','hourly':'hour','daily':'day','nightly':'night',
    'surely':'sure','frankly':'frank','partly':'part','entirely':'entire',
    'slightly':'slight','barely':'bare','precisely':'precise',
    'ultimately':'ultimate','similarly':'similar','additionally':'additional',
    'alternatively':'alternative','apparently':'apparent','evidently':'evident',
    'namely':'name','technically':'technical','utterly':'utter',
    'virtually':'virtual','plainly':'plain','swiftly':'swift','ideally':'ideal',
    'conversely':'converse','comparatively':'comparative','equally':'equal',
    'firstly':'first','secondly':'second','thirdly':'third','lastly':'last',
    'importantly':'important','significantly':'significant','chiefly':'chief',
    'subsequently':'subsequent','consequently':'consequent','greatly':'great',
    'mostly':'most','globally':'global','locally':'local','nationally':'national',
    'internationally':'international','politically':'political','socially':'social',
    'culturally':'cultural','economically':'economic','financially':'financial',
    'historically':'historical','legally':'legal','medically':'medical',
    'mentally':'mental','morally':'moral','professionally':'professional',
    'visually':'visual','vocally':'vocal','verbally':'verbal',
    'physically':'physical','emotionally':'emotional','spiritually':'spiritual',
    'mainly':'main','generally':'general','specifically':'specific',
    'individually':'individual','collectively':'collective','officially':'official',
    'positively':'positive','negatively':'negative','effectively':'effective',
    'efficiently':'efficient','practically':'practical','theoretically':'theoretical',
    'literally':'literal','figuratively':'figurative','seriously':'serious',
    'casually':'casual','privately':'private','publicly':'public',
    'directly':'direct','indirectly':'indirect','explicitly':'explicit',
    'implicitly':'implicit','formally':'formal','informally':'informal',
    'strictly':'strict','loosely':'loose','tightly':'tight','widely':'wide',
    'closely':'close','freely':'free','deeply':'deep','roughly':'rough',
    'smoothly':'smooth','warmly':'warm','coldly':'cold','strongly':'strong',
    'weakly':'weak','richly':'rich','poorly':'poor','shortly':'short',
    'longly':'long','tightly':'tight','briefly':'brief','widely':'wide',
    'truly':'true','fully':'full','hardly':'hard','merely':'mere',
    'fairly':'fair','firmly':'firm','politely':'polite','honestly':'honest',
    'kindly':'kind','badly':'bad','sadly':'sad','gladly':'glad','safely':'safe',
    'rudely':'rude','clearly':'clear','perfectly':'perfect','gently':'gentle',
    'simply':'simple','rarely':'rare','newly':'new','highly':'high',
    'lowly':'low','commonly':'common','gradually':'gradual',
    'occasionally':'occasional','extremely':'extreme','approximately':'approximate',
    'fortunately':'fortunate','unfortunately':'unfortunate','silently':'silent',
    'patiently':'patient','impatiently':'impatient','quickly':'quick','slowly':'slow',
    'loudly':'loud','softly':'soft','quietly':'quiet','happily':'happy',
    'angrily':'angry','easily':'easy','busily':'busy','noisily':'noisy',
    'hungrily':'hungry','really':'real','finally':'final','usually':'usual',
    'actually':'actual','totally':'total','naturally':'natural','normally':'normal',
    'especially':'especial','definitely':'definite','absolutely':'absolute',
    'completely':'complete','exactly':'exact','nearly':'near','recently':'recent',
    'currently':'current','eventually':'eventual','frequently':'frequent',
    'immediately':'immediate','originally':'original','particularly':'particular',
    'probably':'probable','suddenly':'sudden','lately':'late',
    'beautifully':'beautiful','wonderfully':'wonderful','helpfully':'helpful',
    'usefully':'useful','carefully':'careful','carelessly':'careless',
    'painfully':'painful','powerfully':'powerful','cheerfully':'cheerful',
    'hopefully':'hopeful','thoughtfully':'thoughtful','thankfully':'thankful',
    'awfully':'awful','obviously':'obvious','seriously':'serious',
    'curiously':'curious','famously':'famous','dangerously':'dangerous',
    'nervously':'nervous','generously':'generous','jealously':'jealous',
    'consciously':'conscious','anxiously':'anxious','furiously':'furious',
    'mysteriously':'mysterious','enormously':'enormous',
}

# -al 形容詞
AL = {
    'normal':'norm','arrival':'arrive','formal':'form','digital':'digit',
    'virtual':'virtue','original':'origin','sentimental':'sentiment',
    'temperamental':'temperament','proposal':'propose','betrayal':'betray',
    'withdrawal':'withdraw','recital':'recite','signal':'sign',
    'additional':'addition','educational':'education','survival':'survive',
    'approval':'approve','continual':'continue','conventional':'convention',
    'economical':'economic','natural':'nature','national':'nation',
    'central':'center','musical':'music','cultural':'culture',
    'medical':'medicine','historical':'history','logical':'logic',
    'magical':'magic','tropical':'tropic','environmental':'environment',
    'accidental':'accident','emotional':'emotion','traditional':'tradition',
    'professional':'profession','industrial':'industry','global':'globe',
    'political':'politics','seasonal':'season','personal':'person',
    'sexual':'sex','occasional':'occasion','sensational':'sensation',
    'fictional':'fiction','optional':'option','rental':'rent',
    'denial':'deny','refusal':'refuse','removal':'remove',
    'disposal':'dispose','rehearsal':'rehearse','survival':'survive',
    'arrival':'arrive','departure':'depart',
}

# -y 形容詞
Y = {
    'easy':'ease','funny':'fun','juicy':'juice','bakery':'bake',
    'delivery':'deliver','grocery':'grocer','recovery':'recover',
    'beefy':'beef','bulky':'bulk','classy':'class','foxy':'fox',
    'curly':'curl','bumpy':'bump','lumpy':'lump','grumpy':'grump',
    'jumpy':'jump','rusty':'rust','crispy':'crisp','crusty':'crust',
    'pricey':'price','fruity':'fruit','minty':'mint','chewy':'chew',
    'stinky':'stink','itchy':'itch','thorny':'thorn','woody':'wood',
    'grassy':'grass','soupy':'soup','pearly':'pearl','creepy':'creep',
    'sneaky':'sneak','peachy':'peach','cherry':'cherry',
    'speedy':'speed','greedy':'greed','needy':'need','risky':'risk',
    'sleepy':'sleep','smelly':'smell','starry':'star','fiery':'fire',
    'sugary':'sugar','milky':'milk','spotty':'spot','dotty':'dot',
    'rosy':'rose','stormy':'storm','breezy':'breeze','misty':'mist',
    'frosty':'frost','gloomy':'gloom','dirty':'dirt','guilty':'guilt',
    'fishy':'fish','wealthy':'wealth','healthy':'health','meaty':'meat',
    'leafy':'leaf',
}

# 模板
def note(suf, base, word):
    if suf == 'ly':
        return f'副詞版本(+ly,從 {base} 來)'
    if suf == 'al':
        return f'形容詞版本(+al,從 {base} 來)'
    if suf == 'y':
        return f'形容詞版本(+y,描述 {base} 特性)'
    return ''

applied = 0
skipped = 0
for d, suf in [(LY,'ly'), (AL,'al'), (Y,'y')]:
    for word, base in d.items():
        if word not in idx:
            skipped += 1; continue
        if 'base' in idx[word]:
            skipped += 1; continue
        if base not in idx:
            skipped += 1; continue
        idx[word]['base'] = base
        idx[word]['family-note'] = note(suf, base, word)
        applied += 1

with open(VOCAB, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"applied: {applied}")
print(f"skipped: {skipped}")
print(f"total with base: {sum(1 for w in words if 'base' in w)}")
