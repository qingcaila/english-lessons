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
