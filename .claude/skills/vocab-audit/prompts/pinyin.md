審查注音(`py` 欄位)是否反映實際英文發音,**並標出弱讀(schwa /ə/)位置**。

讀以下檔案(每行格式:`index | word | mean | img | chunks=... | py=... | ...`):

{FILES}

**任務**:對每個字判斷 py 注音腳手架是否準確,並檢查弱讀位置。

**注音規則**:
- 用注音符號粗略模擬英文發音
- 音節用 `-` 分隔(bedtime → ㄅㄝㄉ-ㄊㄞㄇ)
- 多種發音字標斜線(read → ㄖㄧㄉ / ㄖㄝㄉ)
- **schwa /ə/ 一律用 ㄜ**(這是教學重點 — 學習者要看到「這音節要輕讀」)

**該報的問題類型(按嚴重度排序)**:

1. **完全唸錯**(嚴重):
   - beat → ㄎㄚㄊ(子音都錯)
   - eight → ㄝㄍ(t 沒標,gh 該不發音)

2. **母音類型錯**:
   - beat 用短 ㄧ(該長 ㄧ)
   - cat 用 ㄝ(該 ㄚ 或 ㄟ)

3. **子音類型錯**:
   - sing 用 ㄒ(該 ㄙ 起頭)
   - water 沒體現中間 /t/ 美音 flap(可選但建議)

4. **跟 chunks 不一致**:chunks 拆 3 音節但 py 只給 2 音節

5. **schwa 漏標(教學重點)**:
   - banana 標 ㄅㄚ-ㄋㄚ-ㄋㄚ → 該 **ㄅㄜ**-ㄋㄚ-**ㄋㄜ**(第 1, 3 音節是弱讀)
   - about 標 ㄚ-ㄅㄠㄊ → 該 **ㄜ**-ㄅㄠㄊ(第 1 音節 schwa)
   - computer 標 ㄎㄚㄇ-... → 該 **ㄎㄜㄇ**-ㄆㄧㄨ-ㄊㄜ(第 1 音節 schwa)
   - problem 標 ...-ㄅㄌㄝㄇ → 該 ...-**ㄅㄌㄜㄇ**(第 2 音節 schwa)
   - 規則:多音節字裡,非重音音節的母音通常該是 ㄜ
   - 特別注意 -tion / -sion / -er / -or / -ar 結尾(常 schwa)
   - 介系詞 of, to, for, from 在快讀時也是 schwa(但單字卡片可標重讀版)

6. **重要不規則沒提示**:silent letter 沒在 py 反映(eight 標 ㄟㄍㄊ 不對,該 ㄟㄊ)

**不報**(避免噪音):
- 用 ㄙ 或 ㄗ 模擬 th 的風格爭議(thank → ㄙㄢㄎ vs ㄗㄤㄎ 都接受)
- 用 ㄈ 或 ㄋ 模擬 -ng 結尾的爭議
- 單音節字裡 ㄜ vs ㄝ 差一點(只有多音節 schwa 弱讀位置才報)

回傳嚴格 JSON(不包 markdown):
```
[
  {
    "word": "banana",
    "current": "ㄅㄚ-ㄋㄚ-ㄋㄚ",
    "suggested": "ㄅㄜ-ㄋㄚ-ㄋㄜ",
    "type": "schwa",
    "reason": "第 1、3 音節是弱讀 schwa,該用 ㄜ"
  }
]
```

`type` 取以下之一:
- `error` — 完全唸錯
- `vowel` — 母音類型錯
- `consonant` — 子音類型錯
- `chunks-mismatch` — 跟 chunks 對不上
- `schwa` — 弱讀位置該用 ㄜ
- `silent-missing` — 漏標 silent letter

最多 80 筆。寧缺勿濫,真該改才報。schwa 優先抓常見高頻字(banana, computer, about, problem, America, family, doctor, water 等)。
