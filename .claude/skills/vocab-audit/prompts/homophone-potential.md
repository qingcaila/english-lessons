審查英文單字有沒有「同音字 / 易混字」沒標到。

讀以下檔案(每行格式:`index | word | mean | ... | [有易混提示]` 標記表已標):

{FILES}

**任務**:對**沒有 [有易混提示] 的字**判斷:這字會不會跟其他字撞?

判斷規則:

1. **同音字**:發音完全相同但拼字不同(see/sea, hear/here, know/no)
2. **同字異義**:同一字多義可能讓人會錯意(bank=銀行/河岸)
3. **拼字易混**:長很像、學習者容易寫錯(then/than, lose/loose, principal/principle)
4. **過去式撞字**:read 過去式 ㄖㄝㄉ 撞 red、saw 撞 see 過去式
5. **用法易混**:lay/lie, rise/raise, lend/borrow, teach/learn 這種文法陷阱

**只報常見高頻陷阱**,不報冷僻組合(bough/bow 這種就跳過)。

**回傳格式**(嚴格 JSON 陣列,不要包 markdown):
```
[
  {"word":"...", "twin":"撞的字 / 多義拆解", "note":"⚠️ 開頭的易混提示"}
]
```

note 範例:
- 同音:`"⚠️ 同音字:bee 蜜蜂 / be 是、當"`
- 易混:`"⚠️ 易混字:lose 失去(動詞)/ loose 鬆的(形容詞)"`
- 用法:`"⚠️ 易混字:lay 放置(及物,lay-laid-laid)/ lie 躺(不及物,lie-lay-lain)"`

最多回 80 筆。同一對只標一邊也可,我會自動補另一邊。
