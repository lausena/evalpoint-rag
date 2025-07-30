from langchain_openai import ChatOpenAI
from pydantic import SecretStr


def get_openai_llm(api_key: SecretStr, model_name: str):
    return ChatOpenAI(
        api_key=api_key,
        model=model_name,
    )