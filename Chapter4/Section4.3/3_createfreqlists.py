import os
import pandas as pd
from collections import Counter
import re

# -----------------------------
# PATH CONFIG
# -----------------------------
MORPH_IT = r"morph-it_048.txt"
CSV_IN   = r"2_semi&mezzo_codit.csv"

BUCKET_DIRS = {
    "1200_1499": r"C:\Users\fpisc\Downloads\dataset-train\dataset-train\before-1500",
    "1500_1699": r"C:\Users\fpisc\Downloads\dataset-train\dataset-train\from-1500-to-1700",
    "1700_1899": r"C:\Users\fpisc\Downloads\dataset-train\dataset-train\from-1700-to-1900",
    "1900": r"C:\Users\fpisc\Downloads\dataset-train\dataset-train\after-1900-selected",
}

# -----------------------------
# LOAD morph-it
# -----------------------------
morph = pd.read_csv(
    MORPH_IT, sep="\t", header=None, encoding="latin-1",
    names=["form", "lemma", "morph"]
)
morph["form"] = morph["form"].str.lower()
morph["lemma"] = morph["lemma"].str.lower()

lemma_to_forms = morph.groupby("lemma")["form"].apply(set).to_dict()

# -----------------------------
# LOAD your dataset
# -----------------------------
df = pd.read_csv(CSV_IN, sep=";")
df["form_base"] = df["form_base"].astype(str).str.lower()
df["lemma_base"] = df["lemma_base"].astype(str).str.lower()

all_lemmas = sorted(set(df["lemma_base"]))

# -----------------------------
# TOKENIZER
# -----------------------------
token_pattern = re.compile(r"\b[^\W\d_]+\b", flags=re.UNICODE)

def tokenize(text):
    return token_pattern.findall(text.lower())

# -----------------------------
# PROCESS BUCKETS
# -----------------------------
for bucket, folder in BUCKET_DIRS.items():
    print(f"\n=== Processing bucket {bucket} ===")
    counter = Counter()

    # 1. Count token frequencies in the bucket corpus
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".txt"):
                file_path = os.path.join(root, f)
                # tenta UTF-8
                try:
                    with open(file_path, encoding="utf-8") as t:
                        text = t.read()
                except UnicodeDecodeError:
                    try:
                        # tenta latin-1
                        with open(file_path, encoding="latin-1") as t:
                            text = t.read()
                    except UnicodeDecodeError:
                        # fallback aggressivo
                        with open(file_path, encoding="utf-8", errors="ignore") as t:
                            text = t.read()

                toks = tokenize(text)
                counter.update(toks)

    rows = []

    for lemma in all_lemmas:
        if lemma in lemma_to_forms:
            forms = lemma_to_forms[lemma]
        else:
            # fallback: use your CSV forms
            forms = set(df[df["lemma_base"] == lemma]["form_base"])

        for form in forms:
            freq = counter.get(form, 0)
            rows.append((form, lemma, freq))

    out = pd.DataFrame(rows, columns=["form", "lemma", "freq"])
    out.to_csv(f"{bucket}_forms.csv", index=False, encoding="utf-8")
    print(f"Saved: {bucket}_forms.csv")
