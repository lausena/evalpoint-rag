import json

from pydantic import SecretStr

from researchengine.llm_utils import get_openai_llm
from dotenv import load_dotenv, find_dotenv
from researchengine.logger import logger
import os

_ = load_dotenv(find_dotenv())

def run(question):
    logger.info(f'{question} .. End.')


    openai_key = SecretStr(os.environ['OPENAI_API_KEY'])
    get_openai_llm(api_key=openai_key, model_name="gpt-4o-mini")

