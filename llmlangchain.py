import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

def similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a,b)/ (np.linalg.norm(a) * (np.linalg.norm(b)))

v1 = embeddings.embed_query("I build machines")
v2 = embeddings.embed_query("I have spareparts")
v3 = embeddings.embed_query("The car is fast")

print("machines vs spareparts (similar): ", round(similarity(v1, v2), 2))
print("machines vs car (different): ", round(similarity(v1, v3), 2))