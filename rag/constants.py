from enum import Enum

class DataType(Enum):
    PDF = 'PDF'
    TEXT = 'TEXT'
    S3 = 'S3'


class ChunkingStrategy(Enum):
    SEMANTIC_CHUNKER = 'SemanticChunker'
    FIXED_CHUNKER = 'FixedChunker'
    FIXED_CHUNKER_WITH_OVERLAP = 'FixedChunkerWithOverlap'