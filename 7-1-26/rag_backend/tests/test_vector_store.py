from database.chroma import collection

def test_embedding_creation():
    text = "This is a test chunk for embedding"

    result = collection.add(
        documents=[text],
        ids=["test-id-1"]
    )

    assert result is None  