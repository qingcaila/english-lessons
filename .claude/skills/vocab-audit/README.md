# vocab-audit Skill

對 `vocab.json`(10K+ 字)做機器規則 + AI 全字審查的 skill。

## 觸發

跟 Claude 講「跑檢查」「audit」「品質審查」「全字檢查」即可,Claude 會自動讀 SKILL.md 走流程。

也可以直接 CLI 跑:

```bash
# Layer 1 機器規則(秒級)
python .claude/skills/vocab-audit/scripts/run_layer1.py

# Layer 2 切批次(印 agent 派發指令)
python .claude/skills/vocab-audit/scripts/prepare_layer2.py family-potential

# 看上次跑的狀態
cat .claude/skills/vocab-audit/history.json
```

## 進度追蹤

`history.json` 紀錄:
- 每個 check 上次跑的時間
- 跑時的 vocab.json hash(用來判斷有沒有變動)
- 找到幾個 issue / 修了幾個
- report 檔路徑

**避免重跑邏輯**:當前 vocab hash 跟某 check 上次跑時 hash 一樣 → 跳過,提示「沒變動」。

## 可選 Check

| Check ID | Layer | 用途 |
|---|---|---|
| L1-all | 1 機器 | 13 項格式 / 完整性 / 重複(秒級) |
| L2-translation | 2 AI | 翻譯品質 |
| L2-family-potential | 2 AI | 找漏網家族線 |
| L2-homophone-potential | 2 AI | 找漏網同音/易混字 |
| L2-emoji-fit | 2 AI | emoji 配字義 |
| L2-theme-fit | 2 AI | 主題分類合理性 |

加新 check:在 `prompts/` 寫 `{check_id}.md`,prompt 模板用 `{FILES}` 佔位給 agent 讀的批次檔。

## 結果留檔

每次跑都產出 `reports/{date}-{check_id}.md`,內含:
- 跑了幾字
- 找到幾 issue
- 套用幾個修正
- 完整 issue 列表

## 不會做什麼

- 不主動跑(學習者沒講就不跑)
- 不一次全跑 12 項 L2(成本太高,引導學習者選)
- 不靜默套用修正(每次找到 issue 都列給學習者過目)
