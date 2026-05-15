"""套用 7 個 agent 找到的 emoji 修正(高信心 + 真誤導的才套)"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'vocab.json'))
with open(VOCAB, 'r', encoding='utf-8') as f: data = json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

# 過濾原則:只套「明顯真錯」+「有具體更好替代」
# 跳過:純抽象概念、字義邊緣、agent 自己標 "OK 保留"
FIXES = {
    # ===== batch 0 =====
    'belt':'👖','table':'🪑','oven':'♨️','tray':'🥡','sand':'🏖️',
    'by':'↔️','from':'⬅️','over':'⏫','front':'👆','back':'🔙','far':'🛣️',
    'drive':'🚗','finish':'🏁','throw':'🤾','pull':'🫳','come':'🫴',
    'finger':'👆','head':'👤','skin':'🫆','throat':'🗣️',
    'row':'🪑','pile':'📚','plenty':'💯','floor':'🪵',
    'chimney':'🏭','mole':'🦫','possum':'🐀','moth':'🐛',
    'wasp':'🐝','dragonfly':'🪰','eel':'🐍','seahorse':'🐴',
    'lighthouse':'🗼','firefly':'✨','snowball':'❄️','playground':'🛝',
    'trunk':'🌲','bark':'🪵','bush':'🌿','jam':'🍞','ketchup':'🍅',
    'wool':'🧶','cotton':'☁️','denim':'👖','lace':'🪡','silk':'🪡',
    'chips':'🍟','pork':'🐖','board':'⬜','discount':'📉',

    # ===== batch 1 =====
    'receive':'📥','borrow':'🤲','napkin':'🍽️','hood':'💨',
    'tablecloth':'🍽️','bathmat':'🛁','mouthwash':'👄',
    'cranberry':'🫐','mulberry':'🫐','jackfruit':'🥭',
    'passionfruit':'🥥','rambutan':'🍓','churro':'🥖',
    'guava':'🍐','sweetpotato':'🍠','hearse':'⚰️',
    'submarine':'🚢','wagon':'🚙','stroller':'👶',
    'prison':'🔒','jail':'🔒','glue':'🧴','tape':'📼',
    'iron':'🔩','trial':'⚖️','server':'💁','busboy':'🍽️',
    'pension':'💰','diabetes':'🍬','ground':'⚙️',
    'bound':'🪢','won':'💴','pad':'🩸','hairspray':'💨',
    'foundation':'🧴','flung':'🤾','swung':'🪢',
    'deodorant':'🧴','jetlag':'🕐','asthma':'😮‍💨',
    'strainer':'🥣','colander':'🥣','microwave':'♨️',

    # ===== batch 2 =====
    'nun':'⛪','hairy':'🧔','scrawny':'🦴','foxy':'💋',
    'pinwheel':'🎡','playdough':'🧱','singleplayer':'🧑',
    'npc':'🤖','savanna':'🦒','aloof':'🙅','distant':'🧊',
    'selfless':'🤲','separate':'↔️','forgive':'🙏',
    'ghosting':'🙊','chemistry':'💞','hookup':'🌙',
    'fling':'💔','frenemy':'😏','plaything':'🎲',
    'realism':'📷','cubism':'🔷','mosaic':'🧩',
    'origami':'📄','composting':'🌱','hoarding':'📦',
    'amateur':'🔰','devotee':'🙌','costume':'👗',
    'binge':'📺','ip':'©️','bullmarket':'🐂','bearmarket':'🐻',
    'acidrain':'🌧️','reduce':'➖','opportunitycost':'⚖️',
    'q1':'📅','q2':'📅','reel':'🎞️','defeat':'🏳️',
    'riot':'🔥','ribboncutting':'🎀',

    # ===== batch 3 =====
    'rescuer':'🧑‍🚒','survivor':'🧍','hose':'🚿','hostage':'🙇',
    'horn':'📯','whistle':'😗','refugee':'🧳','flatter':'😏',
    'resent':'😤','lament':'😭','deceive':'🤥','flourish':'🌻',
    'thrive':'🌱','endure':'😣','alone':'🧍','able':'💪',
    'act':'🎭','address':'📮','airmail':'✉️','allow':'✅',
    'anything':'❓','appear':'👀','auntie':'👩','aunty':'👩',
    'base':'🧱','basic':'🧱','bath':'🛁','bathe':'🛁',
    'become':'🦋','believe':'🙏','belong':'🔗','best':'🏆',
    'better':'👍','bite':'🦷','blow':'💨','born':'👶',
    'box':'📦','shovel':'⛏️','rake':'🧹','welder':'⚙️',
    'lawnmower':'🚜','hoe':'⛏️','steel':'🔩','aluminum':'🥫',
    'titanium':'🔩','zinc':'🔋','tin':'🥫','cardboard':'📦',
    'copper':'🪙','feeling blue':'😔',

    # ===== batch 4 =====
    'camp':'⛺','cowboy':'🤠','luncheon':'🍱','lily':'🌷',
    'mail':'📬','pool':'🏊','stair':'🪜','trouble':'⚠️',
    'king':'👑','queen':'👸','glad':'😄','scare':'😱',
    'surprise':'😲','thank':'🙏','fright':'😱','feelings':'💗',
    'catsup':'🍅','jog':'🏃','noise':'📢','clue':'🔍',
    'dam':'🌊','disappoint':'😞','disappointment':'😞',
    'flesh':'🥩','fountain':'⛲','hook':'🪝','appoint':'📋',
    'spit':'💧','sweat':'💦','ditch':'🕳️','image':'🖼️',
    'impress':'✨','impressive':'✨','represent':'📊',
    'motor':'⚙️','impression':'💭','sorrow':'😢',
    'suspicion':'🤨','doubtful':'🤔','announce':'📢',
    'declare':'📢','peep':'👀','magic':'✨','manner':'🛠️',
    'magical':'✨','grammatical':'📝','spray':'💦',
    'track':'👣','superior':'⬆️','tack':'📌','pin':'📌',
    'facial':'😀','oral':'👄','shortly':'⏱️',
    'style':'✨','weaken':'📉','tulip':'🌷',
    'penny':'🪙','dime':'🪙','bang':'💥','loaf':'🍞',
    'glance':'👀','stitch':'🪡','freshman':'🎓',
    'civilian':'👤','consistent':'🎯','unity':'🤝',
    'stepchild':'👶','consequence':'➡️','eve':'🌙',
    'forth':'➡️','cigar':'🚬','chill':'🥶','radar':'📡',
    'remain':'➕','learned':'📚','leisurely':'🚶',
    'apply':'🖌️','reply':'💬','badly':'👎','odd':'🤪',
    'inspire':'💡','fashion':'👗','fashionable':'👗',
    'bravery':'🦁','active':'⚡','freeway':'🛣️',
    'hairdresser':'💇','pitch':'⚾','tasty':'😋',
    'efficient':'⚡',

    # ===== batch 5 =====
    'permanent':'💇','recite':'📖','pursuit':'🏃',
    'sophomore':'🎓','scenery':'🏞️','seagull':'🕊️',
    'shameful':'😳','sparkle':'✨','surf':'🏄',
    'terrify':'😱','troublesome':'😣','tug-of-war':'🪢',
    'vessel':'🚢','alien':'👽','butcher':'🔪',
    'carnation':'🌷','crossing':'🚦','delegate':'🧑‍💼',
    'dressing':'🥗','glee':'😄','gobble':'🦃',
    'gorge':'🏞️','gulp':'😋','jaywalk':'🚸',
    'laser':'🔦','lessen':'📉','lifelong':'⏳',
    'marvel':'😲','mansion':'🏛️','mermaid':'🧜',
    'mayonnaise':'🥫','mutton':'🍖','oversleep':'😴',
    'overeat':'🍔','pier':'⚓','peek':'👀','poetic':'📜',
    'realm':'👑','rubbish':'🗑️','saddle':'🐴',
    'sentiment':'💭','shutter':'🪟','simmer':'🍲',
    'sober':'🧠','spotlight':'💡','spur':'🥾',
    'startle':'😱','stereotype':'🧩','stylish':'👗',
    'token':'🎟️','verbal':'🗣️','wade':'💧',
    'wharf':'⚓','abstraction':'💭','daffodil':'🌼',
    'decent':'👍','dispatch':'📨','disgrace':'😞',
    'heroin':'💉','naval':'⚓','paralyze':'🦽',
    'shoplift':'🛍️','sewer':'🚽','spire':'⛪',
    'treason':'⚖️','reservoir':'💧','carbohydrate':'🍞',
    'caffeine':'☕','burial':'⚰️','radiant':'✨',
    'rein':'🐎','sprawl':'🛌','clinical':'🏥',
    'expertise':'🛠️','specialize':'🎯','accelerate':'⚡',
    'morale':'💪','distrust':'🤨','melancholy':'😔',
    'indignant':'😠','indignation':'😠','affectionate':'🥰',
    'crust':'🥧','crumb':'🍞','grill':'🍳','stew':'🍲',
    'pastry':'🥐','dandruff':'💆','bowel':'🫃',
    'clam':'🦪','locust':'🦗','oyster':'🦪','trout':'🐟',
    'woodpecker':'🐦','harness':'🐴','saloon':'🍺',
    'symbolic':'🔣','symbolize':'🔣',

    # ===== batch 6 =====
    'victor':'🏆','watertight':'💧','windshield':'🚗',
    'sweetness':'🍬','encouragement':'💪','fisher':'🎣',
    'learner':'🧑‍🎓','thinker':'🤔','maker':'🔨',
    'navigator':'🧭','cyclist':'🚴','optimist':'😊',
    'pessimist':'😔','whim':'💭','spent':'💸',
    'sadly':'😢','delete':'🗑️','backdrop':'🖼️',
    'beachfront':'🏖️','beehive':'🐝','breadcrumb':'🍞',
    'newsletter':'📰','sitemap':'🗺️','endorse':'👍',
    'stockholder':'📈','blister':'🩹','pandemic':'🦠',
    'predator':'🦁','clueless':'🤷','regretful':'😞',
    'sleepless':'😴','confide':'🤫','deplore':'😢',
    'disseminate':'📡','exalt':'🙌','exhilarate':'🤩',
    'mortify':'😳','overpower':'💪','peruse':'📖',
    'promulgate':'📜','salvage':'🛟','brie':'🧀',
    'cashew':'🥜','cheddar':'🧀','lasagna':'🍝',
    'mascarpone':'🧀','parmesan':'🧀','pistachio':'🥜',
    'saffron':'🌸','tortilla':'🌮','insurgent':'⚔️',
    'warhead':'💣','zealot':'🔥','volcanic':'🌋',
    'crusader':'⚔️','unbearable':'😣',
}

n = 0
not_found = []
for word, new_emoji in FIXES.items():
    if word not in idx:
        not_found.append(word)
        continue
    old = idx[word].get('img','')
    if old == new_emoji:
        continue
    idx[word]['img'] = new_emoji
    n += 1

with open(VOCAB, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"已修 emoji: {n}")
if not_found:
    print(f"找不到 ({len(not_found)}): {not_found[:30]}")
