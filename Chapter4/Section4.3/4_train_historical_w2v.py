import os
import re
from gensim.models import Word2Vec
from tqdm import tqdm

import os
import shutil
from gensim.utils import simple_preprocess

# ----------------------------
# CONFIG
# ----------------------------
source_dir = r"\dataset-train\dataset-train\after-1900"
target_dir = r"\dataset-train\dataset-train\after-1900-selected"
max_tokens = 13_000_000  # 13 milioni di token

os.makedirs(target_dir, exist_ok=True)

# ----------------------------
# PROCESSING
# ----------------------------
total_tokens = 0

for fname in sorted(os.listdir(source_dir)):
    if not fname.endswith(".txt"):
        continue

    src_path = os.path.join(source_dir, fname)
    with open(src_path, "r", encoding="utf-8") as f:
        text = f.read()
        n_tokens = len(simple_preprocess(text))

    # se aggiungendo questo file superiamo il limite
    if total_tokens + n_tokens > max_tokens:
        # tagliamo il file a quanti token rimangono
        tokens_needed = max_tokens - total_tokens
        words = simple_preprocess(text)[:tokens_needed]
        with open(os.path.join(target_dir, fname), "w", encoding="utf-8") as out_f:
            out_f.write(" ".join(words))
        total_tokens += tokens_needed
        print(f"{fname} tagliato a {tokens_needed} token. Totale={total_tokens}")
        break
    else:
        # copiamo intero file
        shutil.copy2(src_path, target_dir)
        total_tokens += n_tokens
        print(f"{fname} copiato. Totale token={total_tokens}")

print(f"\nFatto! Token totali selezionati: {total_tokens}")

# -----------------------------
# PATH CONFIG
# -----------------------------
BUCKET_DIRS = {
    "1200_1499": r"\dataset-train\dataset-train\before-1500",
    "1500_1699": r"\dataset-train\dataset-train\from-1500-to-1700",
    "1700_1899": r"\dataset-train\dataset-train\from-1700-to-1900",
    "1900": r"\dataset-train\dataset-train\after-1900-selected",
}

OUT_DIR = "w2v_models"
os.makedirs(OUT_DIR, exist_ok=True)

# -----------------------------
# TOKENIZER (italiano storico)
# -----------------------------
token_pattern = re.compile(r"\b[^\W\d_]+\b", flags=re.UNICODE)

def tokenize(text):
    return token_pattern.findall(text.lower())

# -----------------------------
# SENTENCE GENERATOR
# -----------------------------s
def sentence_iterator(folder):
    for root, _, files in os.walk(folder):
        for fname in files:
            if not fname.endswith(".txt"):
                continue

            path = os.path.join(root, fname)
            try:
                text = open(path, encoding="utf-8").read()
            except UnicodeDecodeError:
                text = open(path, encoding="latin-1", errors="ignore").read()

            # frase per frase (fallback semplice)
            for sent in re.split(r"[.!?;\n]", text):
                tokens = tokenize(sent)
                if len(tokens) >= 3:
                    yield tokens

# -----------------------------
# TRAIN MODELS
# -----------------------------
for bucket, folder in BUCKET_DIRS.items():
    print(f"\n=== Training Word2Vec for {bucket} ===")

    sentences = list(sentence_iterator(folder))

    model = Word2Vec(
        sentences = sentences,
        vector_size=200,
        window=5,
        min_count=10,
        sg=1,            
        workers=5,
        epochs = 15
    )


    # save full model
    model_path = os.path.join(OUT_DIR, f"w2v_{bucket}.model")
    model.save(model_path)

    # save vectors only (word → vector)
    vec_path = os.path.join(OUT_DIR, f"w2v_{bucket}.kv")
    model.wv.save(vec_path)

    print(f"Saved model: {model_path}")
    print(f"Saved vectors: {vec_path}")
