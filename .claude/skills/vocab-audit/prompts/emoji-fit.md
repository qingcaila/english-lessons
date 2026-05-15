審查英文單字配的 emoji 對不對字義。

讀以下檔案(每行格式:`index | word | mean | img | ...`):

{FILES}

**任務**:對每個字判斷 `img` 欄位的 emoji 配得上 word + mean 嗎?**只報配不上的**。

判斷:
- ✅ 字義跟 emoji 一眼能對上(apple→🍎, run→🏃, happy→😊)
- ❌ 完全不相關(thing→🔵 太抽象)
- ⚠️ 有更直觀的選擇(conditioner→🧴 比 💆 直觀)

**不報告**:
- 抽象概念類(love/hope/idea 配什麼都尷尬)
- 純文字 img(數字 11/20/100/1st 等是故意的文字非 emoji)
- 配得上但你個人覺得有更可愛的 emoji 那種

**回傳格式**(嚴格 JSON):
```
[
  {"word":"...", "mean":"...", "current":"emoji", "suggested":"better emoji", "reason":"..."}
]
```

最多 60 筆。
