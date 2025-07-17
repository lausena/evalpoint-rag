from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS

from rag.chunker import Chunker
from rag.constants import DataType, ChunkingStrategy
from PyPDF2 import PdfReader
from rag.logger import logger



class Ingestion:
    """
    This class is responsible for ingestion steps required for the
    data that will be embedded.
    """
    def __init__(self, data_type, data_path, chunking_strategy, embedding_model=OpenAIEmbeddings()):
        self.data_path = data_path
        self.data_type = data_type
        self.chunking_strategy = chunking_strategy
        self.embedding_model = embedding_model
        self.data = None

    def process_pdf(self):
        text = ""
        pdf_reader = PdfReader(self.data_path)
        for page in pdf_reader.pages:
            text += page.extract_text()

        self.data = text

    def build_vectorestore(self, documents):
        vectorstore = FAISS.from_documents(documents, self.embedding_model)
        vectorstore.save_local('faiss_index')

    def process(self):
        if self.data_type == DataType.PDF.value:
            logger.info('Ingesting PDF...')
            self.process_pdf()

        if self.data:
            logger.info('Ingesting SemanticChunker...')

            documents = None
            if self.chunking_strategy == ChunkingStrategy.SEMANTIC_CHUNKER.value:
                chunker = Chunker(self.chunking_strategy, self.embedding_model, self.data)
                documents = chunker.semantic_chunker()
                logger.info(f'Building vectorstore...')
            # else: TODO other chunking strategies need to be supported here

            if documents:
                self.build_vectorestore(documents)
        else:
            logger.error('Ingestion failed.')

        return self.data