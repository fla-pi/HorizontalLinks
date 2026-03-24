import os
import torch
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse
from adjustText import adjust_text
import matplotlib.patheffects as PathEffects 
from umap import UMAP

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------

LEMMA_VEC_PATHS = {
    "1200-1499": r"1200_1499_lemma_vectors_w2v.pkl",
    "1500-1699": r"1500_1699_lemma_vectors_w2v.pkl",
    "1700-1899": r"1700_1899_lemma_vectors_w2v.pkl"
}


DATA_PATH = r"2_semi&mezzo_codit.csv"

BUCKETS = {
    "1200-1499": (1200, 1499),
    "1500-1699": (1500, 1699),
    "1700-1899": (1700, 1899)
}

palette = {"mezzo": "#38B3FF", "semi-": "#FD0E0E", "shared": "#7547AD"}

min_vectors_for_umap = 3


# -------------------------------------------------------
# LOAD LEMMA EMBEDDINGS
# -------------------------------------------------------

import pickle
import numpy as np

def load_lemma_vectors(path):
    print("Loading:", path)
    with open(path, "rb") as f:
        d = pickle.load(f)

    # normalize lemma keys
    lemma_vecs = {lemma.lower(): np.array(vec) for lemma, vec in d.items()}
    return lemma_vecs

print("Loading lemma-based embeddings...")
lemma_embeddings = {bucket: load_lemma_vectors(path) 
                    for bucket, path in LEMMA_VEC_PATHS.items()}
print("Done.\n")


# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

df = pd.read_csv(DATA_PATH, sep=";")
df.columns = df.columns.str.lower()

df["lemma_base"] = df["lemma_base"].astype(str).str.lower()
df["construction"] = df["construction"].astype(str).str.lower()
df["cent"] = df["cent"].astype(int)

def assign_bucket(cent):
    for name, (lo, hi) in BUCKETS.items():
        if lo <= cent <= hi:
            return name
    return None

df["cent_bucket"] = df["cent"].apply(assign_bucket)
df = df[df["cent_bucket"].notna()]


# -------------------------------------------------------
# umap + DISPERSION
# -------------------------------------------------------

umap_frames = []
results = []


def plot_cov_ellipse(ax, mean, cov, color, n_std=1.5, alpha=0.2):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]
    w, h = 2 * n_std * np.sqrt(vals)
    ang = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    ell = Ellipse(xy=mean, width=w, height=h, angle=ang, color=color, alpha=alpha)
    ax.add_patch(ell)

centroids_umap = []

for bucket_name in BUCKETS.keys():
    df_bucket = df[df["cent_bucket"] == bucket_name]

    print(f"\n=== Bucket {bucket_name} ===")

    if df_bucket.empty:
        continue

    # Pick the lemma embeddings for this bucket
    emb_dict = lemma_embeddings[bucket_name]

    lemmas = set(df_bucket["lemma_base"])

    # Annotate: shared, mezzo, semi-
    lemmas_mezzo = set(df_bucket[df_bucket["construction"] == "mezzo"]["lemma_base"])
    print("mezzo: ----------------")
    print(lemmas_mezzo)
    lemmas_semi  = set(df_bucket[df_bucket["construction"] == "semi-"]["lemma_base"])
    print("mezzo: ----------------")
    print(lemmas_semi)
    shared = lemmas_mezzo & lemmas_semi

    words = []
    vecs = []
    labels = []

    for lemma in sorted(lemmas):
        if lemma not in emb_dict:
            continue
        label = (
            "shared" if lemma in shared else
            "mezzo"  if lemma in lemmas_mezzo else
            "semi-"  if lemma in lemmas_semi else
            "other"
        )
        words.append(lemma)
        vecs.append(emb_dict[lemma])
        labels.append(label)

    if len(vecs) < min_vectors_for_umap:
        print("  Too few lemma vectors → skip umap")
        continue

    vecs = np.vstack(vecs)
    umap = UMAP(n_neighbors=15, min_dist=0.1, metric="cosine")
    coords = umap.fit_transform(vecs)

    '''
    for i, var in enumerate(umap.explained_variance_ratio_, 1):
        print(f"PC{i}: {var:.4f}") '''

    df_p = pd.DataFrame(coords, columns=["x", "y"])
    df_p["lemma"] = words
    df_p["construction"] = labels
    df_p["bucket"] = bucket_name
    umap_frames.append(df_p)

    # DISPERSION (same logic, now on lemma vectors)
    for constr, target_set in [("mezzo", lemmas_mezzo), ("semi-", lemmas_semi)]:
        found = [l for l in target_set if l in emb_dict]
        if len(found) > 1:
            mat = np.vstack([emb_dict[l] for l in found])
            weights = np.array([
                df_bucket[df_bucket["lemma_base"] == l].shape[0]
                for l in found
            ])

            # centroide pesato
            centroid = np.average(mat, axis=0, weights=weights)

            # cosine distance pesata
            sims = cosine_similarity(mat, centroid.reshape(1, -1)).flatten()
            weighted_disp = np.average(1 - sims)
            centroid = mat.mean(axis=0)
            sims = cosine_similarity(mat, centroid.reshape(1, -1)).flatten()
            dispersion = float(np.mean(1 - sims))
        else:
            dispersion = np.nan

        results.append({
            "bucket": bucket_name,
            "construction": constr,
            "dispersion": dispersion,
            "weighted_dispersion": weighted_disp,
            "n_forms": len(found)
        })

    


    for constr in ["mezzo", "semi-"]:

        found = [
            l for l in df_bucket[df_bucket["construction"] == constr]["lemma_base"].unique()
            if l in emb_dict
        ]

        if len(found) < 2:
            continue

        mat = np.vstack([emb_dict[l] for l in found])

        weights = np.array([
            df_bucket[df_bucket["lemma_base"] == l].shape[0]
            for l in found
        ])

        # centroide pesato nello spazio embedding
        centroid = np.average(mat, axis=0, weights=weights)

        # proiezione umap
        centroid_xy = umap.transform(centroid.reshape(1, -1))[0]

        centroids_umap.append({
            "x": centroid_xy[0],
            "y": centroid_xy[1],
            "construction": constr,
            "bucket": bucket_name
        })


# -------------------------------------------------------
# umap PLOTS (with weighted centroids)
# -------------------------------------------------------

df_p_all = pd.concat(umap_frames, ignore_index=True)
df_p_all["period"] = df_p_all["bucket"]

df_centroids_umap = pd.DataFrame(centroids_umap)

sns.set(style="whitegrid")
g = sns.FacetGrid(
    df_p_all,
    col="period",
    hue="construction",
    palette=palette,
    height=4.5,
    sharex=False,
    sharey=False
)

g.map_dataframe(
    sns.scatterplot,
    x="x", y="y",
    s=40,
    alpha=0.8
)

