from database.chroma import collection

def test_vectors_are_stored():
    count = collection.count()
    assert count > 0
