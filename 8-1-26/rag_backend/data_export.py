import pandas as pd
import json
from database.chroma import collection  # your existing Chroma init

def export_vectors():
    print("Fetching all vectors from Chroma...")

    data = collection.get(include=["documents", "metadatas"])

    ids = data["ids"]
    documents = data["documents"]
    metadatas = data["metadatas"]

    rows = []

    for i in range(len(ids)):
        rows.append({
            "id": ids[i],
            "chunk_text": documents[i],
            "metadata": metadatas[i]
        })

    df = pd.DataFrame(rows)

    # Save to Excel
    df.to_excel("chroma_vectors.xlsx", index=False)

    # Save to JSON
    with open("chroma_vectors.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    print("✅ Export completed!")
    print("Files created:")
    print(" - chroma_vectors.xlsx")
    print(" - chroma_vectors.json")

if __name__ == "__main__":
    export_vectors()
