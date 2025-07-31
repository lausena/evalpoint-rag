from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda
from langchain_core.runnables.utils import Input, Output
from langchain.schema.output_parser import StrOutputParser
from researchengine.prompts import WEB_SEARCH_PROMPT_TEMPLATE
from researchengine.utils import to_obj
from typing import Optional, Any

NUM_SEARCH_QUERIES = 2

class WebSearchesChain(Runnable):
    def __init__(self, llm):
        self.chain = (
            RunnableLambda(lambda x:
                           {
                               'assistant_instructions': x['assistant_instructions'],
                               'num_search_queries': NUM_SEARCH_QUERIES,
                               'user_question': x['user_question']
                           })
            | WEB_SEARCH_PROMPT_TEMPLATE
            | llm
            | StrOutputParser()
            | to_obj
        )

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Output:
        return self.chain.invoke(input, config, **kwargs)

