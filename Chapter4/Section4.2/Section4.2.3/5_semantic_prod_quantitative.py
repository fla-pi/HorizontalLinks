# =========================
# IMPORT
# =========================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from gensim.models import KeyedVectors
from sklearn.cluster import KMeans
from umap import UMAP
from scipy.spatial import ConvexHull

# =========================
# LOAD
# =========================
DATA_PATH = r"Section4.2/2_dataset_clean.csv"
MODEL_PATH = r"itwac_lemma.w2v"

model = KeyedVectors.load_word2vec_format(MODEL_PATH, no_header=True)
df = pd.read_csv(DATA_PATH, sep=";")

df_eval = df[df["Function"] == "half_of_a _whole"]

mezzo = df_eval[df_eval["Cxn"] == "mezzo"]["Base"].unique().tolist()
semi  = df_eval[df_eval["Cxn"] == "semi"]["Base"].unique().tolist()

# =========================
# corrections
# =========================
errori = ['sbilanciato','automatizzato', 'standardizzato', 'rovinato', 'seduto', 'svestito', 'ipotecato', 'schiave', 'rimbambiti', 'crepuscolari', 'sprofondato', 'ipnotizzato', 'paralizzante', 'formalizzato', 'congelato', 'polverizzato', 'rosicchiato', 'addestrati', 'commutato', 'disseccato', 'smantellato', 'militari', 'putrefatto', 'ombreggiato', 'schiccherato', 'appannati', 'decomposto', 'umidi', 'periferiche', 'disgregato', 'carenata', 'sollevata', 'abbassato', 'scappato', 'isola pedonale', 'privatizzato', 'avvolto', 'sbottonato', 'confessato', 'strangolato', 'delinquneziali', 'boscosa', 'inginocchiato', 'masticati', 'mangiato', 'fortificato', 'aperta', 'digerito', 'sode', 'ripetitivi', 'sbucciato', 'concordanze', 'permamenti', 'frantumato', 'asfissiato', 'accecato', 'fracassato', 'reclinato', 'svenuto', 'abbaio', 'ibernato', 'affondato', 'affossato', 'carnivora', 'spiegazzato', 'decollato', 'ingrosso', 'deficienti', 'paludosa', 'arrugginito', 'definitiva', 'Baggio', 'mascherato', 'coagulato', 'Manicone', 'sbranato', 'assopito', 'voltato', 'tappezzato', 'sfasciato', 'rovesciato', 'spennacchiato', 'carbonizzato', 'investito', 'rimbecillito', 'accucciato', 'sussurrato', 'scalastrato', 'cancellato', 'piegato', 'caduto', 'bloccato', 'devastato', 'intontito', 'spopolato']
correzioni = ['sbilanciare', 'automatizzare', 'standardizzare', 'rovinare', 'sedere', 'svestire', 'ipotecare', 'schiavo', 'rimbambito', 'crepuscolare', 'sprofondare', 'ipnotizzare', 'paralizzante', 'formalizzare', 'congelare', 'polverizzare', 'rosicchiare', 'addestrato', 'commutare', 'disseccare', 'smantellare', 'militare', 'putrefatto', 'ombreggiare', 'schiccherare', 'appannato', 'decomporre', 'umido', 'periferico', 'disgregare', 'carenato', 'sollevato', 'abbassare', 'scappare', 'isola pedonale', 'privatizzare', 'avvolto', 'sbottonare', 'confessare', 'strangolare', 'delinquenziale', 'boscoso', 'inginocchiare', 'masticato', 'mangiare', 'fortificare', 'aperto', 'digerito', 'sodo', 'ripetitivo', 'sbucciare', 'concordanza', 'permamente', 'frantumare', 'asfissiare', 'accecare', 'fracassare', 'reclinare', 'svenire', 'abbaio', 'ibernare', 'affondare', 'affossare', 'carnivoro', 'spiegazzare', 'decollare', 'ingrosso', 'deficiente', 'paludoso', 'arrugginito', 'definitivo', 'baggio', 'mascherare', 'coagulare', 'manicone', 'sbranare', 'assopire', 'voltare', 'tappezzare', 'sfasciare', 'rovesciare', 'spennacchiare', 'carbonizzare', 'investire', 'rimbecillire', 'accucciare', 'sussurrare', 'scalastrare', 'cancellare', 'piegare', 'cadere', 'bloccare', 'devastare', 'intontire', 'spopolare']



def apply_corrections(word_list):
    return [correzioni[errori.index(w)] if w in errori else w for w in word_list]

mezzo = apply_corrections(mezzo)
semi  = apply_corrections(semi)

# =========================
# VECTOR BUILD
# =========================
all_words = list(set(mezzo + semi))

vocab = {}
missing = []

for w in all_words:
    if w in model.key_to_index:
        vocab[w] = model.key_to_index[w]
    else:
        missing.append(w)

print("\nOOV:", missing)

X = model[list(vocab.keys())]
words = list(vocab.keys())

# =========================
# UMAP
# =========================
umap_model = UMAP(n_neighbors=15, min_dist=0.1, metric="cosine")
X_umap = umap_model.fit_transform(X)

# =========================
# KMEANS
# =========================
k = 6
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_umap)

# =========================
# DATAFRAME OUTPUT
# =========================
df_out = pd.DataFrame({
    "word": words,
    "cluster": clusters,
    "label": [
        "both" if w in mezzo and w in semi else
        "mezzo" if w in mezzo else
        "semi"
        for w in words
    ]
})

df_out.to_csv("cluster_annotations.csv", index=False)

# =========================
# COLORS
# =========================
colors = []
for w in words:
    if w in mezzo and w in semi:
        colors.append("purple")
    elif w in mezzo:
        colors.append("orangered")
    else:
        colors.append("deepskyblue")

# =========================
# PLOT
# =========================
plt.figure(figsize=(10,7))

# punti
for i in range(len(X_umap)):
    plt.scatter(X_umap[i,0], X_umap[i,1], c=colors[i], s=30)

# convex hull
palette = sns.color_palette("viridis", k)

for c in range(k):
    pts = X_umap[clusters == c]
    if len(pts) >= 3:
        hull = ConvexHull(pts)
        hull_pts = pts[hull.vertices]
        plt.fill(hull_pts[:,0], hull_pts[:,1], alpha=0.1, color=palette[c])

# etichette centrali
N_CENTRALI = 1

for c in range(k):
    idx = np.where(clusters == c)[0]
    pts = X_umap[idx]

    if len(idx) == 0:
        continue

    centroid = pts.mean(axis=0)
    dists = np.linalg.norm(pts - centroid, axis=1)
    closest = dists.argsort()[:N_CENTRALI]

    for i in closest:
        word_idx = idx[i]
        plt.text(
            X_umap[word_idx,0],
            X_umap[word_idx,1],
            words[word_idx],
            fontsize=9,
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.2")
        )

plt.title("Evaluative cxns clustering")
plt.xlabel("UMAP1")
plt.ylabel("UMAP2")
plt.tight_layout()
plt.show()

N_CENTRALI = 10

cluster_top_words = {}

for c in range(k):
    idx = np.where(clusters == c)[0]
    pts = X_umap[idx]

    if len(idx) == 0:
        continue

    centroid = pts.mean(axis=0)
    dists = np.linalg.norm(pts - centroid, axis=1)

    # prendi i 10 più vicini al centro
    closest = dists.argsort()[:N_CENTRALI]

    words_top = [words[idx[i]] for i in closest]
    cluster_top_words[c] = words_top

    print(f"\nCluster {c} — TOP 10 centrali:")
    print(words_top)