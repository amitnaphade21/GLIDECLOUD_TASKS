from database.chroma import collection

def test_insert_and_fetch():
    text = "FastAPI works well with vector databases"
    doc_id = "pytest-doc-1"

    # Cleanup if already exists
    try:
        collection.delete(ids=[doc_id])
    except:
        pass

    # Insert
    collection.add(
        documents=[text],
        ids=[doc_id]
    )

    # Fetch
    result = collection.get(ids=[doc_id])

    # Assert
    assert result is not None
    assert len(result["documents"]) == 1
    assert result["documents"][0] == text
