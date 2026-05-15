審查不規則字是否漏標 phonics 學習提示(💡)。

讀以下檔案:

{FILES}

**任務**:找出哪些字應該要有 💡 學習提示但沒標。

**判斷標準**(看 word 跟 py 注音):
1. **silent letter**(不發音的字母)
   - know(k 不發音)、knife(k 不發音)、wrong(w 不發音)、psychology(p 不發音)
   - climb(b 不發音)、debt(b 不發音)、doubt(b 不發音)
   - listen(t 不發音)、castle(t 不發音)、receipt(p 不發音)
2. **不規則發音**:
   - women(唸 /wɪmɪn/)、busy(唸 /bɪzi/)、build(短 i)
   - friend(唸 /frɛnd/,ie 唸 ㄝ)
   - colonel(唸 /kɝnəl/)、recipe(唸 /rɛsəpi/)
3. **重音特殊**:
   - photograph 重音在第 1 / photographer 重音在第 2
   - record(名/動詞重音不同)
4. **同字異唸**:
   - read 現在式 ㄖㄧㄉ / 過去式 ㄖㄝㄉ
   - tear 撕 ㄊㄝㄜ / 眼淚 ㄊㄧㄜ
   - bow 鞠躬 ㄅㄠ / 弓 ㄅㄛ
5. **音節重音變化** / R-控制 / schwa 等罕見

**只報「真的不規則但 mean / py 沒提示」的字**。

注意:目前我們沒有 `tip` 欄位,所以這個 check 主要是**列出建議該加 tip 的字清單**,給未來功能擴充用。

回傳嚴格 JSON:
[{"word":"...", "py":"...", "tip_type":"silent letter/不規則發音/重音/同字異唸", "suggested_tip":"...", "reason":"..."}]

最多 80 筆。
