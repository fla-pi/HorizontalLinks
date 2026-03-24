import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
from sklearn_extra.cluster import KMedoids

# =======================================================
# CONFIG
# =======================================================

LEMMA_VEC_PATHS = {
    "model_1": r"1200_1499_lemma_vectors_w2v.pkl",
    "model_2": r"1500_1699_lemma_vectors_w2v.pkl",
    "model_3": r"1700_1899_lemma_vectors_w2v.pkl",
    "model_4": r"1900_lemma_vectors_w2v.pkl"
}

PERIODS = {
    "1200-1300": {"model": "model_1", "centuries": [1200, 1300]},
    "1400":      {"model": "model_1", "centuries": [1400]},
    "1500":      {"model": "model_2", "centuries": [1500]},
    "1600":      {"model": "model_2", "centuries": [1600]},
    "1700":      {"model": "model_3", "centuries": [1700]},
    "1800":      {"model": "model_3", "centuries": [1800]},
    "1900":      {"model": "model_4", "centuries": [1900]},
}

DATA_PATH = r"C:\Users\fpisc\Documents\semi&mezzo_codit.csv"

BOOT_N = 1000  # numero iterazioni bootstrap

# =======================================================
# LOAD EMBEDDINGS & DATA
# =======================================================

def load_lemma_vectors(path):
    with open(path, "rb") as f:
        d = pickle.load(f)
    return {k.lower(): np.array(v) for k, v in d.items()}

lemma_embeddings = {m: load_lemma_vectors(p) for m,p in LEMMA_VEC_PATHS.items()}

df = pd.read_csv(DATA_PATH, sep=";")
df.columns = df.columns.str.lower()
df["lemma_base"] = df["lemma_base"].str.lower()
df["construction"] = df["construction"].str.lower()
df["cent"] = df["cent"].astype(int)

# =======================================================
# FUNZIONI METRICHE
# =======================================================

def centroid_weighted_dispersion(vectors, centroid, weights):
    if len(vectors) < 2:
        return np.nan
    dists = cosine_distances(vectors, centroid.reshape(1, -1)).flatten()
    return np.average(dists, weights=weights)

def compute_medoid_single_cluster(vectors, lemmas):
    D = cosine_distances(vectors)
    idx = np.argmin(D.mean(axis=1))
    return lemmas[idx], vectors[idx]

def weighted_semantic_dispersion(vectors, weights):
    if len(vectors) < 2:
        return np.nan
    D = cosine_distances(vectors)
    W = np.outer(weights, weights)
    iu = np.triu_indices(len(vectors), k=1)
    return np.sum(D[iu]*W[iu]) / np.sum(W[iu])

def medoid_silhouette_score(vectors, labels, medoids):
    n = len(vectors)
    sil_scores = np.zeros(n)
    for i in range(n):
        cluster_i = labels[i]
        a = cosine_distances(vectors[i].reshape(1,-1), medoids[cluster_i].reshape(1,-1))[0,0]
        b = np.min([cosine_distances(vectors[i].reshape(1,-1), medoids[j].reshape(1,-1))[0,0]
                    for j in range(len(medoids)) if j != cluster_i])
        sil_scores[i] = (b - a)/max(a,b) if max(a,b) > 0 else 0
    return sil_scores.mean()

def compute_metrics_for_df(df_p, emb, period):
    pdata = {}
    for cons in ["mezzo","semi-"]:
        lemmas = df_p[df_p["construction"]==cons]["lemma_base"].unique()
        lemmas = [l for l in lemmas if l in emb]
        if len(lemmas) < 2:
            return None
        vecs = np.vstack([emb[l] for l in lemmas])
        weights = np.array([df_p[df_p["lemma_base"]==l].shape[0] for l in lemmas])
        centroid = np.average(vecs, axis=0, weights=weights)
        pdata[cons] = {
            "vecs": vecs,
            "weights": weights,
            "centroid": centroid,
            "disp_pairwise": weighted_semantic_dispersion(vecs, weights),
            "disp_centroid": centroid_weighted_dispersion(vecs, centroid, weights)
        }
    # distances
    centroid_dist = 1 - cosine_similarity(
        pdata["mezzo"]["centroid"].reshape(1,-1),
        pdata["semi-"]["centroid"].reshape(1,-1)
    )[0,0]
    filler_dist = cosine_distances(pdata["mezzo"]["vecs"], pdata["semi-"]["vecs"]).mean()
    # medoids
    medoids = {}
    for cons in ["mezzo","semi-"]:
        vecs = pdata[cons]["vecs"]
        if len(vecs) <= 3:
            k_opt = 1
        else:
            scores = []
            max_k = int(np.sqrt(len(vecs)))
            for k in range(2, max_k+1):
                km = KMedoids(n_clusters=k, metric="cosine", random_state=42)
                labels = km.fit_predict(vecs)
                ms = medoid_silhouette_score(vecs, labels, km.cluster_centers_)
                scores.append((k,ms))
            k_opt = max(scores, key=lambda x: x[1])[0]
        km = KMedoids(n_clusters=k_opt, metric="cosine", random_state=42)
        labels = km.fit_predict(vecs)
        medoids[cons] = [compute_medoid_single_cluster(vecs[labels==i], list(range(np.sum(labels==i))))[1] for i in range(k_opt)]
    medoid_dist = cosine_distances(np.vstack(medoids["mezzo"]), np.vstack(medoids["semi-"])).mean()
    return {
        "period": period,
        "CentroidDistance": centroid_dist,
        "AvgFillerDistance": filler_dist,
        "AvgMedoidDistance": medoid_dist,
        "Dispersion_mezzo": pdata["mezzo"]["disp_pairwise"],
        "Dispersion_semi": pdata["semi-"]["disp_pairwise"],
        "Dispersion_from_Centroid_mezzo": pdata["mezzo"]["disp_centroid"],
        "Dispersion_from_Centroid_semi": pdata["semi-"]["disp_centroid"],
    }

# =======================================================
# BOOTSTRAP CON TUTTI I LEMMI
# =======================================================

boot_results = []

for period, cfg in PERIODS.items():
    print(f"\n=== BOOTSTRAP {period} ===")
    df_period = df[df["cent"].isin(cfg["centuries"])]
    emb = lemma_embeddings[cfg["model"]]
    if df_period.empty:
        print("  no data → skip")
        continue
    metrics_full = compute_metrics_for_df(df_period, emb, period)
    if metrics_full is None:
        print("  too few lemmas → skip")
        continue
    for i in range(BOOT_N):
        df_sample = df_period.sample(n=len(df_period), replace=True)
        res = compute_metrics_for_df(df_sample, emb, period)
        if res is not None:
            res["iter"] = i
            boot_results.append(res)

df_boot = pd.DataFrame(boot_results)

# =======================================================
# CALCOLO Z-SCORE GLOBALE (TUTTI I PERIODI)
# =======================================================

metrics_cols = ["CentroidDistance","AvgFillerDistance","AvgMedoidDistance",
                "Dispersion_mezzo","Dispersion_semi",
                "Dispersion_from_Centroid_mezzo","Dispersion_from_Centroid_semi"]

summary_list = []
global_mean_std = {}

# calcolo media e std globale per z-score
for col in metrics_cols:
    global_mean_std[col] = (df_boot[col].mean(), df_boot[col].std())

for period, group in df_boot.groupby("period"):
    summary = {"period": period}
    for col in metrics_cols:
        mean = group[col].mean()
        std = group[col].std()
        ci_low = group[col].quantile(0.025)
        ci_high = group[col].quantile(0.975)
        # z-score globale
        global_mean, global_std = global_mean_std[col]
        z = (mean - global_mean)/global_std if global_std>0 else 0
        summary.update({
            f"{col}_mean": round(mean,4),
            f"{col}_std": round(std,4),
            f"{col}_ci_low": round(ci_low,4),
            f"{col}_ci_high": round(ci_high,4),
            f"{col}_z_global": round(z,4)
        })
    summary_list.append(summary)

df_summary = pd.DataFrame(summary_list)

# =======================================================
# PLOT TUTTE LE METRICHE
# =======================================================

for col in metrics_cols:
    plt.figure(figsize=(9,5))
    plt.plot(df_summary["period"], df_summary[f"{col}_mean"], marker="o", label=col)
    plt.fill_between(df_summary["period"],
                     df_summary[f"{col}_ci_low"],
                     df_summary[f"{col}_ci_high"],
                     alpha=0.3)
    plt.title(col)
    plt.ylabel("Value")
    plt.xlabel("Period")
    plt.xticks(rotation=45)
    # aggiunge valore medio arrotondato sul plot
    for i, v in enumerate(df_summary[f"{col}_mean"]):
        plt.text(i, v, f"{v:.4f}", ha='center', va='bottom', fontsize=8)
    plt.tight_layout()
    plt.show()

# =======================================================
# SAVE RESULTS
# =======================================================

df_summary.to_csv("bootstrap_fullsample_zscore_global.csv", index=False)
print(df_summary)
