"""算 vocab.json 的 sha256,用來判斷有沒有變動"""
import hashlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'vocab.json'))

def hash_vocab():
    with open(VOCAB, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def hash_per_word():
    """算每個字的個別 hash,用於增量檢查"""
    import json
    with open(VOCAB, 'r', encoding='utf-8') as f:
        data = json.load(f)
    out = {}
    for w in data['words']:
        s = repr(sorted(w.items()))
        out[w['word']] = hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]
    return out

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'per-word':
        import json
        out = hash_per_word()
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(hash_vocab())
