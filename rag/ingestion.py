from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from rag.datatype import DataType
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

    def semantic_chunker(self):
        chunker = SemanticChunker(self.embedding_model)
        chunks = chunker.split_text(self.data)
        documents = [Document(page_content=text, metadata={"id": str(i)}) for i, text in enumerate(chunks)]
        return documents

    def build_vectorestore(self, documents):
        vectorstore = FAISS.from_documents(documents, self.embedding_model)
        vectorstore.save_local('faiss_index')

    def process(self):
        if self.data_type == DataType.PDF.value:
            logger.info('Ingesting PDF...')
            self.process_pdf()

        if self.data:
            logger.info('Ingesting SemanticChunker...')
            documents = self.semantic_chunker()
            logger.info(f'Building vectorstore...')
            self.build_vectorestore(documents)

        else:
            logger.error('Ingestion failed.')

        return self.data