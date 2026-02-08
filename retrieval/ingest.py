import os
import numpy as np
import faiss
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# 🔒 Force-load .env from project root
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# 🔍 DEBUG (leave this temporarily)
print("DEBUG KEY =", os.getenv("GOOGLE_API_KEY"))

client = genai.Client(
    api_key=os.environ["GOOGLE_API_KEY"]
)

docs = open("data/pra_rulebook.txt").read().split("\n\n") + \
open("data/corep_instructions.txt").read().split("\n\n")

def embed(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values
vectors = np.array([embed(d) for d in docs]).astype("float32")

index = faiss.IndexFlatL2(len(vectors[0]))
index.add(vectors)

faiss.write_index(index, "regulations.index")
np.save("regulations.npy", docs)

print("[SUCCESS] Regulatory corpus indexed (Gemini - new SDK)")
