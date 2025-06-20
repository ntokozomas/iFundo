import json
import numpy as np
import boto3
import os
import socket

# === CONFIG ===
EMBEDDINGS_FILE = "embeddings.json"
CACHE_FILE = "query_cache.json"


# === OFFLINE CHECK ===
def is_offline():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return False
    except OSError:
        return True


# === COSINE SIMILARITY ===
def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# === LOAD OFFLINE KB ===
with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
    knowledge = json.load(f)


# === LOAD QUERY CACHE ===
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        query_cache = json.load(f)
else:
    query_cache = {}


# === EMBED WITH TITAN OR USE CACHE ===
def get_query_embedding(text):
    if text in query_cache:
        print("🧠 Using cached embedding")
        return query_cache[text]

    if is_offline():
        print("📴 Offline and no cached embedding for this query.")
        return None

    print("⚡ Embedding with Titan...")
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = json.dumps({ "inputText": text })
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=body,
        contentType="application/json"
    )
    result = json.loads(response["body"].read())
    embedding = result["embedding"]

    # Save to cache
    query_cache[text] = embedding
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(query_cache, f, indent=2)

    return embedding


# === MAIN LOGIC ===
query = input("🗣️ Ask something: ").strip()
query_vector = get_query_embedding(query)

if not query_vector:
    print("\n🛑 Sorry, I haven’t learned this one yet. Try again when online.")
    exit()

# Find best match
best_score = -1
best_response = "🤷‍♀️ I don't have a match for that yet."

for entry in knowledge:
    score = cosine_similarity(query_vector, entry["embedding"])
    if score > best_score:
        best_score = score
        best_response = entry["text"]

print(f"\n✅ Best Match:\n{best_response}\n(Similarity Score: {best_score:.4f})")
