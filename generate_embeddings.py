import json
import boto3

def embed_query_with_titan(prompt):
    try:
        bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
        body = json.dumps({ "inputText": prompt })
        response = bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            body=body,
            contentType="application/json"
        )
        result = json.loads(response["body"].read())
        return result["embedding"]
    except Exception as e:
        print("❌ Titan embedding failed:", e)
        return None

def split_entries(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    entries = []
    chunks = raw.strip().split("# ")
    for chunk in chunks:
        if not chunk.strip():
            continue
        lines = chunk.strip().split("\n", 1)
        if len(lines) != 2:
            continue
        title = lines[0].strip()
        body = lines[1].strip()
        if not title or not body:
            continue
        entries.append({ "title": title, "text": body })
    return entries

def main():
    entries = split_entries("knowledge_base/offline_knowledge.txt")
    enriched = []
    skipped = 0

    for e in entries:
        prompt = e["title"]
        embedding = embed_query_with_titan(prompt)
        if embedding:
            enriched.append({
                "title": e["title"],
                "text": e["text"],
                "embedding": embedding
            })
        else:
            skipped += 1
            print(f"⚠️ Skipped: {prompt}")

    with open("knowledge_base/embeddings.json", "w", encoding="utf-8") as f:

        json.dump(enriched, f, indent=2)

    print(f"✅ Done. Embedded {len(enriched)} entries. Skipped {skipped}.")

if __name__ == "__main__":
    main()


