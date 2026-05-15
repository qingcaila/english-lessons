審查英文單字的 theme 主題分類有沒有亂標。

讀以下檔案:

{FILES}

themes.json 主題清單(只列常見錯誤標靶):
- `actions` 動作 / 動詞
- `adjectives` 形容詞
- `animals` 動物
- `food` / `fruits` / `vegetables` / `drinks` / `desserts`
- `body` 身體部位
- `places` 場所
- `numbers` 數字 / 數量詞
- `time` 時間
- `health` 健康 / `medical` 醫療
- `jobs` 職業
- `business` / `technology` / `internet`
- `sight-words` 高頻字
- `phrasal-verbs` 片語動詞
- `connectors` 連接詞
- `academic-words` 抽象學術字

**任務**:對每個字判斷 theme 對不對。**只報明顯錯誤**。

常見錯類型:
1. 動詞被標 `adjectives`(finish/drive 不是形容詞)
2. 數字主題雜入動詞(speed/increase 應 actions)
3. drinks 主題雜入非飲品(pool/dam/dive)
4. animals 主題雜入非動物(motor/clue)
5. 形容詞 mean 結尾「的」但 theme 不是 adjectives

**不報告**:
- 邊界模糊(running 標 actions vs sports 都行)
- 主題標太籠統但不算錯(food vs fruits)

**回傳格式**(嚴格 JSON):
```
[
  {"word":"...", "mean":"...", "current_theme":"...", "suggested_theme":"...", "reason":"..."}
]
```

最多 60 筆。
