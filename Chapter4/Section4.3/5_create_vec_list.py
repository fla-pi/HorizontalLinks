import pandas as pd
import numpy as np
import pickle
from gensim.models import KeyedVectors

MODEL_BINS = {
    "1200_1499": r"w2v_models\w2v_1200_1499.kv",
    "1500_1699": r"w2v_models\w2v_1500_1699.kv",
    "1700_1899": r"w2v_models\w2v_1700_1899.kv",
    "1900": r"w2v_models\w2v_1900.kv"
}

def load_embeddings_w2v(model_path):
    return KeyedVectors.load(model_path, mmap='r')

# ----------------------------------------
# PROCESS BUCKETS
# ----------------------------------------
for bucket, model_path in MODEL_BINS.items():
    print(f"\n=== Building lemma vectors for {bucket} ===")

    wv = load_embeddings_w2v(model_path)

    forms_file = f"{bucket}_forms.csv"
    df = pd.read_csv(forms_file, sep=";")

    lemma_vectors = {}

    for lemma, sub in df.groupby("lemma"):
        weighted = []
        weights  = []

        for _, row in sub.iterrows():
            form = row["form"]
            freq = row["freq"]

            if freq == 0:
                continue
            if form not in wv:
                continue

            weighted.append(wv[form] * freq)
            weights.append(freq)

        if weighted:
            lemma_vec = np.sum(weighted, axis=0) / np.sum(weights)
            lemma_vectors[lemma] = lemma_vec

    with open(f"{bucket}_lemma_vectors_w2v.pkl", "wb") as f:
        pickle.dump(lemma_vectors, f)

    print(f"Saved: {bucket}_lemma_vectors_w2v.pkl")
