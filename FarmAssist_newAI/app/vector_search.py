import os
import json
import faiss

from sentence_transformers import SentenceTransformer


# ==========================================
# PATH CONFIGURATION
# ==========================================


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


VECTOR_DIR = os.path.join(
    BASE_DIR,
    "vector_db"
)



INDEX_PATH = os.path.join(
    VECTOR_DIR,
    "farmassist.index"
)


METADATA_PATH = os.path.join(
    VECTOR_DIR,
    "metadata.json"
)



# ==========================================
# LOAD FAISS INDEX
# ==========================================


index = faiss.read_index(
    INDEX_PATH
)


# ==========================================
# LOAD METADATA
# ==========================================


with open(
    METADATA_PATH,
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)



documents = data["documents"]

metadata = data["metadata"]



# ==========================================
# LOAD MODEL
# ==========================================


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# ==========================================
# SEMANTIC SEARCH FUNCTION
# ==========================================


def semantic_search(
        query,
        top_k=5
):


    query_embedding = model.encode(
        [query]
    )


    distances, indexes = index.search(
        query_embedding,
        top_k
    )


    results = []


    for i in indexes[0]:


        if i == -1:
            continue


        results.append({

            "score": float(
                distances[0][len(results)]
            ),

            "type":
                metadata[i].get(
                    "type"
                ),

            "details":
                metadata[i],

            "content":
                documents[i]

        })


    return results