from rag.ingestion import Ingestion
from rag.logger import logger


def handle_rag(question):
    logger.info(f'Your question: {question}')

    # Ingestion step:
    # 1. Read the proper data format and store data
    # 2. Apply chunking strategy
    ingestion = Ingestion(
        data_type='PDF',
        data_path='resources/pdfs/GEM_Model.pdf',  # TODO - make this a directory for all pdf files
        chunking_strategy='SemanticChunker')
    data = ingestion.process()

    logger.info('End.')
