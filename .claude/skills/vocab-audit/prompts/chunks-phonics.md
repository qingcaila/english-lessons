審查 chunks(拆字唸塊)拆法是否符合 phonics 規則。

讀以下檔案(每行格式:`index | word | mean | img | chunks=[...] | py=... | ...`):

{FILES}

**任務**:對每個字判斷 chunks 拆得對不對。

**規則**(依據 CLAUDE.md):
- 多音節 → 按音節分(bedtime → [bed, time])
- 單音節 + blend/digraph → 起始輔音群 + 韻(snow → [sn, ow], sheep → [sh, eep], three → [thr, ee])
- 單音節 CVC → onset + rime(cat → [c, at], dog → [d, og])
- 單音節 + silent-e → onset + silent-e rime(cake → [c, ake])
- 單音節 + vowel team → onset + team rime(moon → [m, oon])
- 真不規則才寫單塊(one, two, eight, ice, eye, ear, arm, egg)

**只報拆錯的**:
- 拆塊邊界錯(`["bro","ther"]` 應為 `["br","other"]`)
- 該拆沒拆(多音節字只有 1 塊)
- 不該拆卻拆了(真不規則被切兩塊)
- blend/digraph 切錯(`["s","now"]` 應為 `["sn","ow"]`)

**不報**:
- 多種拆法都合理只是風格不同
- 拆得不漂亮但不違規

回傳嚴格 JSON(不包 markdown):
[{"word":"...", "current":["x","y"], "suggested":["a","b"], "reason":"..."}]

最多 80 筆。
