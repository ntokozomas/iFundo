import json

# Load your full Titan knowledge base
with open("offline_embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Format: keep only the text (body) + embedding (which was based on title)
formatted = []
for entry in data:
    if "text" in entry and "embedding" in entry:
        formatted.append({
            "text": entry["text"],
            "embedding": entry["embedding"]
        })

# Save the formatted version
with open("embeddings.json", "w", encoding="utf-8") as f:
    json.dump(formatted, f, indent=2)

print(f"✅ Saved {len(formatted)} formatted entries to embeddings.json")
