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
