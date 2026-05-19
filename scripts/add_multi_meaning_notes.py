#!/usr/bin/env python3
"""一次性腳本:批次補上 homophone-note(多義字 / 多種發音)。

只動沒 note 的字,有 note 的一律跳過(不蓋掉學習者既有判斷)。
"""
import json
from pathlib import Path

VOCAB = Path(__file__).parent.parent / "vocab.json"

# ── Tier 1: 兩種發音(heteronym - 不同唸法)─────────────────
HETERONYMS = {
    "read": "⚠️ 兩種發音:read ㄖㄧㄉ=讀(現在式)/ ㄖㄝㄉ=讀過(過去式 / 過去分詞,拼字相同)",
    "lead": "⚠️ 兩種發音:lead ㄌㄧㄉ=領導(動詞)/ ㄌㄝㄉ=鉛(名詞)",
    "tear": "⚠️ 兩種發音:tear ㄊㄧㄜ=眼淚(名詞)/ ㄊㄜ=撕、扯破(動詞)",
    "bow": "⚠️ 兩種發音:bow ㄅㄠ=鞠躬、船頭 / ㄅㄡ=弓、蝴蝶結",
    "record": "⚠️ 兩種發音:record 重音在前=名詞:紀錄、唱片 / 重音在後=動詞:錄音、記錄",
    "conduct": "⚠️ 兩種發音:conduct 重音在前=名詞:行為、品行 / 重音在後=動詞:指揮、進行",
    "desert": "⚠️ 兩種發音:desert ㄉㄝㄗㄜㄊ=沙漠(名詞)/ ㄉㄧㄗㄜㄊ=拋棄(動詞)",
    "present": "⚠️ 兩種發音:present 重音在前=名詞:現在、禮物 / 重音在後=動詞:呈現、贈送",
    "object": "⚠️ 兩種發音:object 重音在前=名詞:物體 / 重音在後=動詞:反對",
    "subject": "⚠️ 兩種發音:subject 重音在前=名詞:科目、主題 / 重音在後=動詞:使臣服",
    "contest": "⚠️ 兩種發音:contest 重音在前=名詞:比賽 / 重音在後=動詞:競爭、爭奪",
    "contract": "⚠️ 兩種發音:contract 重音在前=名詞:合約 / 重音在後=動詞:收縮、感染(疾病)",
    "export": "⚠️ 兩種發音:export 重音在前=名詞:出口物 / 重音在後=動詞:出口、輸出",
    "import": "⚠️ 兩種發音:import 重音在前=名詞:進口物 / 重音在後=動詞:進口",
    "progress": "⚠️ 兩種發音:progress 重音在前=名詞:進步 / 重音在後=動詞:進行、進步",
    "project": "⚠️ 兩種發音:project 重音在前=名詞:專案 / 重音在後=動詞:投射、預測",
    "protest": "⚠️ 兩種發音:protest 重音在前=名詞:抗議 / 重音在後=動詞:抗議",
    "produce": "⚠️ 兩種發音:produce 重音在前=名詞:農產品 / 重音在後=動詞:生產、製造",
    "permit": "⚠️ 兩種發音:permit 重音在前=名詞:許可證 / 重音在後=動詞:允許",
    "refuse": "⚠️ 兩種發音:refuse ㄖㄝㄈㄧㄨㄙ=名詞:廢棄物 / ㄖㄧㄈㄩㄗ=動詞:拒絕",
    "content": "⚠️ 兩種發音:content 重音在前=名詞:內容 / 重音在後=形容詞:滿意的",
    "estimate": "⚠️ 兩種發音:estimate 結尾 -ate 唸 ㄜㄊ=名詞:估計值 / 唸 ㄝㄊ=動詞:估計",
    "advocate": "⚠️ 兩種發音:advocate 結尾 -ate 唸 ㄜㄊ=名詞:擁護者 / 唸 ㄝㄊ=動詞:提倡",
    "alternate": "⚠️ 兩種發音:alternate 結尾 -ate 唸 ㄜㄊ=形容詞:替換的 / 唸 ㄝㄊ=動詞:輪流",
    "associate": "⚠️ 兩種發音:associate 結尾 -ate 唸 ㄜㄊ=名詞:同事、夥伴 / 唸 ㄝㄊ=動詞:聯想、交往",
    "appropriate": "⚠️ 兩種發音:appropriate 結尾 -ate 唸 ㄜㄊ=形容詞:適當的 / 唸 ㄝㄊ=動詞:撥用、挪用",
    "frequent": "⚠️ 兩種發音:frequent 重音在前=形容詞:頻繁的 / 重音在後=動詞:常去",
    "intimate": "⚠️ 兩種發音:intimate 結尾 -ate 唸 ㄜㄊ=形容詞:親密的 / 唸 ㄝㄊ=動詞:暗示",
    "separate": "⚠️ 兩種發音:separate 結尾 -ate 唸 ㄜㄊ=形容詞:分開的 / 唸 ㄝㄊ=動詞:使分開",
    "moderate": "⚠️ 兩種發音:moderate 結尾 -ate 唸 ㄜㄊ=形容詞:中等的、適度的 / 唸 ㄝㄊ=動詞:緩和、主持",
    "deliberate": "⚠️ 兩種發音:deliberate 結尾 -ate 唸 ㄜㄊ=形容詞:故意的、慎重的 / 唸 ㄝㄊ=動詞:商議",
    "dedicate": "⚠️ 一字多義:dedicate 奉獻、致力於 / 把(書、作品)獻給某人",
    "perfect": "⚠️ 兩種發音:perfect 重音在前=形容詞:完美的 / 重音在後=動詞:使完美、改善",
}

# ── Tier 2: 一字多義(同音不同義 - 常踩雷)─────────────────
POLYSEMES = {
    "light": "⚠️ 一字多義:light 光、燈(名)/ 點燃(動)/ 輕的、淡的(形)",
    "spring": "⚠️ 一字多義:spring 春天(名)/ 彈簧、泉水(名)/ 跳躍(動)",
    "bat": "⚠️ 一字多義:bat 球棒(名)/ 蝙蝠(名)",
    "bear": "⚠️ 一字多義:bear 熊(名)/ 承受、忍受(動)/ 生育(動)",
    "check": "⚠️ 一字多義:check 檢查(動)/ 支票(名,英 cheque)/ 結帳、帳單(美式)",
    "watch": "⚠️ 一字多義:watch 手錶(名)/ 觀看、注意(動)",
    "glass": "⚠️ 一字多義:glass 玻璃(名)/ 玻璃杯(名)/ 複數 glasses=眼鏡",
    "date": "⚠️ 一字多義:date 日期(名)/ 約會(名/動)/ 椰棗(水果)",
    "match": "⚠️ 一字多義:match 比賽(名)/ 火柴(名)/ 配對、相符(動)",
    "pen": "⚠️ 一字多義:pen 筆(名)/ 圍欄(名,如 pig pen)",
    "ring": "⚠️ 一字多義:ring 戒指、環(名)/ 響鈴(動,過 rang / rung)",
    "letter": "⚠️ 一字多義:letter 字母(名)/ 信件(名)",
    "well": "⚠️ 一字多義:well 嗯、好吧(感嘆)/ 良好地(副)/ 井(名)",
    "draw": "⚠️ 一字多義:draw 畫、繪(動)/ 拉、拖(動)/ 平手(名,如球賽)",
    "sound": "⚠️ 一字多義:sound 聲音(名)/ 聽起來(動)/ 健全的、可靠的(形)",
    "plant": "⚠️ 一字多義:plant 植物(名)/ 栽種(動)/ 工廠(名,如 power plant)",
    "type": "⚠️ 一字多義:type 類型、種類(名)/ 打字(動)",
    "file": "⚠️ 一字多義:file 檔案(名)/ 銼刀(名)/ 提交(動,如 file a complaint)",
    "form": "⚠️ 一字多義:form 形狀、形式(名)/ 表格(名)/ 形成、組成(動)",
    "ground": "⚠️ 一字多義:ground 地面(名)/ grind 過去式(磨碎了)/ 禁足(動,如 grounded)",
    "last": "⚠️ 一字多義:last 最後的(形)/ 上一個的(形,如 last week)/ 持續(動)",
    "post": "⚠️ 一字多義:post 郵件(名)/ 柱子、職位(名)/ 張貼、發文(動)",
    "second": "⚠️ 一字多義:second 第二(形)/ 秒(名)/ 附議、支持(動)",
    "mind": "⚠️ 一字多義:mind 心智、頭腦(名)/ 介意、留心(動)",
    "kind": "⚠️ 一字多義:kind 善良的(形)/ 種類(名,如 a kind of)",
    "fair": "⚠️ 一字多義:fair 公平的(形)/ 集市、博覽會(名)/ 金髮的、淺色的(形)",
    "safe": "⚠️ 一字多義:safe 安全的(形)/ 保險箱(名)",
    "hot": "⚠️ 一字多義:hot 熱的(形)/ 辣的(形)/ 熱門的、火紅的(形)",
    "cool": "⚠️ 一字多義:cool 涼的(形)/ 酷的(形)/ 冷靜的(形)",
    "fine": "⚠️ 一字多義:fine 好的(形)/ 罰金(名/動)/ 細的、精緻的(形)",
    "patient": "⚠️ 一字多義:patient 病人(名)/ 有耐心的(形)",
    "press": "⚠️ 一字多義:press 按、壓(動)/ 新聞媒體、出版社(名)/ 推舉(健身)",
    "might": "⚠️ 一字多義:might 可能(助動詞)/ 力量、威力(名)/ may 過去式",
    "bill": "⚠️ 一字多義:bill 帳單(名)/ 紙鈔(美,名)/ 法案(名)/ 鳥喙(名)",
    "ball": "⚠️ 一字多義:ball 球(名)/ 舞會(名)",
    "duck": "⚠️ 一字多義:duck 鴨子(名)/ 低頭閃躲(動)",
    "court": "⚠️ 一字多義:court 法庭(名)/ 球場(名,如 tennis court)/ 宮廷(名)",
    "volume": "⚠️ 一字多義:volume 音量(名)/ 體積(名)/ 一卷、一冊(書)",
    "club": "⚠️ 一字多義:club 俱樂部(名)/ 球桿(名,如 golf club)/ 棍棒(名)",
    "stamp": "⚠️ 一字多義:stamp 郵票(名)/ 跺腳、踩(動)/ 印章、戳印(名)",
    "stick": "⚠️ 一字多義:stick 棍棒(名)/ 黏住(動,過 stuck)/ 堅持、刺(動)",
    "swallow": "⚠️ 一字多義:swallow 吞嚥(動)/ 燕子(名)",
    "trunk": "⚠️ 一字多義:trunk 樹幹(名)/ 後車廂(名,美式)/ 象鼻(名)",
    "seal": "⚠️ 一字多義:seal 海豹(名)/ 封印、密封(名/動)/ 印章(名)",
    "star": "⚠️ 一字多義:star 星星(名)/ 明星(名)/ 主演(動,如 starring)",
    "pool": "⚠️ 一字多義:pool 水池、游泳池(名)/ 集合、共用(動,如 carpool)/ 撞球(名)",
    "pack": "⚠️ 一字多義:pack 打包(動)/ 一包、一群(名,如 a pack of wolves)",
    "point": "⚠️ 一字多義:point 點、要點(名)/ 分數(名)/ 指(動)",
    "race": "⚠️ 一字多義:race 賽跑(名/動)/ 種族(名)",
    "state": "⚠️ 一字多義:state 狀態(名)/ 州(名,如 50 states)/ 陳述、聲明(動)",
    "still": "⚠️ 一字多義:still 仍然、還(副)/ 靜止的(形)/ 安靜的(形)",
    "store": "⚠️ 一字多義:store 商店(名)/ 儲存(動)",
    "back": "⚠️ 一字多義:back 後面、背(名)/ 回去、向後(副)/ 支持(動)",
    "front": "⚠️ 一字多義:front 前面(名)/ 前線(名)/ 假象(名)",
    "side": "⚠️ 一字多義:side 邊、旁邊(名)/ 方面(名)/ 立場、一方(名)",
    "line": "⚠️ 一字多義:line 線(名)/ 排隊(名)/ 台詞(名,如 forgot my lines)",
    "stage": "⚠️ 一字多義:stage 舞台(名)/ 階段(名,如 this stage)",
    "change": "⚠️ 一字多義:change 改變(動)/ 零錢(名)/ 換衣服(動)",
    "run": "⚠️ 一字多義:run 跑(動)/ 經營、運作(動)/ 一段時期(名)",
    "pass": "⚠️ 一字多義:pass 經過(動)/ 通過考試(動)/ 通行證(名)",
    "turn": "⚠️ 一字多義:turn 轉彎(動)/ 變成(動)/ 輪流(名,如 my turn)",
    "play": "⚠️ 一字多義:play 玩、演奏(動)/ 戲劇(名)/ 表現(體育)",
    "down": "⚠️ 一字多義:down 向下(副/介)/ 沮喪的(形)/ 羽絨(名)",
    "up": "⚠️ 一字多義:up 向上(副/介)/ 起來、起床(副)/ 結束、到期(形,如 time's up)",
    "over": "⚠️ 一字多義:over 在...上方(介)/ 結束(形,如 it's over)/ 超過(介)",
    "under": "⚠️ 一字多義:under 在...下(介)/ 少於(介)/ 在...之中(介)",
    "just": "⚠️ 一字多義:just 剛剛(副)/ 只是、僅(副)/ 公正的(形)",
    "only": "⚠️ 一字多義:only 只(副)/ 唯一的(形)/ 但是(連,口語)",
    "even": "⚠️ 一字多義:even 甚至(副)/ 平的、平坦的(形)/ 偶數的(形)",
    "fast": "⚠️ 一字多義:fast 快的(形/副)/ 禁食、齋戒(動/名)",
    "iron": "⚠️ 一字多義:iron 鐵(名)/ 熨斗(名)/ 熨燙(動)",
    "free": "⚠️ 一字多義:free 自由的(形)/ 免費的(形)/ 釋放(動)",
    "firm": "⚠️ 一字多義:firm 穩固的(形)/ 公司、事務所(名)",
    "blow": "⚠️ 一字多義:blow 吹(動)/ 打擊(名,如 a heavy blow)/ 搞砸(口語)",
    "bright": "⚠️ 一字多義:bright 明亮的(形)/ 聰明的(形)",
    "bowl": "⚠️ 一字多義:bowl 碗(名)/ 保齡球(動,如 bowling)",
    "novel": "⚠️ 一字多義:novel 小說(名)/ 新奇的(形)",
    "crane": "⚠️ 一字多義:crane 鶴(名)/ 起重機(名)",
    "crow": "⚠️ 一字多義:crow 烏鴉(名)/ 公雞啼叫(動)",
    "mole": "⚠️ 一字多義:mole 鼴鼠(名)/ 痣(名)/ 內奸(名)",
    "pitcher": "⚠️ 一字多義:pitcher 水壺(名)/ 投手(名,棒球)",
    "round": "⚠️ 一字多義:round 圓的(形)/ 一回合、一輪(名)/ 環繞(介)",
    "square": "⚠️ 一字多義:square 正方形(形/名)/ 廣場(名)/ 平方(數學)",
    "spell": "⚠️ 一字多義:spell 拼字、拼寫(動)/ 咒語(名)/ 一段時間(名,如 cold spell)",
    "yard": "⚠️ 一字多義:yard 院子(名)/ 碼(長度,3 英尺)",
    "lap": "⚠️ 一字多義:lap 大腿、膝上(名,如 sit on my lap)/ 一圈(名,跑道)/ 舔(動)",
    "rest": "⚠️ 一字多義:rest 休息(名/動)/ 剩下的(名,如 the rest of)",
    "note": "⚠️ 一字多義:note 筆記(名)/ 音符(名)/ 紙鈔(英)/ 注意到(動)",
    "ground": "⚠️ 一字多義:ground 地面(名)/ grind 過去式(磨碎了)/ 根據、理由(名)",
    "leg": "⚠️ 一字多義:leg 腿(名)/ 一段路程、一段賽程(名)",
    "neck": "⚠️ 一字多義:neck 脖子(名)/ 親熱(動,口語)",
    "arm": "⚠️ 一字多義:arm 手臂(名)/ 武器(名,複數 arms)/ 武裝(動)",
    "cell": "⚠️ 一字多義:cell 細胞(名)/ 牢房(名)/ 手機(美式 cellphone)",
}

# ── 額外補一輪我可能漏掉的多義字 ──────────────────
EXTRA = {
    "rose": "⚠️ 一字多義:rose 玫瑰(名)/ rise 過去式(升起了)",
    "found": "⚠️ 一字多義:found find 過去式(找到了)/ 創立(動,如 found a company)",
    "fly": None,  # already tagged
    "saw": "⚠️ 一字多義:saw see 過去式(看見了)/ 鋸子(名)/ 鋸(動)",
    "rock": None,  # already tagged
    "bank": None,  # already tagged
    "fall": None,  # already tagged
    "kind": None,  # already in POLYSEMES above
    "mean": None,  # already tagged
    "bow": None,  # already in HETERONYMS above
    "fan": "⚠️ 一字多義:fan 電風扇(名)/ 粉絲、迷(名)/ 搧、煽動(動)",
    "wave": "⚠️ 一字多義:wave 波浪(名)/ 揮手(動)/ 浪潮、風潮(名)",
    "wing": "⚠️ 一字多義:wing 翅膀(名)/ 側翼、廂房(名)",
    "head": None,  # already tagged
    "hand": None,  # already tagged
    "foot": None,  # already tagged
    "eye": None,  # already tagged
    "ear": None,  # already tagged (assumed)
    "row": "⚠️ 兩種發音:row ㄖㄡ=一排、划船 / ㄖㄠ=爭吵(英式)",
    "wound": "⚠️ 兩種發音:wound ㄨㄨㄣㄉ=傷口(名)/ ㄨㄠㄣㄉ=wind 過去式(纏繞了)",
    "live": None,  # already tagged
    "use": "⚠️ 兩種發音:use ㄐㄩㄗ=動詞:使用 / ㄐㄩㄙ=名詞:用途",
    "abuse": "⚠️ 兩種發音:abuse ㄜㄅㄐㄩㄗ=動詞:濫用、虐待 / ㄜㄅㄐㄩㄙ=名詞:濫用、虐待",
    "house": "⚠️ 兩種發音:house ㄏㄠㄙ=名詞:房子 / ㄏㄠㄗ=動詞:容納、收容",
    "close": None,  # already tagged
    "wind": None,  # already tagged
    "minute": None,  # already tagged
    "second": None,  # already in POLYSEMES
    "kid": "⚠️ 一字多義:kid 小孩(名)/ 開玩笑(動,如 just kidding)/ 小山羊(名)",
    "rest": None,  # already in POLYSEMES
    "tip": "⚠️ 一字多義:tip 尖端(名)/ 小費(名)/ 訣竅、提示(名)",
    "key": "⚠️ 一字多義:key 鑰匙(名)/ 關鍵的(形)/ 琴鍵、按鍵(名)",
    "lot": "⚠️ 一字多義:lot 許多(名,如 a lot of)/ 一批、一塊地(名)/ 命運、抽籤(名)",
    "drug": "⚠️ 一字多義:drug 藥物(名)/ 毒品(名)/ 下藥(動)",
    "branch": "⚠️ 一字多義:branch 樹枝(名)/ 分公司、分行(名)",
    "case": "⚠️ 一字多義:case 案件(名)/ 盒子、箱(名)/ 情況(名,如 in case)",
    "letter": None,  # already in POLYSEMES
    "right": "⚠️ 一字多義:right 正確的(形)/ 右邊(名/形)/ 權利(名)/ 立刻(副,如 right now)",
    "left": None,  # already tagged
    "long": "⚠️ 一字多義:long 長的(形)/ 長久(副)/ 渴望(動,如 long for)",
    "short": "⚠️ 一字多義:short 短的、矮的(形)/ 短褲(複 shorts)/ 缺乏的(形,如 short on time)",
    "mass": "⚠️ 一字多義:mass 大量、團塊(名)/ 質量(物理)/ 彌撒(名,大寫 Mass)",
    "fall": None,
    "kid": None,  # added above
    "park": None,  # already tagged
    "order": None,  # already tagged
    "trip": None,  # already tagged
    "band": None,  # already tagged
}

UPDATES = {}
for d in (HETERONYMS, POLYSEMES, EXTRA):
    for k, v in d.items():
        if v is None: continue
        if k in UPDATES: continue  # 不覆蓋(HETERONYMS 優先)
        UPDATES[k] = v

print(f"準備寫入的 note 總數: {len(UPDATES)}")


def main():
    data = json.loads(VOCAB.read_text())
    words = data["words"]
    by_word = {w["word"]: w for w in words}

    added = []
    skipped_existing = []
    not_in_vocab = []

    for word, note in UPDATES.items():
        if word not in by_word:
            not_in_vocab.append(word)
            continue
        w = by_word[word]
        if "homophone-note" in w:
            skipped_existing.append(word)
            continue
        w["homophone-note"] = note
        added.append(word)

    # 寫回
    VOCAB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    print()
    print(f"✓ 新增 note: {len(added)} 字")
    for w in added[:5]:
        print(f"    {w:14s}  → {by_word[w]['homophone-note']}")
    print(f"    (省略,共 {len(added)} 字)")
    print()
    print(f"⊘ 已有 note 跳過: {len(skipped_existing)} 字")
    if skipped_existing:
        print(f"    {', '.join(skipped_existing[:20])}")
    print()
    if not_in_vocab:
        print(f"⚠ 不在 vocab 內 跳過: {len(not_in_vocab)} 字")
        print(f"    {', '.join(not_in_vocab)}")

    # 統計總 note 數
    total = sum(1 for w in words if "homophone-note" in w)
    print()
    print(f"=== vocab.json 目前 note 總覆蓋 ===")
    print(f"    homophone-note 字數: {total} / {len(words)}")


if __name__ == "__main__":
    main()
