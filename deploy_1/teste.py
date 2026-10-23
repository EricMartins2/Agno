from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb

vector_db = ChromaDb(collection="pdf_agent", path="tmp/chromadb", persistent_client=True)
knowledge = Knowledge(vector_db=vector_db)

print("Documentos:", vector_db.client.get_collection("pdf_agent").count())
print(knowledge.search("Grendene receita líquida 2T26"))