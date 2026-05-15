審查英文單字有沒有「家族線」沒標到。

讀以下檔案(每行格式:`index | word | mean | img | chunks=... | py=... | theme=... | stage=N`,有的會有 `base=xxx` 表已標):

{FILES}

**任務**:對**沒有 base 欄位的字**逐個判斷:這字是不是另一個字的衍生 / 變形?

判斷規則:
1. **不規則動詞過去式 / 過去分詞**(took ← take, eaten ← eat)
2. **拼字變化**:-ing/-ed/-ies/-er/-est(running ← run, studied ← study, cities ← city, biggest ← big)
3. **衍生形容詞 / 副詞 / 名詞**:-ly/-tion/-ment/-ness/-ful/-less/-able/-ive(slowly ← slow, decision ← decide)
4. **職業 / 工具 -er/-or**:teacher ← teach, sailor ← sail
5. **不規則複數**:feet ← foot, children ← child

**不算**(避免假陽性):
- 兩字長得像但語義無關(mother ≠ moth + er, summer ≠ sum + mer)
- 兩字是不同字根的同源字
- 拼字偶合(carpet ← carp + et 是錯的)

**回傳格式**(嚴格 JSON 陣列,不要包 markdown code block):
```
[
  {"word":"...", "base":"原形字", "type":"過去式/-ing/-ly/...", "note":"白話 + 文法名詞當備註"}
]
```

`type` 簡述變化類型,`note` 用大白話 +(文法名詞):
- ✅「已經做過的版本(過去式)」
- ❌「過去式」(對初學者太抽象)

最多回 80 筆。寧缺勿濫,只報你**確定**是家族關係的。
