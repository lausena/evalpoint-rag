from rag.ingestion import Ingestion


def handle_rag(question):
    print(question)


    # Ingestion step:
    # 1. Read the proper data format and store data
    # 2. Apply chunking strategy
    ingestion = Ingestion(
        data_type='PDF',
        data_path='resources/pdfs/GEM_Model.pdf',
        chunking_strategy='SemanticChunker')
    data = ingestion.process()
