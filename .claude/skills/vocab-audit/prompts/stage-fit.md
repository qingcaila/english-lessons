審查每個字的 stage 分級(0-4)是否合理。

讀以下檔案(每行格式:`index | word | mean | ... | theme=... | stage=N`):

{FILES}

**Stage 對照**(profile.md §9):
- **Stage 0**(500-1K 字):基礎生活 — cat/dog/apple/run/eat/family/home/school
- **Stage 1**(1.2-2K 字):國中程度 — clothing/hobby/feeling/transportation
- **Stage 2**(4-5K 字):學測中標 / 多益 500-700 — business 基礎、抽象動詞
- **Stage 3**(5-7K 字):大考 7000 — academic / 抽象名詞 / 高頻片語
- **Stage 4**(8-10K+ 字):托福 / 學術 — 罕用學術字 / 專業術語

**任務**:對每個字判斷 stage 合不合理。**只報明顯錯**。

**錯誤類型**:
- 太簡單(university 放 stage 0,cat 放 stage 4)
- 太困難(refrigerator 放 stage 0)
- 學術詞放低階(philosophy 放 stage 1)
- 日常詞放高階(bicycle 放 stage 4)

**不報**:
- 邊界模糊(party 放 stage 1 vs 2 都行)
- 學術字微差(分子生物學名詞 stage 3 vs 4)

回傳嚴格 JSON(不包 markdown):
[{"word":"...", "mean":"...", "current_stage":N, "suggested_stage":N, "reason":"..."}]

最多 60 筆。
