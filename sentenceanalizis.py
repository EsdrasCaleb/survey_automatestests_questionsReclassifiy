import json
import pandas as pd

from sentence_transformers import SentenceTransformer

from sklearn.cluster import KMeans
from sklearn.metrics import (
    adjusted_rand_score,
    silhouette_score
)

from collections import Counter


# =========================
# LOAD DATA
# =========================

df = pd.read_csv("finalrmarks.csv")

with open("gemini_output.json") as f:
    gemini = json.load(f)


responses = df.iloc[:, 0].tolist()

themes = gemini["themes"]

theme_to_id = {
    theme: i
    for i, theme in enumerate(themes)
}


llm_labels = [
    theme_to_id[a["theme"]]
    for a in gemini["assignments"]
]


# =========================
# EMBEDDINGS
# =========================

print("Loading embeddings model...")

model = SentenceTransformer(
    "sentence-transformers/all-mpnet-base-v2"
)

embeddings = model.encode(
    responses,
    show_progress_bar=True
)


# =========================
# CLUSTERING
# =========================

k = len(themes)

print(f"Clustering with K={k}")

kmeans = KMeans(
    n_clusters=k,
    random_state=42,
    n_init="auto"
)

cluster_labels = kmeans.fit_predict(
    embeddings
)


# =========================
# METRICS
# =========================

ari = adjusted_rand_score(
    llm_labels,
    cluster_labels
)

silhouette = silhouette_score(
    embeddings,
    cluster_labels
)


# =========================
# DIVERGENCES
# =========================

divergences = []

for i in range(len(responses)):

    if llm_labels[i] != cluster_labels[i]:

        divergences.append({
            "id": i,
            "llm_theme": themes[llm_labels[i]],
            "cluster": cluster_labels[i],
            "response": responses[i]
        })


# =========================
# REPORT
# =========================

print("\n===== RESULTS =====")

print(f"Responses: {len(responses)}")
print(f"Themes: {k}")

print(f"\nARI: {ari:.3f}")
print(f"Silhouette: {silhouette:.3f}")

print(
    f"\nDivergences: "
    f"{len(divergences)} "
    f"({100*len(divergences)/len(responses):.1f}%)"
)


print("\nCluster distribution:")

dist = Counter(cluster_labels)

for cluster_id, count in sorted(
    dist.items()
):
    print(
        f"Cluster {cluster_id}: "
        f"{count}"
    )


# =========================
# SAVE DIVERGENCES
# =========================

pd.DataFrame(
    divergences
).to_csv(
    "divergences.csv",
    index=False
)


print(
    "\nSaved: divergences.csv"
)