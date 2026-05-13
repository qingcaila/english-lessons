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
