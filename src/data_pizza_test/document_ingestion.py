from datapizza.core.vectorstore import VectorConfig
from datapizza.embedders import ChunkEmbedder
from datapizza.embedders.openai import OpenAIEmbedder
from datapizza.modules.parsers.text_parser import TextParser
from datapizza.modules.splitters import NodeSplitter
from datapizza.pipeline import IngestionPipeline
from datapizza.vectorstores.qdrant import QdrantVectorstore
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

vectorstore = QdrantVectorstore(location=":memory:")
embedder = ChunkEmbedder(client=OpenAIEmbedder(api_key=openai_api_key, model_name="text-embedding-3-small"))
vectorstore.create_collection("my_documents",vector_config=[VectorConfig(name="embedding", dimensions=1536)])

pipeline = IngestionPipeline(
    modules=[
        TextParser(),
        NodeSplitter(max_char=1024),
    ],
    vector_store=vectorstore,
    collection_name="my_documents"
)

pipeline.run("sample.pdf")

results = vectorstore.search(query_vector = [0.0] * 1536, collection_name="my_documents", k=5)
print(results)