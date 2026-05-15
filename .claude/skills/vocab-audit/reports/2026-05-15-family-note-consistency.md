# L2-family-note-consistency 審查報告

> 2026-05-15 派 7 個 agent 平行掃 10,101 字的家族線(1,268 個有 base 的字),
> 找出 family-note 跟 mean / base 的邏輯衝突。**未套用**,等學習者決定。

## 重點發現

7 個 agent 共回報約 225 筆問題,分以下幾類:

### 🔴 A. base 字源錯誤(假家族線)— ~40 字

機器原本用「字尾匹配 + 字根在 vocab 裡」自動標,但實際上很多字根對不上:

| word | 機器標的 base | 真相 |
|---|---|---|
| molest | mole | 來自拉丁 molestus,跟「鼴鼠/痣」無關 |
| faction | face | 來自拉丁 facere(做),跟「臉」無關 |
| coalition | coal | 來自 coalesce,跟「煤」無關 |
| paradise | parade | 無詞源關係 |
| capable | cap | 來自拉丁 capere,跟「帽子」無關 |
| visible | vise | 來自拉丁 videre,跟「老虎鉗」無關 |
| mental | mind | 來自拉丁 mens,不是 mind+al |
| notion | no | 來自拉丁 notio,跟「不」無關 |
| comment | come | 來自拉丁 commentum,跟「來」無關 |
| tradition | trade | 來自拉丁 tradere,跟「交易」無關 |
| passive | pass | 來自拉丁 pati(承受) |
| petition | pet | 來自拉丁 petere |
| savor | save | 來自 sapor,跟「拯救」無關 |
| legible | leg | 來自 legere,跟「腿」無關 |
| improvise | improve | 字源不同 |
| pension | pen | 來自 pendere |
| operation | opera | 應為 operate |
| caption | cap | 來自 capere,跟「帽子」無關 |
| donation | done | 應為 donate |
| pious | pie | 來自 pius,跟「派」無關 |
| rotation | rot | 應為 rotate |
| banner | ban | 詞源無關 |
| mansion | man | 來自 manere,跟「男人」無關 |
| notable | not | 應為 note |
| sober | sob | 詞源無關 |
| torment | tore | 應為 torment 自身 |
| violation | viola | 應為 violate |
| tension | ten | 應為 tense |
| fury | fur | 詞源無關 |
| career | care | 來自法語跑道,無關 |
| earnest | earn | 詞源無關 |
| tender | tend | 詞源無關 |
| alive | ale | 應為 live |
| business | bus | 應為 busy |
| solution | sole | 應為 solve |
| copier | cop | 應為 copy |
| frontier | front | front+ier 不是比較級 |
| forgive | forge | 應為 give |
| action | ace | 應為 act |
| animation | anime | 應為 animate(anime 是縮寫) |

**建議**:這些字的 base + family-note 應該**直接刪除**,而不是改。標錯比沒標更誤導。

### 🟡 B. 詞性不符 / 名詞 vs 進行式 — ~80 字

`-ing/-ed/-al/-ation/-ment` 名詞被機器套上「進行式/過去式/形容詞」模板:

| word | mean | 現在 note | 應該 |
|---|---|---|---|
| shooting | 槍擊 | 正在…進行式 | 名詞化(事件) |
| warning | 警告 | 正在…進行式 | 名詞化 |
| ruling | 裁決 | 正在統治進行式 | 名詞化(結果) |
| voting | 投票 | 進行式 | 動名詞 |
| drawing | 圖畫 | 進行式 | 名詞(結果) |
| setting | 場景 | 進行式 | 名詞 |
| screening | 放映 | 進行式 | 名詞(事件) |
| manufacturing | 製造業 | 進行式 | 名詞(行業) |
| opening | 開幕 | 進行式 | 名詞(事件) |
| closing | 閉幕 | 進行式 | 名詞(事件) |
| gathering | 聚會 | 進行式 | 名詞 |
| training | 訓練 | 進行式 | 名詞(課程) |
| reading | 閱讀 | 進行式 | 動名詞 |
| writing | 寫作 | 進行式 | 動名詞 |
| baking | 烘焙 | 進行式 | 動名詞 |
| booking | 訂位 | 進行式 | 名詞 |
| fitting | 試穿 | 進行式 | 名詞 |
| healing | 癒合 | 進行式 | 名詞 |
| painting | 畫(作) | 進行式 | 名詞 |
| building | 建築物 | 進行式 | 名詞 |
| meeting | 會議 | 進行式 | 名詞(已部分修) |
| serving | 一份 | 進行式 | 名詞 |
| offering | 供品 | 進行式 | 名詞 |
| sparkling | 氣泡 | 正在閃亮進行式 | 形容詞 |
| including | 包括 | 進行式 | 介系詞 |
| considering | 考慮到 | 進行式 | 連接詞 |
| supposing | 假設 | 進行式 | 連接詞 |
| provided | 假如 | 過去式 | 連接詞 |
| signal | 信號 | 形容詞 +al | 名詞 |
| narrative | 敘事 | 形容詞 +ive | 名詞 |
| detective | 偵探 | 形容詞 +ive | 名詞 |
| relative | 親戚 | 形容詞 +ive | 名詞 |
| executive | 主管 | 形容詞 +ive | 名詞 |
| archive | 封存 | 形容詞 +ive | 動詞 |
| treatise | 論文 | 動詞 +ise | 名詞 |
| proposal | 求婚 | 形容詞 +al | 名詞 |
| withdrawal | 戒斷 | 形容詞 +al | 名詞 |
| recital | 獨奏會 | 形容詞 +al | 名詞 |
| betrayal | 背叛 | 形容詞 +al | 名詞 |
| arrival | 抵達 | 形容詞 +al | 名詞 |
| departure | 出發 | 形容詞 +al(字尾錯) | 名詞 -ure |
| refusal | 拒絕 | 形容詞 +al | 名詞 |
| denial | 否認 | 形容詞 +al | 名詞 |
| rehearsal | 排練 | 形容詞 +al | 名詞 |
| removal | 移去 | 形容詞 +al | 名詞 |
| rental | 租金 | 形容詞 +al | 名詞 |
| disposal | 處理 | 形容詞 +al | 名詞 |
| musical | 音樂劇 | 形容詞 +al | 名詞用法 |
| bakery / grocery / delivery / recovery | -店/-業 | 形容詞 +y | 名詞 -ery/-ry |
| starter | 前菜 | 做這件事的人 | 物 |
| former | 前者 | +er 人/工具 | 形容詞/代名詞 |
| closer | 更近 | +er 人/工具 | 比較級形容詞 |
| regardless | 無論 | +less 形容詞 | 副詞 |
| moved | 感動的 | 過去式 | 形容詞 |
| broken | 壞掉 | 過去分詞配 have | 形容詞 |
| drunk | 喝醉的 | 過去分詞 | 形容詞 |
| used | 舊的 | 過去式 | 形容詞 |
| learned | 博學的 | 過去式 | 形容詞 |
| promising | 有希望的 | 進行式 | 形容詞 |

**建議**:這些字的 family-note 改用「名詞化版本」「形容詞版本」「連接詞用法」等對的模板,**不用刪 base**(base 是對的,只是 note 模板套錯)。

### 🟡 C. self-base(三態同形字)— ~10 字

| word | 現在 | 問題 |
|---|---|---|
| run / read / put / cut / hit / let / shut / bet / burst / quit / spread | base=自己 | mean 是現在式,note 卻寫「過去式同形」造成混亂 |
| forecast | base=forecast | mean=名詞「預報」,note 寫動詞過去式 |
| beat | base=beat | mean=名詞節拍,note 主軸是動詞過去式 |
| set / hurt / upset | base=自己 | 多義字需要更完整說明 |
| split / thrust / forbid | base=自己 | forbid 過去式其實是 forbade,不是同形 |

**建議**:這些字的 base 改成「移除」,或改成 `"原形和過去式同拼字"` 類描述。

### 🟡 D. 同形異義字混淆 — ~10 字

| word | mean | base 標的 | 問題 |
|---|---|---|---|
| left | 左 | leave | 「左」跟 leave 過去式同形但不同字 |
| won | 韓圓 | win | 貨幣名跟 win 過去式同形不同源 |
| wound | 傷口 | wind | 名詞傷口跟動詞繞的過去式同形不同源 |
| poker | 撲克 | poke | 牌類遊戲跟撥火棒不同源 |
| paradise | 天堂 | parade | 完全無關 |
| fed | 聯準會 | feed | 縮寫 vs feed 過去式 |
| cast | 演員陣容 | cast | 名詞義跟動詞過去式不該套同模板 |

**建議**:加註「同形字」或刪除 base。

### 🟡 E. family-note 太抽象違反白話原則 — ~30 字

| word | 現在 note | 應該白話化 |
|---|---|---|
| daily/weekly/monthly/yearly/hourly | 副詞版本 +ly | 形容詞/副詞版本(daily 主要當形容詞用) |
| lonely / friendly | 副詞版本 +ly | 形容詞版本(+ly 接名詞變形容詞,例外) |
| snowy / foggy / healthy / juicy / easy / funny | 「描述帶有 X 特性的」 | 直接說「下雪的/起霧的/健康的」 |
| reservation / presentation / assignment 等 -ation/-ment | 「這個動作的結果/事物」 | 加具體例子 |
| developer / producer / winner / loser / lover | 「做這件事的人/工具」 | 統一說「人」(很明顯不是工具) |
| opener / toaster / mixer / freezer / shaver | 「做這件事的人/工具」 | 統一說「東西」(很明顯不是人) |
| was / were | 用詞抽象 | 補主詞列表(I/he/she/it 配 was) |
| portable / profitable / fashionable / agreeable | 「可以被 X」 | 補語意橋接 |
| critical | 「批判的」 | mean 是「危急的、關鍵的」應對齊 |
| fearful / hateful | +ful 形容詞 | 釐清語意方向(主動 vs 被動) |
| conventional | 「會議的」 | 應為「傳統的、常規的」 |
| shortly | 「+ly 不久」 | 補橋接「short 時間後 → 立刻」 |

### 🟡 F. 詞義/語意衝突 — ~20 字

| word | mean | family-note | 衝突 |
|---|---|---|---|
| shaver | 理髮師 | 刮鬍刀 | mean 跟 note 不同物 |
| cashier | 收銀員 | 比較級 | cashier 是「人」不是 cash 的比較級 |
| wise | 明智 | base=we 動詞版本 | base 完全錯,wise 是形容詞 |
| endive | 苦苣 | +ive 形容詞 | endive 是植物名詞 |
| upset(emotions 主題) | 心煩 | 過去式弄翻 | 主題下應對應形容詞用法 |
| broadcast(名詞) | 播送 | 動詞過去式同形 | 詞性錯位 |
| bid | 投標 | 過去式 | 自指 + mean 是名詞 |
| sparkling(飲料) | 氣泡 | 正在閃亮 | 飲料語境下應為形容詞 |
| miserable | 悲慘 | base=miser(吝嗇鬼) | 字源實際來自 misery |
| rubber | 橡膠 | 橡皮擦 | mean 是材料,note 寫具體物品 |
| foundation | 粉底液 | 動作結果(found→) | 語意斷裂(打地基→粉底?) |
| won(貨幣) | 韓圓 | win 過去式 | 完全無關 |
| broken / drunk / used / learned | 形容詞 mean | 過去分詞動詞 note | 詞性 |
| moved | 感動的 | 移動過去式 | 語意 |
| fearful | 可怕的 | 充滿…的 | 方向相反 |
| boring(box+ing) | 拳擊 | 運動 +ing | OK 但 box 主義是盒子需補 |
| funny | 好笑 | +y 描述 fun 特性 | 抽象 |

## 套用建議

**保守做法(建議)**:
1. **刪除 A 類 40 個假家族線** — 標錯不如不標
2. **修正 B 類 80 個詞性錯誤** — 套對的模板
3. **D 類同形字加註** — 避免混淆
4. **E + F 類** — 較主觀,個案處理

**激進做法**:全部 225 筆套用(包含主觀判斷)。

## 不套用先存的原因

很多修正涉及「該刪 base 還是該保留只改 note」這種**語言學 vs 教學取捨**判斷。例如:
- `wise` 字源真的不是 we+ise,但對學習者來說標 base 沒任何學習價值,該全刪
- `passive` 字源是 pati 但學習者一定先學 pass,標一下提醒「拼字像但無關」可能有用?

這些都需要學習者(你)決定教學取向才能定案。

## 工具狀態

- batches 切完留在 `batches/20260515-family-note-consistency/`
- 完整 agent 輸出留在 task output(已收完)
- history.json 待你決定後再 update
