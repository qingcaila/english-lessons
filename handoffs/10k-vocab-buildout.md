# 交接文件 — 把 vocab.json 擴建到 10,000+ 字

> **這份是給接手 AI 的獨立工作指令**。讀完後不需要原對話脈絡也能執行。學習者本人會把這份貼給新對話。
>
> **目標總時程**:不限,可以分多次對話累積,每次累積 300-500 字。**不要試圖一次塞完 10K**——對話容量會爆,品質會掉。
>
> **建立日**:2026-05-13(基準:224 字)

---

## 0. 在動手之前你必須讀的檔案

按順序讀,讀完就懂專案全貌:

1. **`D:\英\CLAUDE.md`** ← 協作守則,所有硬規則的權威
2. **`D:\英\profile.md`** 第 9 章「詞彙學習哲學」 ← 為什麼用 L4 計、為什麼不要狂加新字
3. **`D:\英\syllabus.md`** ← 5 階段課綱、每階段字量目標
4. **`D:\英\lessons\themes.json`** ← 50+ 主題與分類定義(已存在,擴字時不要動結構)
5. **`D:\英\lessons\vocab.json`** ← 現有 224 字的格式範例,**新字要照同樣格式 append 到 `words` 陣列尾端**

**禁忌**:
- ❌ 不要重新評估學習者程度
- ❌ 不要動 themes.json 的分類結構,只能 append themes(極少需要)
- ❌ 不要碰 srs.js / lesson.html / index.html / quiz.html(那些是運作引擎)

---

## 1. 任務本身

**現況**:`D:\英\lessons\vocab.json` 目前 224 字。
**目標**:擴到 10,000+ 字,涵蓋 Stage 0-4 全主題。
**做法**:每次對話 append 300-500 字到 `words` 陣列,品質優先於速度。

**字量階段對照**(L4 計算):
- Stage 0 超級基礎 → 500-1,000
- Stage 1 基礎 → 2,000-3,000
- Stage 2 中下 → 4,000-5,000
- Stage 3 中 → 5,000-7,000
- Stage 4 中上 → 8,000-10,000+

---

## 2. 單字格式規範(每筆 JSON 必須有這些欄位)

```json
{
  "word": "bedtime",
  "mean": "就寢時間",
  "img": "🛏️🕘",
  "chunks": ["bed","time"],
  "py": "ㄅㄝㄉ-ㄊㄞㄇ",
  "split": "bed (CVC) + time (silent-e)",
  "theme": "phonics-compound",
  "stage": 0
}
```

### 各欄位規則

| 欄位 | 規則 |
|------|------|
| `word` | 全小寫英文字。複合字不加連字號(`bedtime` 不是 `bed-time`) |
| `mean` | 中文意思,**短,2-4 字最佳**。多義字用 `/` 分隔(例 `"short": "短 / 矮"`) |
| `img` | emoji,**必須對得上字義**。沒有貼切 emoji 時用「概念近似」的 emoji。**禁止用無關 emoji 湊數**(例 `tail` 配 🐲 是錯的)。組合 emoji(像 🛏️🕘)兩個間不加空格 |
| `chunks` | 拆字唸陣列。**所有字必須能拆 2+ 塊**(規則見下方 §3)。真正不規則才用單塊 |
| `py` | 注音腳手架。不求 100% 準,目的是讓學習者敢開口唸。多音節用 `-` 連接(例 `ㄅㄝㄉ-ㄊㄞㄇ`) |
| `split` | 拼讀塊 / 規則文字說明。讓學習者看見每塊用了什麼規則 |
| `theme` | 必須是 `themes.json` 裡存在的 id。見 §4 |
| `stage` | 0-4 整數。決定何時開放(學習者目前在 Stage X 時,只看得到 stage ≤ X 的字) |

### 不可以做的事

- ❌ 不加 `level / first / lastSeen / nextDue / ease / playCount` 等 SRS 欄位 —— 那些是執行時 srs.js 自動加在 localStorage 的,不是 vocab.json 該管的
- ❌ 不要為 vocab.json 創造新的最外層欄位
- ❌ JSON 不要有 trailing comma(JavaScript 嚴格 parser 會炸)

---

## 3. Chunks 拆字唸的詳細規則

(權威來源:`CLAUDE.md`「課程網站架構 → 範本應內含 → chunks」段落)

### 基本拆法
| 字型 | 拆法 | 例 |
|------|------|----|
| 多音節 | 按音節分 | `bedtime` → `["bed","time"]`、`apple` → `["ap","ple"]` |
| 單音節 CVC | onset + rime | `cat` → `["c","at"]`、`dog` → `["d","og"]` |
| 單音節 silent-e | onset + silent-e rime | `cake` → `["c","ake"]`、`rice` → `["r","ice"]` |
| 單音節 vowel team | onset + team rime | `moon` → `["m","oon"]`、`tea` → `["t","ea"]` |
| Blend 起始 | 整 blend + 韻 | `snow` → `["sn","ow"]`、`three` → `["thr","ee"]` |
| Digraph 起始 | digraph + 韻 | `ship` → `["sh","ip"]`、`sheep` → `["sh","eep"]` |
| 無 onset(以母音開頭) | 整塊單塊 | `arm` → `["arm"]`、`ear` → `["ear"]` |

### 「不規則」字也要盡量拆(用 §4 模式)

| 模式 | 例 | 拆法 |
|------|----|------|
| `igh` 含 silent gh | night / light | `["n","ight"]` |
| `eigh` | eight / weight | `["eigh","t"]` |
| soft c (c+e/i/y) | ice / face | `["i","ce"]`、`["f","ace"]` |
| soft g | age / gem | `["a","ge"]`、`["g","em"]` |
| 雙子音 gg/ll/ss/tt | egg / ball | `["e","gg"]`、`["b","all"]` |
| silent kn | know / knife | `["kn","ow"]` |
| silent wr | write / wrap | `["wr","ite"]` |
| silent h(字首)| hour | `["h","our"]` |
| 不規則 ea | bread / friend | `["br","ead"]`、`["fr","iend"]` |
| silent w | two | `["tw","o"]` |

**真的不規則才單塊**:`one`、`eye`、`old`、`earth`、`eat`(這幾個沒清楚 onset/rime 邊界)

---

## 4. Themes 對應(用哪些 theme id)

完整目錄在 `themes.json`。**新字的 `theme` 欄位必須是其中一個 id**。

### 已有主題(寫字時用 id 填 `theme` 欄位)

**daily 日常生活**:`numbers / time / family / body / colors / food / animals / clothing / weather / places / transportation / school / home-items / nature / kitchen-utensils / bathroom / fruits / vegetables / drinks / desserts / shapes / directions`

**actions-feelings 動作與情緒**:`actions / adjectives / emotions / personality / relationships`

**people-jobs 人物與職業**:`jobs / jobs-advanced / appearance`

**entertainment 娛樂與興趣**:`sports / music / toys / art / hobbies / games / movies-tv`

**social 社會與生活**:`travel / shopping / restaurant / money / emergencies / events / environment / crime`

**health 健康與身體**:`health / medical / fitness / diseases`

**tech-media 科技與媒體**:`technology / internet / media`

**business 商業與經濟**:`office / business / economy`

**academic 學術與抽象**:`science / history / geography / politics / law / religion / philosophy / literature / academic-words`

**special 特別**:`phonics-compound / sight-words / idioms`

### 每主題目標字數(粗估)

|  主題類型 | 目標字數 / 主題 |
|----------|----------------|
| 高頻日常(numbers, time, family, body, colors, food...) | 30-50 |
| 一般主題 | 50-150 |
| 大領域(business, science, academic...) | 100-300 |
| sight-words | ~500(Fry 高頻字補完) |
| idioms | ~300-500 |
| academic-words | ~570(AWL 完整) |

---

## 5. 加字優先順序

**單次對話的建議流程**:

1. 開頭讀 §0 那幾個檔案
2. 用 `grep -c '"word":' D:\英\lessons\vocab.json` 看現在多少字
3. 看現有字裡**哪些主題還少於目標**(`grep '"theme":"<id>"' | wc -l`)
4. **選 2-4 個薄弱主題,每個補 50-150 字**(本輪累計 300-500)
5. **照頻率排**:先填高頻字(Oxford 3000 / Fry / GSL 前面)
6. **照階段排**:Stage 0-1 主題填滿之前不要往 Stage 3-4 跳
7. Edit `vocab.json`:在 `words` 陣列的最後一個元素後 append(注意逗號)
8. Commit + push(看 §7)

---

## 6. 品質範例

### ✅ 好的條目
```json
{"word":"car","mean":"汽車","img":"🚗","chunks":["c","ar"],"py":"ㄎㄚㄦ","split":"c + ar (R-controlled)","theme":"transportation","stage":0}
```
- 中文簡潔
- emoji 完全對得上字義
- 拆字遵循 onset + rime 規則
- 注音腳手架
- split 點明用了什麼 phonics 規則
- 主題 + 階段都對

### ❌ 壞的條目(避免)
```json
{"word":"car","mean":"一種有四個輪子的交通工具,用引擎驅動","img":"🚙🚗🚕","chunks":["car"],"py":"car","split":"car","theme":"transport","stage":0}
```
問題:
- 中文太長
- emoji 太多湊數
- chunks 沒拆
- 注音不是注音
- split 沒講規則
- theme id 拼錯(應是 `transportation` 不是 `transport`)

---

## 7. Commit & Push 流程

每次 append 完一批字:

```powershell
Set-Location "D:\英\lessons"
git add vocab.json
git commit -m "vocab: +N 字 (主題A / 主題B / 主題C)"
git push
```

學習者已設好 GitHub Pages(`qingcaila/english-lessons`),push 後 30 秒部署。

**Commit message 規則**:
- 開頭 `vocab:` 表示是字量擴建
- 寫**新增的字數**和**涵蓋的主題**
- 例:`vocab: +250 字 (kitchen-utensils / bathroom / fruits / vegetables)`

---

## 8. 跨對話累積的紀錄

每次對話結束前,在這個檔案末端 append 一筆紀錄:

```markdown
## 累積紀錄
- 2026-05-13 / 對話 1 / +0(本檔案建立,基準 224 字)
- 2026-MM-DD / 對話 N / +XXX 字 / 涵蓋主題 / 累計 YYY
```

讓下次接手 AI 一眼看到進度。

---

## 9. 給接手 AI 的最後三條提醒

1. **不要重新評估學習者程度**(profile.md 第 10 章寫了)。直接執行字量擴建任務。
2. **不要主動提及任何個人識別資訊**(學習者極在意這條)。本任務不需要任何個人資訊。
3. **品質 > 數量**。寧可這次只加 200 個好字,也不要塞 1000 個爛字。Phonics 拆解錯誤、emoji 不對、注音亂寫,**比沒加更糟**(學習者會學到錯的)。

---

## 批次地圖(2026-05-13 學習者確認:依序做完到 10,000+)

每批 300-400 字。**接手的對話 = 找下方第一個未勾選的批次去做**。完成後在批次號旁打勾 `[x]`,並在「累積紀錄」append 一行。

### Stage A:Stage 0-1 日常底盤(741 → 2,100)
- [x] **A1**(+271 / 累計 1,012)numbers 81 / time 80 / colors 55 / animals 100 — 全部超標完成
- [x] **A2**(+239 / 累計 1,251)clothing 54 / weather 60 / food 65 / school 55 / home-items 60 — 全部達標
- [x] **A3**(+224 / 累計 1,475)jobs 55 / sports 54 / music 55 / nature 55 / phonics-compound 55 — 全達標
- [x] **A4**(+146 / 累計 1,621)sight-words 推到 251 — Fry 第二段完成

### Stage B:Stage 1-2 廣度鋪開(2,100 → 4,200)
- [x] **B1**(+193 / 累計 1,814)family 85 / body 99 / emotions 100 / actions 100 — 達標(family 略不到 100 因詞彙密度上限)
- [x] **B2**(+206 / 累計 2,020)adjectives 100 / kitchen-utensils 55 / bathroom 47 / fruits 69 / vegetables 69 — adjectives 達 100,其餘 47-69(因主題詞彙密度上限不易硬塞到 100)
- [x] **B3**(+312 / 累計 2,332)drinks 62 / desserts 58 / shapes 60 / directions 60 / transportation 70 / places 69
- [x] **B4**(+247 / 累計 2,651)travel 63 / shopping 62 / restaurant 63 / money 60 / health 66
- [x] **B5**(+168 / 累計 2,819)sight-words 389(近 400) / technology 47
- [x] **B6**(+160 / 累計 2,958)過去式 60(sight-words) / 片語動詞 60 / 連接副詞 40 — 直接打學習者閱讀斷崖

### Stage C:Stage 2-3 抽象 + 領域(4,200 → 6,500)
- [x] **C1**(+300 / 累計 3,258)jobs-advanced 80 / appearance 59 / personality 80 / relationships 81
- [x] **C2**(+259 / 累計 3,517)toys 69 / art 50 / hobbies 50 / games 50 / movies-tv 50
- [x] **C3**(+399 / 累計 3,916)medical 80 / fitness 77 / diseases 80 / office 80 / business 82
- [ ] **C4**(+~400 / 累計 ~5,800)economy / internet / media / events / environment
- [ ] **C5**(+~400 / 累計 ~6,200)science / history / geography
- [ ] **C6**(+~300 / 累計 ~6,500)emergencies / crime / law(基礎)

### Stage D:Stage 3-4 學術 + 收尾(6,500 → 10,000+)
- [ ] **D1**(+~400 / 累計 ~6,900)politics / religion / philosophy
- [ ] **D2**(+~400 / 累計 ~7,300)literature / sight-words 推到 500(Fry 完成)
- [ ] **D3**(+~400 / 累計 ~7,700)academic-words 1(AWL Sublist 1-3)
- [ ] **D4**(+~400 / 累計 ~8,100)academic-words 2(AWL Sublist 4-6)
- [ ] **D5**(+~400 / 累計 ~8,500)academic-words 3(AWL Sublist 7-10,完成 ~570)
- [ ] **D6**(+~400 / 累計 ~8,900)idioms 1(常見 100 條)
- [ ] **D7**(+~400 / 累計 ~9,300)idioms 2 + phrasal verbs 進階
- [ ] **D8**(+~400 / 累計 ~9,700)抽象詞補完 / 學術領域補漏
- [ ] **D9**(+~300 / 累計 10,000+)收尾 + 看哪些主題還不夠就補

### 批次操作守則
1. 動工前 `git pull`,參考「並行對話協調規則」
2. 一輪只動 2-4 個主題,**不要為了打勾跨多個批次**(品質先)
3. 完成後:(a) 把該批 `[ ]` 改成 `[x]` (b) 累積紀錄 append 紀錄 (c) commit + push
4. 平行對話:從**未勾批次裡跳一段挑**,避撞主題(例如對話 A 做 A1、對話 B 做 A3)
5. 如果學習者實際停在某 Stage 太久,可暫停批次衝刺、改成只補學習者卡的主題

---

## 累積紀錄

- **2026-05-13** / 對話 1(主對話,本檔建立)/ +0 / 基準 224 字
- **2026-05-13** / 對話 2(平行)/ +16 / sight-words / 累計 240
- **2026-05-13** / 對話 1(主對話)/ +196 / kitchen-utensils / bathroom / fruits / vegetables / drinks / desserts / shapes / directions / travel / shopping / restaurant / money / health / technology / 累計 **436**
- **2026-05-13** / 對話 3(平行)/ +305 / actions(74) / adjectives(59) / emotions(48) / sight-words(95) / body(29) / 累計 **741**
- **2026-05-13** / 對話 3(批次 A1)/ +271 / numbers(+71→81) / time(+70→80) / colors(+45→55) / animals(+85→100) / 累計 **1,012**
- **2026-05-13** / 對話 3(批次 A2)/ +239 / clothing(+44→54) / weather(+50→60) / food(+50→65) / school(+45→55) / home-items(+50→60) / 累計 **1,251**
  - 重點:clothing 完整補完(內衣/泳裝/正式服裝/布料);weather 補完天氣現象 + 自然災害;food 走熟食/加工/調味 (避開 fruits/vegetables 已有的部分);school 完整課業流程詞;home-items 涵蓋家具/結構/電器/清潔/格局
  - 下一個:**A3**(jobs / sports / music / nature / phonics-compound 各推到 50)
- **2026-05-13** / 對話 3(批次 A3)/ +224 / jobs(+45→55) / sports(+44→54) / music(+45→55) / nature(+45→55) / phonics-compound(+45→55) / 累計 **1,475**
  - 重點:jobs 涵蓋專業/服務/法律/科技;sports 含團隊球類+個人運動+比賽詞;music 樂器+曲式+音樂家+曲風;nature 地形+水體+礦物+植物部位;phonics-compound 完整 light/snow/fire/eye/foot/hand/book/under/some-/every- 等複合家族
  - 下一個:**A4**(sight-words 推到 250 — Fry 第二段,主要是基本動詞、副詞、形容詞、常用名詞)
- **2026-05-13** / 對話 3(批次 A4)/ +146 / sight-words(+146→251) / 累計 **1,621**
  - 重點:Fry 第二段連接詞(although/though/unless/however/therefore/thus/instead/otherwise) + 空間介系詞(above/below/among/into/onto/against/through/across/along/beyond/toward/throughout/within/without) + 人稱類(people/person/anyone/everybody/anybody/nobody/somebody/mother/father/son/daughter/neighbor/human/adult/teen/citizen/individual/member) + 抽象名詞(thing/way/place/life/world/state/city/town/area/story/fact/idea/problem/example/reason/result/matter/step/rule/plan/system/concept/event/chance/opportunity)
  - 下一個:**B1**(family / body / emotions / actions 各推到 100)
- **2026-05-13** / 對話 3(批次 B1)/ +193 / family(+75→85) / body(+60→99) / emotions(+42→100) / actions(+16→100) / 累計 **1,814**
  - 重點:family 涵蓋祖孫/姻親/繼親/教親/婚姻生死全套;body 補完軀幹四肢肌骨內臟細部;emotions 加入抽象情緒名詞 + 強烈情緒形容詞 + 道德相關;actions 補完選擇/同意/期待類動詞
  - 下一個:**B2**(adjectives / kitchen-utensils / bathroom / fruits / vegetables 各推到 100)
- **2026-05-13** / 對話 3(批次 B2)/ +206 / adjectives(+31→100) / kitchen-utensils(+40→55) / bathroom(+35→47) / fruits(+50→69) / vegetables(+50→69) / 累計 **2,020** ⭐ 突破 2K
  - 重點:adjectives 加聰明/愚笨/簡複/罕奇/光糙;kitchen 補小器具(削皮/打蛋/濾網)和電器(微波/烤箱);bathroom 補化妝品/急救/個人清潔;fruits 走熱帶水果 + 漿果家族;vegetables 走葉菜 + 根莖類 + 香草
  - 下一個:**B3**(drinks / desserts / shapes / directions / transportation / places 各推到 80)
- **2026-05-13** / 對話 3(批次 B3)/ +312 / drinks 62 / desserts 58 / shapes 60 / directions 60 / transportation 70 / places 69 / 累計 **2,332**
  - 重點:drinks 加酒類+咖啡+茶+水類;desserts 跨歐美亞甜點;shapes 補完幾何+測量詞;directions 補方位+轉向+幾何位置;transport 補陸海空+特殊車輛;places 涵蓋商業/宗教/娛樂/行政
  - 下一個:**B4**(travel / shopping / restaurant / money / health 各推到 80)
- **2026-05-13** / 對話 1(主對話,結構擴充)/ **+5 主題 / +72 字** / 累計 **2,404**
  - **新增 5 個主題到 themes.json**(因 52 主題在 10K 字量下會擠;經評估後新增):
    - `materials` 🪨 材料(Stage 2,daily 分類)
    - `tools` 🔨 工具(Stage 2,daily 分類)
    - `countries` 🌍 國家(Stage 1,social 分類)
    - `phrasal-verbs` 🔗 片語動詞(Stage 1,special 分類)— **Stage 1 閱讀斷崖核心**
    - `connectors` 🪢 連接詞(Stage 1,special 分類)— **讀文章必認**
  - 5 個新主題各 12-15 字示範字,讓主題不再是空殼:
    - materials 15 / tools 12 / countries 15 / phrasal-verbs 15 / connectors 15
  - 注意:`countries` 字保留**首字大寫**(專有名詞慣例);`phrasal-verbs` 字含**空格**(例 "get up"),chunks 拆成兩部分
  - 主題總數:**52 → 57**;有單字的主題提升,首頁主題進度將不再有那麼多灰色
  - 下一個:依原計畫,**B4 起點**(travel / shopping / restaurant / money / health 各推到 80)
  - 重點:numbers 完成 11-90 + ordinals + 數學詞 + 量詞;time 完成 days/months/seasons/parts of day + 時態 + 頻率副詞;colors 涵蓋金屬色/寶石色/明度修飾詞;animals 補齊哺乳/鳥/海洋/爬蟲/昆蟲六大類
  - 驗證:JSON 合法、無重複、1012 條全部 7 欄位齊全
  - 下一個:**A2**(clothing / weather / food / school / home-items 各推到 50)
  - 重點:Stage 0-1 高頻動詞 + 形容詞補完、Fry sight-words 推進到 ~105(含 went/saw/said/took/thought/knew 等過去式斷崖關鍵字 + 情態 will/would/could/should/might + 所有人稱代名詞)、body 補內外部位
  - 已驗證:`node -e` parse JSON 合法、無重複字、所有條目 7 欄位齊全、chunks 全部 ≥2 塊
  - **注意 hook 行為**:本輪 Edit vocab.json 後一個 auto-commit hook 自動把改動 commit 成 `aa1dc0e 新增 session 記錄 + 白名單設定`(訊息與內容無關但內容正確且已 push)。後續對話如果想 push 出乾淨的 `vocab: +N` 訊息,可能要先停掉這個 hook,或手動補 commit。
  - **下一輪可補主題**(由高到低,各只 10-19 字):numbers / time / colors / animals / clothing / weather / food / school / home-items / jobs / sports / music / nature / phonics-compound — 都是 Stage 0 高頻日常,目標補到 30-50 字/主題

---

## 並行對話協調規則(2026-05-13 新增)

如果你看到上面累積紀錄裡**有同一日多個對話 push 過字**,代表這個學習者**同時有多個對話視窗在擴字**。動之前必須:

1. `cd D:\英\lessons && git pull` — **強制先抓最新**,避免覆蓋別人的字
2. **不要重寫 vocab.json**,只能用 Edit append 到 `words` 陣列尾端(JSON 注意逗號)
3. 選的主題**避開別的對話正在做的**(看累積紀錄最近幾條的主題清單)
4. push 之前再 `git pull --rebase` 一次保險
5. 完成後**立刻**在累積紀錄 append 新紀錄,讓下個並行對話看到
