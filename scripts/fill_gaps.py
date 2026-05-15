"""補家族線 / 易混提示的漏網之魚"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', 'vocab.json'))
with open(VOCAB,'r',encoding='utf-8') as f: data=json.load(f)
words = data['words']
idx = {w['word']: w for w in words}

# ============ 1) 不規則動詞補 base ============
IRR = {
    'bore':      ('bear',  '已經承受過的版本(過去式;也指鑽孔)'),
    'beat':      ('beat',  '已經打敗的版本(過去式同形;也指拍子/節拍)'),
    'become':    ('become','成為(過去式同形)'),
    'bet':       ('bet',   '已經打賭的版本(過去式同形)'),
    'bit':       ('bite',  '已經咬過的版本(過去式)'),
    'blown':     ('blow',  '已經吹過的版本(過去分詞,配 have 用)'),
    'broadcast': ('broadcast','已經播放過的版本(過去式同形)'),
    'burst':     ('burst', '已經爆裂的版本(過去式同形)'),
    'forecast':  ('forecast','已經預測過的版本(過去式同形)'),
    'ground':    ('grind', '已經研磨的版本(過去式;也指地面)'),
    'lay':       ('lie',   '躺(過去式;但也是「放置」動詞原形,易混)'),
    'read':      ('read',  '已經讀過的版本(過去式同形,唸 ㄖㄝㄉ)'),
    'run':       ('run',   '已經跑過的版本(過去分詞同形)'),
    'swung':     ('swing', '已經揮過的版本(過去式)'),
    'upset':     ('upset', '已經弄翻/沮喪的版本(過去式同形)'),
    'woken':     ('wake',  '已經醒了的版本(過去分詞,配 have 用)'),
    'wept':      ('weep',  '已經哭過的版本(過去式)'),
    'wound':     ('wind',  '已經繞過的版本(過去式;也指傷口)'),
}

# ============ 2) 衍生詞補 base ============
DERIV = {
    'rider':       ('ride',     '做這件事的人(rid + er,騎乘者)'),
    'creation':    ('create',   '這個動作的結果(creat + ion,創造物)'),
    'discussion':  ('discuss',  '這個動作的結果(discuss + ion,討論)'),
    'decision':    ('decide',   '這個動作的結果(decis + ion,決定)'),
    'education':   ('educate',  '這個動作的結果(educ + ation,教育)'),
    'translation': ('translate','這個動作的結果(translat + ion,翻譯)'),
    'protection':  ('protect',  '這個動作的結果(protect + ion,保護)'),
    'happiness':   ('happy',    '「…的性質」(y 變 i + ness,開心)'),
    'beautiful':   ('beauty',   '「充滿…的」(y 變 i + ful,美麗的)'),
}

# ============ 3) 同音/易混字補 homophone-note ============
HOMO = {
    'breath':    '⚠️ 易混字:breath 呼吸(名詞,ㄅㄖㄝㄙ)/ breathe 呼吸(動詞,ㄅㄖㄧㄈ)',
    'breathe':   '⚠️ 易混字:breathe 呼吸(動詞,ㄅㄖㄧㄈ)/ breath 呼吸(名詞,ㄅㄖㄝㄙ)',
    'cloth':     '⚠️ 易混字:cloth 布料(名詞,ㄎㄌㄛㄙ)/ clothe 給...穿衣服(動詞,ㄎㄌㄛㄈ)',
    'clothe':    '⚠️ 易混字:clothe 給...穿衣服(動詞,ㄎㄌㄛㄈ)/ cloth 布料(名詞,ㄎㄌㄛㄙ)',
    'bath':      '⚠️ 易混字:bath 浴缸/泡澡(名詞)/ bathe 洗澡(動詞)',
    'bathe':     '⚠️ 易混字:bathe 洗澡(動詞)/ bath 浴缸/泡澡(名詞)',
    'knew':      '⚠️ 同音字:knew 知道(過去式,k 不發音)/ new 新的',
    'beet':      '⚠️ 同音字:beet 甜菜根 / beat 打敗',
    'made':      '⚠️ 同音字:made 做(過去式)/ maid 女僕',
    'maid':      '⚠️ 同音字:maid 女僕 / made 做(過去式)',
    'threw':     '⚠️ 同音字:threw 丟(過去式)/ through 穿過(介系詞)',
    'through':   '⚠️ 同音字:through 穿過 / threw 丟(過去式)',
    'flew':      '⚠️ 同音字:flew 飛(過去式)/ flu 流感',
    'flu':       '⚠️ 同音字:flu 流感 / flew 飛(過去式)',
    'bored':     '⚠️ 易混字:bored 無聊的(人)/ board 木板',
    'board':     '⚠️ 易混字:board 木板 / bored 無聊的(人)',
    'be':        '⚠️ 同音字:be 是、當 / bee 蜜蜂',
    'bee':       '⚠️ 同音字:bee 蜜蜂 / be 是、當',
    'eight':     '⚠️ 同音字:eight 八 / ate 吃(過去式)',
    'ate':       '⚠️ 同音字:ate 吃(過去式)/ eight 八',
    'heel':      '⚠️ 同音字:heel 腳跟 / heal 治癒',
    'heal':      '⚠️ 同音字:heal 治癒 / heel 腳跟',
    'hi':        '⚠️ 同音字:hi 嗨 / high 高的',
    'high':      '⚠️ 同音字:high 高的 / hi 嗨',
    'him':       '⚠️ 同音字:him 他(受格)/ hymn 讚美詩',
    'hymn':      '⚠️ 同音字:hymn 讚美詩 / him 他(受格)',
    'miner':     '⚠️ 同音字:miner 礦工 / minor 次要的、未成年',
    'minor':     '⚠️ 同音字:minor 次要的、未成年 / miner 礦工',
    'not':       '⚠️ 同音字:not 不 / knot 結(k 不發音)',
    'knot':      '⚠️ 同音字:knot 結(k 不發音)/ not 不',
    'oar':       '⚠️ 同音字:oar 槳 / or 或者 / ore 礦石',
    'or':        '⚠️ 同音字:or 或者 / oar 槳 / ore 礦石',
    'ore':       '⚠️ 同音字:ore 礦石 / or 或者 / oar 槳',
    'peek':      '⚠️ 同音字:peek 偷看 / peak 山峰',
    'peak':      '⚠️ 同音字:peak 山峰 / peek 偷看',
    'pray':      '⚠️ 同音字:pray 祈禱 / prey 獵物',
    'prey':      '⚠️ 同音字:prey 獵物 / pray 祈禱',
    'rain':      '⚠️ 同音字:rain 雨 / reign 統治 / rein 韁繩',
    'reign':     '⚠️ 同音字:reign 統治 / rain 雨 / rein 韁繩',
    'rein':      '⚠️ 同音字:rein 韁繩 / rain 雨 / reign 統治',
    'rap':       '⚠️ 同音字:rap 饒舌 / wrap 包裹(w 不發音)',
    'red':       '⚠️ 同音字:red 紅色 / read 讀(過去式 ㄖㄝㄉ)',
    'role':      '⚠️ 同音字:role 角色 / roll 滾、捲',
    'roll':      '⚠️ 同音字:roll 滾、捲 / role 角色',
    'seen':      '⚠️ 易混字:seen 看見(過去分詞)/ scene 場景',
    'scene':     '⚠️ 易混字:scene 場景 / seen 看見(過去分詞)',
    'sew':       '⚠️ 同音字:sew 縫紉 / so 所以 / sow 播種',
    'so':        '⚠️ 同音字:so 所以 / sew 縫紉 / sow 播種(動詞時)',
    'sow':       '⚠️ 同音字:sow 播種(動詞)/ sew 縫紉 / so 所以',
    'soar':      '⚠️ 同音字:soar 翱翔 / sore 痠痛的',
    'sore':      '⚠️ 同音字:sore 痠痛的 / soar 翱翔',
    'some':      '⚠️ 同音字:some 一些 / sum 總和',
    'sum':       '⚠️ 同音字:sum 總和 / some 一些',
    'stair':     '⚠️ 同音字:stair 樓梯 / stare 盯著看',
    'stare':     '⚠️ 同音字:stare 盯著看 / stair 樓梯',
    'steal':     '⚠️ 同音字:steal 偷 / steel 鋼',
    'steel':     '⚠️ 同音字:steel 鋼 / steal 偷',
    'sweet':     '⚠️ 同音字:sweet 甜的 / suite 套房、組曲',
    'suite':     '⚠️ 同音字:suite 套房、組曲 / sweet 甜的',
    'toe':       '⚠️ 同音字:toe 腳趾 / tow 拖、拽',
    'tow':       '⚠️ 同音字:tow 拖、拽 / toe 腳趾',
    'vain':      '⚠️ 同音字:vain 徒勞的 / vein 血管',
    'vein':      '⚠️ 同音字:vein 血管 / vain 徒勞的',
    'wear':      '⚠️ 同音字:wear 穿 / where 哪裡',
    'where':     '⚠️ 同音字:where 哪裡 / wear 穿',
    'which':     '⚠️ 同音字:which 哪個 / witch 女巫',
    'witch':     '⚠️ 同音字:witch 女巫 / which 哪個',
    'whine':     '⚠️ 同音字:whine 抱怨 / wine 酒',
    'wine':      '⚠️ 同音字:wine 酒 / whine 抱怨',
    'would':     '⚠️ 同音字:would 將會 / wood 木頭',
    'wood':      '⚠️ 同音字:wood 木頭 / would 將會',
    # 易混(用法不同)
    'lay':       '⚠️ 易混字:lay 放置(及物動詞,lay-laid-laid)/ lie 躺(不及物,lie-lay-lain)— 過去式撞字!',
    'lie':       '⚠️ 易混字:lie 躺(lie-lay-lain)/ lay 放置(lay-laid-laid)/ lie 說謊(lie-lied-lied)',
    'rise':      '⚠️ 易混字:rise 上升(不及物,rise-rose-risen)/ raise 抬起(及物,raise-raised-raised)',
    'raise':     '⚠️ 易混字:raise 抬起(及物,需受詞)/ rise 上升(不及物,自己升)',
    'sit':       '⚠️ 易混字:sit 坐(動詞)/ seat 座位(名詞)/ set 設置',
    'seat':      '⚠️ 易混字:seat 座位(名詞)/ sit 坐(動詞)',
    'lend':      '⚠️ 易混字:lend 借出(I lend you)/ borrow 借入(I borrow from you)',
    'borrow':    '⚠️ 易混字:borrow 借入(I borrow from you)/ lend 借出(I lend you)',
    'teach':     '⚠️ 易混字:teach 教(老師→學生)/ learn 學(學生方)',
    'learn':     '⚠️ 易混字:learn 學(學生方)/ teach 教(老師→學生)',
    'bring':     '⚠️ 易混字:bring 帶來(朝說話者)/ take 帶走(離說話者)',
    'take':      '⚠️ 易混字:take 帶走(離說話者)/ bring 帶來(朝說話者)',
    'say':       '⚠️ 易混字:say 說「話的內容」/ tell 告訴「對象」/ speak 講「語言/演講」',
    'tell':      '⚠️ 易混字:tell 告訴(後接人)/ say 說(後接話)/ speak 講語言',
    'speak':     '⚠️ 易混字:speak 講語言/演講 / say 說話 / tell 告訴某人',
    'hope':      '⚠️ 易混字:hope 希望(可能實現)/ wish 但願(常為不可能或過去遺憾)',
    'wish':      '⚠️ 易混字:wish 但願(常為不可能)/ hope 希望(可能實現)',
    'few':       '⚠️ 易混字:few 少數(可數,a few=有一些 / few=幾乎沒)/ little 一點(不可數)',
    'little':    '⚠️ 易混字:little 一點(不可數,a little=有一些 / little=幾乎沒)/ few 少數(可數)',
    'many':      '⚠️ 易混字:many 很多(可數,many books)/ much 很多(不可數,much water)',
    'much':      '⚠️ 易混字:much 很多(不可數,much water)/ many 很多(可數,many books)',
    'among':     '⚠️ 易混字:among 在...之中(3+ 個)/ between 在...之間(2 個)',
    'between':   '⚠️ 易混字:between 在...之間(2 個)/ among 在...之中(3+ 個)',
    'beside':    '⚠️ 易混字:beside 在...旁邊(位置)/ besides 除...之外(還有)',
    'besides':   '⚠️ 易混字:besides 除...之外(還有)/ beside 在...旁邊(位置)',
    'further':   '⚠️ 易混字:further 更進一步(抽象)/ farther 更遠(實際距離)',
    'farther':   '⚠️ 易混字:farther 更遠(實際距離)/ further 更進一步(抽象)',
    'alone':     '⚠️ 易混字:alone 獨自(中性)/ lonely 寂寞(帶負面情緒)',
    'lonely':    '⚠️ 易混字:lonely 寂寞(帶負面情緒)/ alone 獨自(中性)',
    'ago':       '⚠️ 易混字:ago 「(現在算回去)幾天前」/ before 「(某時間點之前)」',
    'before':    '⚠️ 易混字:before 「(某時間點之前)」/ ago 「(現在算回去)幾天前」',
    'almost':    '⚠️ 易混字:almost 幾乎(副詞,almost all)/ nearly 接近地(可互換但 almost 更廣)',
    'nearly':    '⚠️ 易混字:nearly 接近地 / almost 幾乎(可互換但 almost 更廣)',
    'imply':     '⚠️ 易混字:imply 暗示(說話者方)/ infer 推論(聽者方)',
    'infer':     '⚠️ 易混字:infer 推論(聽者方)/ imply 暗示(說話者方)',
    'comprise':  '⚠️ 易混字:comprise 包含(整體 comprises 部分)/ compose 組成(部分 compose 整體)',
    'compose':   '⚠️ 易混字:compose 組成(部分 compose 整體)/ comprise 包含(整體 comprises 部分)',
    'compliment':'⚠️ 易混字:compliment 讚美 / complement 補足、互補',
    'complement':'⚠️ 易混字:complement 補足、互補 / compliment 讚美',
    'council':   '⚠️ 易混字:council 議會、委員會 / counsel 建議、諮商',
    'counsel':   '⚠️ 易混字:counsel 建議、諮商 / council 議會、委員會',
    'emigrate':  '⚠️ 易混字:emigrate 移出(從本國離開)/ immigrate 移入(進入新國)',
    'immigrate': '⚠️ 易混字:immigrate 移入(進入新國)/ emigrate 移出(從本國離開)',
    'precede':   '⚠️ 易混字:precede 在...之前(順序)/ proceed 進行、繼續',
    'proceed':   '⚠️ 易混字:proceed 進行、繼續 / precede 在...之前(順序)',
}

n_irr = n_deriv = n_homo = 0
for word, (base, note) in IRR.items():
    if word in idx and 'base' not in idx[word]:
        idx[word]['base'] = base
        idx[word]['family-note'] = note
        n_irr += 1

for word, (base, note) in DERIV.items():
    if word in idx and 'base' not in idx[word]:
        idx[word]['base'] = base
        idx[word]['family-note'] = note
        n_deriv += 1

for word, note in HOMO.items():
    if word in idx and 'homophone-note' not in idx[word]:
        idx[word]['homophone-note'] = note
        n_homo += 1

with open(VOCAB,'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"不規則動詞補:  {n_irr}")
print(f"衍生詞補:      {n_deriv}")
print(f"同音/易混字補: {n_homo}")
print(f"總 base:       {sum(1 for w in words if 'base' in w)}")
print(f"總 homophone:  {sum(1 for w in words if 'homophone-note' in w)}")
