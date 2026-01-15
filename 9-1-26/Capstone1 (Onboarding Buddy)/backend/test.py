from dotenv import load_dotenv
load_dotenv()

from vector.pinecone_client import index

print(index.describe_index_stats())
