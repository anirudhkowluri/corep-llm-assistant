import os
import faiss
import numpy as np
from google import genai

client = genai.Client(
    api_key=os.environ["GOOGLE_API_KEY"]
)

index = faiss.read_index("regulations.index")
docs = np.load("regulations.npy", allow_pickle=True)

def retrieve(query, k=3):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )
    emb = response.embeddings[0].values

    D, I = index.search(np.array([emb]).astype("float32"), k)
    return [docs[i] for i in I[0]]

