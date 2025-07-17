from langchain_experimental.text_splitter import SemanticChunker
from rag.constants import ChunkingStrategy
from langchain.docstore.document import Document
from rag.logger import logger


class Chunker:
    """
    This class is responsible for implementing the chunking strategy
    for data that has been converted into text.
    """
    def __init__(self, chunkingStrategy: ChunkingStrategy, embedding_model: str, text: str):
        self.embedding_model = embedding_model
        self.chunkingStrategy = chunkingStrategy
        self.text = text

    def semantic_chunker(self) -> list[Document]:
        """
        Semantic Chunking tries to detect topic shifts by looking at the similarity
        which is measured by cosine similarity between one sentence and the next.

        :return: List of LangChain Documents split by the Semantic Chunking strategy.
        """
        chunker = SemanticChunker(self.embedding_model)
        chunks = chunker.split_text(self.text)
        documents = [Document(page_content=text, metadata={"id": str(i)}) for i, text in enumerate(chunks)]
        return documents


    def fixed_size_chunking(self, chunk_size=128):
        return [self.text[i:i + chunk_size] for i in range(0, len(self.text), chunk_size)]


    def fixed_size_chunking_with_overlap(self, chunk_size=128, overlap=30):
        chunks = []
        for i in range(0, len(self.text), chunk_size - overlap):
            chunks.append(self.text[i:i + chunk_size])
        return chunks
