---
name: vocab-audit
description: 全字檢查 vocab.json 資料品質的工具集。學習者說「跑檢查」「品質審查」「audit」「全字檢查」「資料品質」「掃一遍」時觸發。檢查 13 項機器規則(秒級)+ 12 項 AI 語義審查(分鐘級)。內建進度追蹤,自動跳過上次跑過且 vocab 沒變動的檢查。
---

# vocab-audit Skill

## 用途

對 `D:\英\lessons\vocab.json`(10,101+ 字)做**真的全字檢查**,涵蓋:

- **Layer 1 機器規則**(快,~5 秒):欄位完整、chunks 合法、theme/stage 合法、重複、base 斷鏈、亂符號、預設 emoji 等 13 項
- **Layer 2 AI 全字語義審查**(慢,~5-10 分鐘):派多 agent 平行掃,每個字至少被 AI 看過一次
- **進度追蹤**:讀 `history.json` 看哪些 check 跑過、vocab 改了沒、要不要重跑

## 觸發語

學習者說以下任一,啟動這個 skill:
- 「跑檢查」「跑審查」「品質檢查」「audit」「掃一遍」「全字檢查」「資料品質」
- 「家族線檢查」(只跑家族潛力 check)
- 「翻譯檢查」(只跑翻譯品質)
- 「看上次檢查狀態」「audit 紀錄」(只讀 history,不跑)

## 主流程

### Step 1:讀 history,判斷現況

**首選做法**:跑 `python .claude/skills/vocab-audit/scripts/show_status.py` 直接看完整狀態表。

或讀原始檔:
```python
import json
h = json.load(open('.claude/skills/vocab-audit/history.json'))
```

`history.json` 結構:
```json
{
  "vocab_hash_current": "sha256...",
  "checks": {
    "L1-fields":     {"last_run": "2026-05-15", "hash": "sha256...", "issues": 0},
    "L1-chunks":     {"last_run": "2026-05-15", "hash": "sha256...", "issues": 0},
    "L2-translation":{"last_run": "2026-05-15", "hash": "sha256...", "issues": 458},
    ...
  }
}
```

判斷邏輯:
- 當前 `vocab.json` 算 hash → 跟 `vocab_hash_current` 比對
- 一樣 → 顯示「上次檢查後 vocab 沒變動」,問要不要強制重跑
- 不一樣 → 找出哪些 check 的 hash 過時了,建議重跑那些

### Step 2:跟學習者確認跑哪些

預設選單:

```
上次完整檢查:2026-05-15
Vocab 自上次檢查:[沒變動 / 變動了 X 字]

要跑哪些 check?
□ L1-all (機器規則 13 項,5 秒)  [上次:0 異常]
□ L2-translation (翻譯品質,7 agent)  [上次:458 issue 已修]
□ L2-family-potential (家族線潛力)  [從未跑過]
□ L2-homophone-potential (易混字潛力)  [從未跑過]
□ L2-emoji-fit (emoji 配字義)  [從未跑過]
□ L2-chunks-phonics (拆字唸正確性)  [從未跑過]
□ L2-pinyin (注音準度)  [從未跑過]
□ L2-stage-fit (stage 分級合理性)  [從未跑過]
□ L2-modernization (中國用語 / 過時詞)  [從未跑過]
□ 全跑(慎用,~30 分鐘)
```

### Step 3:執行對應 check

**Layer 1**:跑 `scripts/run_layer1.py`,印報告。

**Layer 2**:呼叫 `scripts/prepare_layer2.py {check_type}` 切批次,然後派 7 個 agent 平行跑,每個 agent 用 `prompts/{check_type}.md` 當提示。

### Step 4:彙整 + 套用 + 更新 history

1. agent 結果彙整成修正提案
2. 列給學習者確認
3. 套用後跑 `scripts/update_history.py {check_type}` 紀錄這次跑的 hash + issue 數 + report 路徑

## 12 項 Layer 2 AI 檢查項目

| Check ID | 用途 | 建議頻率 |
|---|---|---|
| `L2-translation` | 翻譯語義正確、多義字漏義、不通順 | 大量加字後 |
| `L2-family-potential` | 全字問 AI「這字有家族關係嗎」找漏網衍生詞 | 每次加新字主題後 |
| `L2-homophone-potential` | 全字問 AI「這字會跟誰撞」找漏網同音/易混字 | 每次加新字主題後 |
| `L2-emoji-fit` | emoji 對得上字義嗎 | 第一次跑完就少跑 |
| `L2-chunks-phonics` | chunks 拆法符合 phonics 規則 | 第一次跑完就少跑 |
| `L2-pinyin` | 注音腳手架對應實際發音 | 第一次跑完就少跑 |
| `L2-theme-fit` | theme 分類合理(動詞別放 adjectives) | 大量加字後 |
| `L2-stage-fit` | stage 分級合理(university 不該在 stage 0) | 重新規劃時 |
| `L2-pos-consistency` | 形容詞 mean 加「的」、動詞別變名詞 | 翻譯品質之後跑 |
| `L2-family-note-consistency` | family-note 跟 mean / base 一致 | 家族線擴充後 |
| `L2-modernization` | 中國用語 / 過時詞(視頻→影片、軟件→軟體) | 第一次跑完就少跑 |
| `L2-tip-coverage` | 不規則字漏標 💡 學習提示 | 第一次跑完就少跑 |

## 進度追蹤關鍵

**避免重跑機制**:
- 每個 check 有自己的「跑完當下 vocab.json 的 sha256」
- 重跑前比對 hash,一樣就跳過
- 加新字 → hash 變 → 但其實只有新字要重看,**TODO**:做 per-word hash 達成增量檢查(目前是全 vocab hash,vocab 動一個字就要重跑全部)

**Report 留檔**:
- 每次跑都寫 `reports/{date}-{check_id}.md`
- 內容:跑了幾字、找到幾 issue、修了幾個、agent 用量

## 檔案結構

```
.claude/skills/vocab-audit/
├── SKILL.md              ← 本檔(Claude 入口)
├── README.md             ← 給人看的(可選)
├── history.json          ← 跑過紀錄
├── scripts/
│   ├── run_layer1.py     ← 跑 13 項機器規則
│   ├── prepare_layer2.py ← 切批次 + 印該派幾個 agent
│   ├── update_history.py ← 更新 history.json
│   └── hash_vocab.py     ← 算當前 vocab.json hash
├── prompts/              ← 每個 L2 check 的 AI prompt 模板
│   ├── translation.md
│   ├── family-potential.md
│   ├── homophone-potential.md
│   ├── emoji-fit.md
│   ├── chunks-phonics.md
│   ├── pinyin.md
│   ├── theme-fit.md
│   ├── stage-fit.md
│   ├── pos-consistency.md
│   ├── family-note-consistency.md
│   ├── modernization.md
│   └── tip-coverage.md
└── reports/              ← 每次跑的結果留檔
    └── {date}-{check_id}.md
```

## Sub-skill 範例:只跑家族線潛力

學習者說「跑家族線檢查」:

1. 讀 history 看 L2-family-potential 上次跑時間 + hash
2. 若 vocab hash 沒變 → 跳出「上次 2026-05-15 跑過 0 漏網,vocab 沒變動,要重跑?」
3. 若有變 → 派 7 個 agent,每個用 `prompts/family-potential.md` 掃 1,500 字
4. 收結果 → 列出漏標的家族線
5. 學習者確認 → 套用
6. 更新 history

## 不做什麼

- 不主動跑(學習者沒講就不跑,避免吃 token)
- 不一次全跑 12 項 L2(成本太高,引導學習者選)
- 不靜默套用修正(每次找到 issue 都先列給學習者過目)
