from typing import Optional, Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda, RunnableParallel
from langchain_core.runnables.utils import Input, Output

from researchengine.prompts import SUMMARY_PROMPT_TEMPLATE
from researchengine.web_utils import web_scrape

RESULT_TEXT_MAX_CHARS = 10_000

class SearchResultAndSummaryChain(Runnable):
    def __init__(self, llm):
        self.chain = (
            RunnableLambda(lambda x:
                           {
                               'search_result_text': web_scrape(url=x['result_url'])[:RESULT_TEXT_MAX_CHARS],
                               'result_url': x['result_url'],
                               'search_query': x['search_query'],
                               'user_question': x['user_question']
                           })
            | RunnableParallel(
            {
                'text_summary': SUMMARY_PROMPT_TEMPLATE
                | llm
                | StrOutputParser(),
                'result_url': lambda x: x['result_url'],
                'user_question': lambda x: x['user_question']
            })
            | RunnableLambda(lambda x:
                             {
                                 'summary': f"Source Url: {x['result_url']}\nSummary: {x['text_summary']}",
                                 'user_question': x['user_question']
                             })
        )

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Output:
        return self.chain.invoke(input, config, **kwargs)


