import json
import os
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


# ==================================================
# PATH CONFIGURATION
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "DATA"
)

VECTOR_DIR = os.path.join(
    BASE_DIR,
    "vector_db"
)

os.makedirs(
    VECTOR_DIR,
    exist_ok=True
)


# ==================================================
# LOAD JSON FILES
# ==================================================

def load_json(filename):

    path = os.path.join(
        DATA_DIR,
        filename
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


markets = load_json(
    "markets.json"
)

schemes = load_json(
    "schemes.json"
)

infrastructure = load_json(
    "infrastructure.json"
)


# ==================================================
# CREATE DOCUMENTS
# ==================================================

documents = []
metadata = []


# ==================================================
# MARKETS
# ==================================================

print("Processing Markets...")

for item in markets:

    text = f"""
    Farmer Direct Market

    District:
    {item['district']}

    Market Name:
    {item['market_name']}

    Number of Shops:
    {item['shops']}

    Working Hours:
    {item['timing']['open']} to {item['timing']['close']}

    Benefit:
    Farmers can directly sell products without middlemen.
    """

    documents.append(text)

    metadata.append({
        "type": "market",
        "market_name": item["market_name"],
        "district": item["district"]
    })


print(f"Markets Added: {len(markets)}")


# ==================================================
# SCHEMES
# ==================================================

print("Processing Schemes...")

scheme_count = 0

for item in schemes:

    description = str(
        item.get(
            "description",
            ""
        )
    ).strip()

    # Skip empty schemes
    if not description:
        print(
            f"Skipping empty scheme: "
            f"{item['scheme_name']}"
        )
        continue

    text = f"""
    Agriculture Government Scheme

    Scheme Name:
    {item['scheme_name']}

    Description:
    {description}

    Beneficiaries:
    {', '.join(item.get('target_users', []))}
    """

    documents.append(text)

    metadata.append({
        "type": "scheme",
        "scheme_name": item["scheme_name"]
    })

    scheme_count += 1


print(f"Schemes Added: {scheme_count}")


# ==================================================
# INFRASTRUCTURE
# ==================================================

print("Processing Infrastructure...")

for item in infrastructure:

    text = f"""
    Agriculture Infrastructure Facility

    Facility:
    {item['facility']}

    District:
    {item['district']}

    Location:
    {item['location']}

    Benefit:
    {item['benefit']}
    """

    documents.append(text)

    metadata.append({
        "type": "infrastructure",
        "facility": item["facility"],
        "district": item["district"]
    })


print(
    f"Infrastructure Added: "
    f"{len(infrastructure)}"
)


# ==================================================
# SUMMARY
# ==================================================

print("\n================================")
print("DOCUMENT CREATION COMPLETED")
print("================================")

print(
    "Total Documents:",
    len(documents)
)


# ==================================================
# LOAD EMBEDDING MODEL
# ==================================================

print("\nLoading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==================================================
# CREATE EMBEDDINGS
# ==================================================

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    show_progress_bar=True
)

embeddings = np.array(
    embeddings,
    dtype="float32"
)


# ==================================================
# NORMALIZE FOR COSINE SIMILARITY
# ==================================================

faiss.normalize_L2(
    embeddings
)


print(
    "Embedding Shape:",
    embeddings.shape
)
# ==================================================
# CREATE FAISS INDEX
# ==================================================

dimension = embeddings.shape[1]

# Fresh index every run
index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print(
    "FAISS Records:",
    index.ntotal
)


# ==================================================
# SAVE FAISS INDEX
# ==================================================

index_path = os.path.join(
    VECTOR_DIR,
    "farmassist.index"
)

faiss.write_index(
    index,
    index_path
)


# ==================================================
# SAVE METADATA
# ==================================================

metadata_path = os.path.join(
    VECTOR_DIR,
    "metadata.json"
)

with open(
    metadata_path,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        {
            "documents": documents,
            "metadata": metadata
        },
        f,
        indent=4,
        ensure_ascii=False
    )


# ==================================================
# FINISH
# ==================================================

print("\n================================")
print("FAISS CREATION COMPLETED")
print("================================")

print("Index File:")
print(index_path)

print("\nMetadata File:")
print(metadata_path)

print(
    "\nTotal Indexed Documents:",
    len(documents)
)

print(
    "FAISS Records:",
    index.ntotal
)
