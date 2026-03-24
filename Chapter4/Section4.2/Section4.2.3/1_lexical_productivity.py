import os
import pandas as pd
import numpy as np
from collections import Counter

# ---------------------------
# CONFIG
# ---------------------------
INPUT_CSV = r"Section4.2\2_dataset_clean.csv"
OUT_DIR = r"bootstrap_results"
os.makedirs(OUT_DIR, exist_ok=True)

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

GLOBAL_N = 500
POS_N = 150
GENRE_NARRAT_N = 150
GENRE_STAMPA_N = 150
N_ITER = 1000

MEASURES = ["V", "TTR", "HTR", "P", "Entropy"]

POS_MERGE = {
    "adjective": "ADJ",
    "participle_adj": "ADJ",
    "participle_pres_adj": "ADJ"
}

# ---------------------------
# UTILITIES
# ---------------------------
def shannon_entropy(freqs):
    total = sum(freqs.values())
    if total == 0:
        return 0.0
    probs = np.array(list(freqs.values())) / total
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

def productivity_measures(freqs_counter):
    N = sum(freqs_counter.values())
    V = len(freqs_counter)
    hapax = sum(1 for f in freqs_counter.values() if f == 1)

    return {
        "V": V,
        "TTR": V / N if N > 0 else 0.0,
        "HTR": hapax / V if V > 0 else 0.0,
        "P": hapax / N if N > 0 else 0.0,
        "Entropy": shannon_entropy(freqs_counter) if N > 0 else 0.0
    }

def bootstrap_productivity(df_subset, cxn, n_sample, n_iter):
    df_cxn = df_subset[df_subset["Cxn"] == cxn]
    if len(df_cxn) == 0:
        return pd.DataFrame()

    n_draw = min(n_sample, len(df_cxn))
    results = []

    for _ in range(n_iter):
        sample = df_cxn.sample(n=n_draw, replace=True)
        freqs = Counter(sample["Base"])
        measures = productivity_measures(freqs)
        results.append(measures)

    return pd.DataFrame(results)

def summarize_bootstrap(df_boot, label, cxn):
    summary = []
    for m in MEASURES:
        summary.append({
            "label": label,
            "Cxn": cxn,
            "measure": m,
            "mean": df_boot[m].mean(),
            "std": df_boot[m].std()
        })
    return pd.DataFrame(summary)

def run_bootstrap(df_subset, n_sample, label):
    mezzo = bootstrap_productivity(df_subset, "mezzo", n_sample, N_ITER)
    semi = bootstrap_productivity(df_subset, "semi", n_sample, N_ITER)

    summaries = []
    if not mezzo.empty:
        summaries.append(summarize_bootstrap(mezzo, label, "mezzo"))
    if not semi.empty:
        summaries.append(summarize_bootstrap(semi, label, "semi"))

    return pd.concat(summaries, ignore_index=True) if summaries else None

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv(INPUT_CSV, sep=";")

for c in ["Cxn", "Function", "Base", "Pos", "Text_genre"]:
    if c not in df.columns:
        raise ValueError(f"Missing column: {c}")

df_eval = df[df["Function"] == "evaluative"].copy()
df_eval["POS_merged"] = df_eval["Pos"].replace(POS_MERGE)

# ---------------------------
# GLOBAL
# ---------------------------
print("GLOBAL")
global_summary = run_bootstrap(df_eval, GLOBAL_N, "GLOBAL")

if global_summary is not None:
    global_summary.to_csv(os.path.join(OUT_DIR, "global_summary.csv"), index=False)
    print(global_summary)

# ---------------------------
# POS
# ---------------------------
print("POS")
pos_results = []

for pos_label, df_pos in [
    ("ADJ", df_eval[df_eval["POS_merged"] == "ADJ"]),
    ("NOUN", df_eval[df_eval["POS_merged"].str.upper() == "NOUN"])
]:
    if len(df_pos) == 0:
        continue

    res = run_bootstrap(df_pos, POS_N, f"POS_{pos_label}")
    if res is not None:
        pos_results.append(res)

if pos_results:
    pos_summary = pd.concat(pos_results, ignore_index=True)
    pos_summary.to_csv(os.path.join(OUT_DIR, "pos_summary.csv"), index=False)
    print(pos_summary)

# ---------------------------
# GENRES
# ---------------------------
print("GENRES")
genre_results = []

for genre, n_sample in [("NARRAT", GENRE_NARRAT_N), ("STAMPA", GENRE_STAMPA_N)]:
    df_gen = df_eval[df_eval["Text_genre"] == genre]
    if len(df_gen) == 0:
        continue

    res = run_bootstrap(df_gen, n_sample, f"GENRE_{genre}")
    if res is not None:
        genre_results.append(res)

if genre_results:
    genre_summary = pd.concat(genre_results, ignore_index=True)
    genre_summary.to_csv(os.path.join(OUT_DIR, "genre_summary.csv"), index=False)
    print(genre_summary)

