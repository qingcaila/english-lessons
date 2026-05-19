# 待辦清單(vocab.json 品質問題)

> 這些是擴字過程中發現但暫時不立刻處理的問題。下個對話可挑來解決。

## chunks 違規(規則:所有字 chunks ≥ 2 塊,真不規則才單塊)

- [ ] **`the`** — 目前 `["the"]`,應改 `["th","e"]` 或視為真不規則保留
- [ ] **`out`** — 目前 `["out"]`,應改 `["o","ut"]`(母音開頭仍可拆,類似 `arm`→`["arm"]` 已是真不規則,但 out 應該拆)

## 工程問題

- [ ] **auto-commit hook 訊息覆寫** — settings.json 裡有 hook 自動把 vocab.json edit 蓋成「help: 新增 §11...」「新增 session 記錄...」之類無關訊息。導致 git log 一半 commit 訊息與內容不符。
  - 排查方向:`cat C:\Users\User\.claude\settings.json` 或 `D:\英\.claude\settings.json` 找 hook 設定
  - 若是學習者刻意設的,保留;若是另一對話亂裝的,停掉

## 主題分布提醒(未到落差層級,只是觀察)

- bathroom 47 / technology 47 / clothing 54 / sports 54 不到 plan 80
  - 自然詞彙密度上限,不要硬塞
  - 可接受為實際完成

---

## 自然發音法 — 待擴充功能(2026-05-13 加入)

> 目前系統已涵蓋 phonics 核心(CVC / silent-e / 母音團 / 子音群 / 雙字母 / R-控制 / 開音節 / 字尾 + 不規則 note)。
> 下列 3 項是進階 phonics 教學常見元素,**架構先記錄**,有需要再實作。

### 1. 拼字訓練(Spelling)— 優先級高

**功能**:聽到字 / 看中文 → 鍵盤輸入或字母塊拼字

**兩種模式**:
- **A. 聽寫**:🔊 唸字 + 中文 → 輸入框打英文
- **B. 字母塊**:可選字母塊 → 拖拉排列(適合觸控)

**需要的新檔**:
- `spell.html` — 拼字練習頁
- `srs.js` 加 `spellCount` 追蹤
- index.html 模式選項加「✏️ 拼字練習」

**整合 SRS**:
- 拼對 → 視為 L4(主動應用)
- 拼錯 → 視為 forgot(很快再來)
- 共用 nextDue / interval

**工作量**:中(用既有 vocab,無需新資料)

---

### 2. 字根字綴(Roots & Affixes)— 優先級中

**功能**:教 Greek / Latin 字根 → 看字根猜字意

**兩種模式**:
- **A. 字根詞典**:50-100 個常用字根 → 列出 vocab.json 中包含該字根的所有字
- **B. 字根組合題**:`bio + logy = ?` 選項題

**需要的新檔**:
- `roots.json` — 字根庫(prefix / root / suffix)
  ```json
  {
    "bio": {"meaning": "生命", "origin": "Greek", "examples": ["biology","biography"]},
    "graph": {"meaning": "寫 / 描繪", "origin": "Greek", "examples": ["photograph","autograph"]}
  }
  ```
- `roots.html` — 字根教學頁
- vocab.json 可選加 `roots` 欄位:`["bio","logy"]`

**整合**:
- 學新字 → 顯示包含的字根
- 字根點擊 → 列同字根的其他字

**工作量**:中(字根表 50-100 條一次性建檔)

---

### 3. 大量閱讀(Extensive Reading)— 優先級低

**功能**:給整段英文,讀完標記陌生字 → 加進 SRS

**兩種來源**:
- **A. 內建分級文章庫**:整合 News in Levels / VOA Slow English / Bookworms
- **B. 自由貼文章**:學習者貼 URL/文字 → 系統解析

**需要的新檔**:
- `read.html` — 閱讀頁
- `reading-articles.json` — 分級文章庫
- 文章內字標記:綠色=L4 / 灰色=未學 / 橘色=該複習

**整合**:
- 文章預先解析 → 標 vocab 命中
- 點字 → tooltip(中文/注音/拆字)
- 「加入待學」→ 進 SRS

**工作量**:**大**(文章版權 / 持續維護)

---

## 實作順序建議

1. **拼字訓練**(最容易、立即有用)
2. **字根字綴**(教學效果強)
3. **大量閱讀**(版權 / 持續性大工)

每個都可以分階段做:先架構框架 + 少量內容,後續慢慢補。

---

## 主對話新加的待辦(2026-05-13 主對話貢獻)

### 內容擴充(2026-05-15 完成 ✓ 部分)

- [x] **家族線 — 不規則動詞**:~~5 字示範~~ → **150+ 字**(過去式 + 過去分詞)✓ 2026-05-15
- [x] **家族線 — 拼字變化**:~~5 字示範~~ → **100+ 字**(-ing/-ed/-ies/-er/-est)✓ 2026-05-15
- [x] **家族線 — 衍生字**:teacher/farmer/programmer/streamer 等 ~80 字 ✓ 2026-05-15
- [x] **家族線 — 副詞/形容詞**:slowly/quickly/healthy/musical 等 ~280 字 ✓ 2026-05-15
- [x] **同音異字 / 同字異義**:77 字 (there/their/they're, to/too/two, lose/loose 等)✓ 2026-05-15
- [x] **phrasal-verbs**:**311 字**(對話 3 完成)
- [x] **connectors**:48 字(基本達標 30-50)

### 內容擴充(2026-05-15 結束狀態)

家族線總計 **1,625 字 / 10,101 = 16.1% 覆蓋率**(2026-05-15 晚上 AI 全字審查後)。剩餘候選大多是真假陽性
(mother≠moth+er, summer≠sum+mer),自動標會錯,留著不處理。

### 資料品質審查(2026-05-15 完成 ✓)

- [x] `full_audit.py` 8 項格式檢查 → 0 異常
- [x] `audit_translations.py` 11 項翻譯品質檢查 → 0 真錯誤
- [x] AI 全字翻譯審查(7 個平行 agent)→ 修 458 字
- [x] 主題標錯修正 → 49 字
- [x] 數字主題視覺修正 → 46 字改純文字

### 2026-05-15 下午+晚上補的(全字 AI 審查)

- [x] 建立 vocab-audit skill(`.claude/skills/vocab-audit/`)+ 進度追蹤 history.json
- [x] L2-emoji-fit AI 全字 → 修 418 字
- [x] L2-modernization 中國用語 → 修 20 字
- [x] L2-pos-consistency 詞性 → 修 196 字
- [x] L2-stage-fit 分級 → 修 260 字
- [x] L2-family-note-consistency 家族邏輯 → 修 167 字(刪 48 個假家族線)
- [x] **L2-family-potential AI 全字**(非規則比對)→ 新增 404 個家族線
- [x] **L2-homophone-potential AI 全字**(非規則比對)→ 新增 157 個易混提示

**今日結束最終覆蓋率**:
- 家族線:10 → **1,625**(16.1%)
- 易混提示:0 → **365**(常見高頻陷阱基本全覆蓋)

### 留待之後低 ROI 不做

- [ ] L2-chunks-phonics(AI 不擅長 phonics 判斷)
- [ ] L2-pinyin(AI 不擅長注音判斷)
- [ ] L2-tip-coverage(vocab 沒對應 `tip` 欄位)

### 2026-05-19 voice 選擇器 + 速度擴充 + UI 修正

延續 5/18 的發音線索,繼續打磨。

**Voice 指示器 + 選擇器**

- [x] lesson.html hint 列加 voice chip:🎤 <名稱> · <品質等級>
  - 顏色分級:綠=高音質 / 橘=增強 / 黃=普通 / 紅=未偵測
  - 點 chip 跳 modal 選擇器,提供 6 個具名 voice + 自動:
    🇺🇸 Samantha / 🇦🇺 Karen / 🇬🇧 Daniel / 🇮🇪 Moira / 🇮🇳 Rishi / 🇿🇦 Tessa
  - 每個有「試聽」按鈕,試聽不選也行
  - 選擇存 localStorage `englessons:voicePref`,跨頁/跨輪記住
- [x] chip 旁加橘色「使用說明」連結 → help.html#voice-setup
  - help.html §11 聲音 h3 加 `id="voice-setup"` 錨點

**iOS Safari 限制誠實面對**

- [x] 排查發現:Apple 把下載的 Premium voice 鎖在系統朗讀功能,
      Web Speech API 拿不到 → 學習者下載 Ava(高音質) 280 MB
      其實在 Safari 用不到。help.html §2 與 §11 改寫為老實版本。
- [x] pickBestVoice 加 en-US 優先(原本按列表順序挑到 Karen 澳洲,
      改成優先 Samantha 美式),過濾音效類 voice(Bad News / Bahh 等)

**速度擴充**

- [x] 速度下拉從 4 段加到 6 段:極慢 0.3 / 超慢 0.45 / 慢 0.6 /
      正常 0.75 / 較快 0.9 / 原速 1.0(預設保持「慢」)
- [x] 速度選擇存 localStorage `englessons:rate`,跨頁/跨輪記住

**UI / Layout 修正**

- [x] 修 iOS WebKit cancel()+speak() bug — September 被砍前音素
      變 "stember"(safeSpeak helper:cancel 後 setTimeout 100ms 再 speak)
- [x] pickBestVoice 正則加「高音質」(iOS 18 把高級改名為高音質,
      原規則只認舊名)
- [x] 卡片 num 欄太窄 — 🔁 + 文字 img(10th/9th/ear 等)互相擠壓
  - grid-template-columns 第 1 欄 30px → calc(40px * fs-scale)
  - 🔁 用 span 包起來 + transform: scale(0.7) 視覺縮小
    (font-size 對 emoji 沒用,scale 才行)
- [x] 加「回到頂部」浮動按鈕(左下,避開右側 ✅/❌)
  - 滾超過 300px 才顯示,點下 smooth scroll

**複習字混合**

- [x] 複習字(🔁)和新字(🆕)從「全部排前面」改成 Fisher-Yates
      shuffle 隨機交錯。每輪重新洗牌。

**多義字 / 多種發音 note 擴充**

- [x] 學習者看到 live 那種「⚠️ 兩種發音」提示有用,問還有哪些
      沒標。掃 150 個常見多義候選 → 寫腳本 `scripts/add_multi_meaning_notes.py`
      curate 補 **129 條 homophone-note**。覆蓋率 365 → **494 / 10101**。
- [x] 學習者問「真的全 1 萬字都掃過了嗎」 → 答案是沒有,只有 150 候選。
      用 vocab-audit skill 跑 **L2-homophone-potential AI 全字掃**:
  - 21 個 batch × 7 個平行 agent,~10 分鐘跑完
  - 7 agent 共回 1,428 筆,去重後 **1,379 唯一候選**
  - 類型分佈:polyseme 786 / confusable 392 / easily-confused 106 / homophone 79 / heteronym 16
  - 學習者選方案 A(全進)→ `scripts/apply_audit_notes.py` 寫入 1,379 筆
  - **最終覆蓋:1,873 / 10,101 = 18.5%**(從 4.9% 跳到 18.5%)
  - report 留檔:`.claude/skills/vocab-audit/reports/20260519-MERGED.json` +
    7 個 agent 個別檔案,將來增量檢查可重用
  - Tier 1 兩種發音(heteronym):read/lead/tear/record/conduct/
    desert/present/object/subject/contest/contract/export/import/
    progress/project/protest/produce/permit/refuse/content/perfect/
    estimate/advocate/alternate/associate/appropriate/frequent/
    intimate/separate/moderate/deliberate 等
  - Tier 2 一字多義:light/spring/bat/bear/check/watch/glass/date/
    match/pen/ring/letter/well/draw/sound/plant/type/file/form/
    ground/last/post/second/mind/kind/fair/safe/cool/fine/patient
    /press/bill/ball/duck/court/volume/club/stamp/stick/swallow/
    trunk/seal/star/pool/pack/point/race/state/still/store/back/
    front/side/line/stage/change/run/pass/turn/play 等
  - 額外:row/wound/use/abuse/house/kid/tip/key/lot/drug/branch/
    case/right/long/short/fan/wave/wing 等

**未做但可選**

- [ ] 把回到頂部按鈕也加到 help.html / quiz.html / validate.html
- [ ] 預生成 mp3 CDN 方案(用 Polly + Cloudflare R2 跳過 iOS Safari
      限制,真正做到 Readle 等級音質)— 目前學習者選 Samantha 接受

### 2026-05-18 發音品質修復 + 文件更新

學習者反映 iPhone 上 September 唸成 "stember"(漏掉開頭 /sɛ/),整體咬字也很糊。

**根因排查 + 修復**

- [x] **iOS WebKit cancel()+speak() 砍前音素 bug** — `stopAll()` 呼叫 `cancel()`
      後立刻 `speak()`,WebKit 沒清乾淨 → 新 utterance 被砍前 100-300ms
  - 加 `safeSpeak()` helper:若引擎還在播,先 cancel + setTimeout 100ms 再 speak
  - 改 `speakWordWithStress` / `speakBase` / `speakChunk` 三處
  - Chrome / Android 無此 bug,延遲無感
- [x] **`pickBestVoice()` 正則漏接 iOS 18 新名稱** — iOS 18 把「高級」改名
      「高音質」,原 regex 只認舊名 → 學習者下載 Ava(高音質)會挑不到
  - regex 加 `高音質`

**新增工具**

- [x] `tts-demo.html` — 月份英文 TTS 試聽比較頁
  - 列出裝置上所有英文 voice(Web Speech API)+ 雲端參考(AWS Polly via
    StreamElements / Google Translate TTS)
  - 12 個月按鈕 + 速度控制
  - 用途:幫學習者 A/B 比較不同 TTS 音質,作為將來是否升級到預生成
    mp3 的決策依據
  - 結論:iOS Safari 擋雲端 endpoint,但本機 Ava 高音質 + 0.6 速度已夠用

**文件同步**

- [x] help.html §2 step 3 — iOS 聲音設定路徑舊版過時
  - 路徑「朗讀內容」→「閱讀與朗讀」(iOS 18+),舊名作為附註
  - 推薦清單從 Siri 聲音/Samantha 高級/Sangeeta 增強 → Ava 高音質/
    Samantha 增強音質/Allison 增強音質
- [x] help.html §11 聲音章節大幅擴寫
  - 5 步驟逐項說明(設定路徑、試聽、下載、重整)
  - 推薦 voice 表(含大小與特色)
  - iOS 18「高級→高音質」改名提醒
  - 補充系統速率滑桿與本網站無關
  - 「完全沒聲音」獨立成小節

**未做但可選的下一步**

- [ ] 預設 rate 從 0.6 → 0.85(學習者表示維持 0.6,因 Ava neural voice
      在低速也清楚,暫不改)
- [ ] 預生成 mp3 CDN 方案(用 Azure / Polly 一次性生 10K 字 mp3 傳
      Cloudflare R2)— 學習者選 Ava 本機 voice 後不需要,先擱置

### 2026-05-15 晚上補的 UX 改動

- [x] 卡片字級可調:topbar 加「字 小/中/大」下拉,3 段:小(1.0×)/中(1.2× 預設)/大(1.4×)
  - emoji 跟字一起放大
  - 狀態存 SRS.settings.fontSize 跨頁/跨輪記住
  - 預設中:打開就舒適閱讀
- [x] 移除 topbar「結束 →」按鈕(下一輪 → 已涵蓋,← 回首頁也行)
- [x] CLAUDE.md / help.html / validate.html 同步
- [x] index.html 載入優化:vocab.json 4.3MB 拖慢主題顯示
  - 拆三階段:localStorage → themes.json(快)→ vocab.json(慢,背景)
  - 主題 tile 100ms 內出現,字數背景補上
  - 加防呆 + 錯誤提示

### 留待之後低 ROI / 進階優化

- [ ] vocab.json minify(`indent=2` → 單行)節省 ~40%(4.3MB → ~2.5MB)
  - 缺點:git diff 難看
- [ ] vocab.json 分檔載入(stage-0.json / stage-1.json...)
  - 只載當前 stage 用到的,更省記憶體
  - 缺點:架構複雜

### 真錯誤修正紀錄(2026-05-15)

13 個真翻錯改掉:niagara(尼加拉瀑布)/ mankind(人類)/ chili(辣椒)/
orphanage(孤兒院)/ oyster(牡蠣)/ snarl(咆哮)/ spade(鏟子)/ 
likelihood(可能性)/ unity(統一)/ withstand(承受)/ heavenly(天堂的)/
sincerity(真誠)/ privacy(隱私)

### 已完成 ✓(對話 3 + 主對話貢獻)

- ✅ 字量達標:**10,101 字**(原訂 10K)
- ✅ 主題系統:**57 個主題 / 10 分類**(52 + 主對話加的 5:materials/tools/countries/phrasal-verbs/connectors)
- ✅ 5 階段下拉 + 不洗資料硬規則
- ✅ 拆字唸 + 點唸計數 + NEW 標籤 + 注音切換
- ✅ 6 種學習模式 + 結束 / 下一輪按鈕
- ✅ 考自己模式(quiz.html)
- ✅ emoji 自評(可選,不強制)
- ✅ **家族線**(lesson.html + quiz.html + 10 示範字)
- ✅ 主題進度漸層條(L1→L5 視覺化 + 排序)
- ✅ L1-L5 解釋卡(首頁底部)
- ✅ 資料品質檢查工具(validate.html)
- ✅ 使用說明 help.html(11 段完整教學)
- ✅ 交接機制(handoffs/ 子資料夾,跨對話協調規則)
- ✅ Stage 切換永遠不洗資料(硬規則 + 記憶系統)

### 系統 / UX 待辦(低優先,等需要再做)

- [ ] **主題進度卡點主題 → 直接進該主題課程**(現在還要回模式選單)
- [ ] **「最常播音的字 Top 10」儀表板區塊**(用 playCount 數據)
- [ ] **跨裝置同步**(目前 localStorage 限單裝置,匯出 JSON 是手動 workaround)
- [ ] **vocab.json 太大優化**:已 192,837 行,載入時間變慢
  - 選項:分檔(stage-0.json / stage-1.json...)/ lazy load / 預先 minify
- [ ] **大量閱讀整合**(已在上面字根字綴 section,排在最低優先)

### 進階 phonics(input-focused 非急,聽多了自然會)

- [ ] **重音 / schwa 標記**(banana 第一音節弱讀)
- [ ] **連音 / linking 提示**("an apple" 唸 anapple)
- [ ] **美音 /t/ flap**(water → wadder)

### 文件 / 教學

- [ ] **profile.md / syllabus.md** 更新到目前 10K 字量現況(舊版仍寫 224 起點)
- [ ] **help.html §5 範例卡片**展示家族線(現在 demo 沒體現新功能)
- [ ] 累積紀錄表新增「對話 1 +10 字 家族線 + UI 系統」紀錄
