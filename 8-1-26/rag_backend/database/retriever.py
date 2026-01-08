from database.chroma import collection

def search_chunks(query: str, top_k: int = 5):
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    hits = []
    for i in range(len(results["documents"][0])):
        hits.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i] if results["metadatas"] else None,
            "score": results["distances"][0][i]
        })

    return hits
