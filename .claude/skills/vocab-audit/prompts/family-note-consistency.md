審查家族線的 `base` + `family-note` 跟 `mean` 是否邏輯一致。

讀以下檔案(只看有 `base=xxx` 的字):

{FILES}

**任務**:對有 base 的字判斷 base / family-note / mean 三者是否互相一致。

**邏輯衝突類型**:
1. **base 拼錯**:base 指向的字根本不該是這個字的家族
   - `went base=run` 應為 `base=go`
2. **family-note 跟 mean 不對應**:
   - mean 是「過去式」但 family-note 寫「進行式」
   - mean 是「複數」但 family-note 寫「比較級」
3. **base 跟 word 詞性對不上**:
   - word 是名詞但 base 寫成形容詞
4. **family-note 用詞太抽象**(違反 CLAUDE.md 白話原則):
   - ❌「過去式」(光名詞)
   - ✅「已經做過的版本(過去式)」
5. **mean 跟 base 中文意思衝突**:
   - mean 是「不規則動詞變過去」但對應的中文翻譯卻不像

**回傳格式**(嚴格 JSON):
[{"word":"...", "mean":"...", "base":"...", "current_note":"...", "issue":"...", "suggested_note":"...?"}]

最多 60 筆。
