import pandas as pd
import numpy as np
from gensim.models import KeyedVectors
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score
from umap import UMAP

# paths
DATA_PATH = r"HorizontalLinks/Chapter4/Section4.2/2_dataset_clean.csv"
MODEL_PATH = r"itwac_lemma.w2v"

# load model
model = KeyedVectors.load_word2vec_format(MODEL_PATH, no_header=True)

# load dataset
df = pd.read_csv(DATA_PATH, sep=";")


df_eval = df[df["Function"] == "evaluative"]

# =========================
# BUILD TYPE LISTS
# =========================
mezzo = df_eval[df_eval["Cxn"] == "mezzo"]["Base"].unique().tolist()
semi  = df_eval[df_eval["Cxn"] == "semi"]["Base"].unique().tolist()

# =========================
# corrections: substitution of participle with full verbs and correction of residual lemmatization errors
# =========================
errori = ['sbilanciato','automatizzato', 'standardizzato', 'rovinato', 'seduto', 'svestito', 'ipotecato', 'schiave', 'rimbambiti', 'crepuscolari', 'sprofondato', 'ipnotizzato', 'paralizzante', 'formalizzato', 'congelato', 'polverizzato', 'rosicchiato', 'addestrati', 'commutato', 'disseccato', 'smantellato', 'militari', 'putrefatto', 'ombreggiato', 'schiccherato', 'appannati', 'decomposto', 'umidi', 'periferiche', 'disgregato', 'carenata', 'sollevata', 'abbassato', 'scappato', 'isola pedonale', 'privatizzato', 'avvolto', 'sbottonato', 'confessato', 'strangolato', 'delinquneziali', 'boscosa', 'inginocchiato', 'masticati', 'mangiato', 'fortificato', 'aperta', 'digerito', 'sode', 'ripetitivi', 'sbucciato', 'concordanze', 'permamenti', 'frantumato', 'asfissiato', 'accecato', 'fracassato', 'reclinato', 'svenuto', 'abbaio', 'ibernato', 'affondato', 'affossato', 'carnivora', 'spiegazzato', 'decollato', 'ingrosso', 'deficienti', 'paludosa', 'arrugginito', 'definitiva', 'Baggio', 'mascherato', 'coagulato', 'Manicone', 'sbranato', 'assopito', 'voltato', 'tappezzato', 'sfasciato', 'rovesciato', 'spennacchiato', 'carbonizzato', 'investito', 'rimbecillito', 'accucciato', 'sussurrato', 'scalastrato', 'cancellato', 'piegato', 'caduto', 'bloccato', 'devastato', 'intontito', 'spopolato']
correzioni = ['sbilanciare', 'automatizzare', 'standardizzare', 'rovinare', 'sedere', 'svestire', 'ipotecare', 'schiavo', 'rimbambito', 'crepuscolare', 'sprofondare', 'ipnotizzare', 'paralizzante', 'formalizzare', 'congelare', 'polverizzare', 'rosicchiare', 'addestrato', 'commutare', 'disseccare', 'smantellare', 'militare', 'putrefatto', 'ombreggiare', 'schiccherare', 'appannato', 'decomporre', 'umido', 'periferico', 'disgregare', 'carenato', 'sollevato', 'abbassare', 'scappare', 'isola pedonale', 'privatizzare', 'avvolto', 'sbottonare', 'confessare', 'strangolare', 'delinquenziale', 'boscoso', 'inginocchiare', 'masticato', 'mangiare', 'fortificare', 'aperto', 'digerito', 'sodo', 'ripetitivo', 'sbucciare', 'concordanza', 'permamente', 'frantumare', 'asfissiare', 'accecare', 'fracassare', 'reclinare', 'svenire', 'abbaio', 'ibernare', 'affondare', 'affossare', 'carnivoro', 'spiegazzare', 'decollare', 'ingrosso', 'deficiente', 'paludoso', 'arrugginito', 'definitivo', 'baggio', 'mascherare', 'coagulare', 'manicone', 'sbranare', 'assopire', 'voltare', 'tappezzare', 'sfasciare', 'rovesciare', 'spennacchiare', 'carbonizzare', 'investire', 'rimbecillire', 'accucciare', 'sussurrare', 'scalastrare', 'cancellare', 'piegare', 'cadere', 'bloccare', 'devastare', 'intontire', 'spopolare']


def apply_corrections(word_list):
    new_list = []
    for w in word_list:
        if w in errori:
            new_list.append(correzioni[errori.index(w)])
        else:
            new_list.append(w)
    return new_list

mezzo = apply_corrections(mezzo)
semi  = apply_corrections(semi)

# =========================
# BUILD VECTOR MATRIX
# =========================
all_words = list(set(mezzo + semi))

vocab = {}
missing = []

for w in all_words:
    if w in model.key_to_index:
        vocab[w] = model.key_to_index[w]
    else:
        missing.append(w)

print("\nOOV words:")
print(missing)

X = model[list(vocab.keys())]
words = list(vocab.keys())

# =========================
# UMAP
# =========================
umap_model = UMAP(n_neighbors=15, min_dist=0.1, metric="cosine", random_state=42)
X_umap = umap_model.fit_transform(X)

# =========================
# SEARCH OPTIMAL K
# =========================
print("\n=== CLUSTER SEARCH ===")

k_values = range(2, 15)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_umap)

    dbi = davies_bouldin_score(X_umap, labels)
    chi = calinski_harabasz_score(X_umap, labels)

    print(f"K={k} | DBI={dbi:.4f} | CHI={chi:.2f}")


    ### REPEAT THE PROCEDURE FOR QUANTITATIVE FILLERS

df = pd.read_csv(DATA_PATH, sep=";")

df_eval = df[df["Function"] == "half_of_a_whole"]

# =========================
# BUILD TYPE LISTS
# =========================
mezzo = df_eval[df_eval["Cxn"] == "mezzo"]["Base"].unique().tolist()
semi  = df_eval[df_eval["Cxn"] == "semi"]["Base"].unique().tolist()

def apply_corrections(word_list):
    new_list = []
    for w in word_list:
        if w in errori:
            new_list.append(correzioni[errori.index(w)])
        else:
            new_list.append(w)
    return new_list

mezzo = apply_corrections(mezzo)
semi  = apply_corrections(semi)

# =========================
# BUILD VECTOR MATRIX
# =========================
all_words = list(set(mezzo + semi))

vocab = {}
missing = []

for w in all_words:
    if w in model.key_to_index:
        vocab[w] = model.key_to_index[w]
    else:
        missing.append(w)

print("\nOOV words:")
print(missing)

X = model[list(vocab.keys())]
words = list(vocab.keys())

# =========================
# UMAP
# =========================
umap_model = UMAP(n_neighbors=15, min_dist=0.1, metric="cosine", random_state=42)
X_umap = umap_model.fit_transform(X)

# =========================
# SEARCH OPTIMAL K
# =========================
print("\n=== CLUSTER SEARCH ===")

k_values = range(2, 15)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_umap)

    dbi = davies_bouldin_score(X_umap, labels)
    chi = calinski_harabasz_score(X_umap, labels)

    print(f"K={k} | DBI={dbi:.4f} | CHI={chi:.2f}")
