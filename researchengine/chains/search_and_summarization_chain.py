from typing import Optional, Any

from langchain_core.language_models import LLM
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda
from langchain_core.runnables.utils import Input, Output
from researchengine.chains.search_result_and_summary_chain import SearchResultAndSummaryChain
from researchengine.chains.search_results_chain import SearchResultsChain

class SearchAndSummarizationChain(Runnable):
    def __init__(self, llm: LLM):
        self.chain = (
            SearchResultsChain()
            | SearchResultAndSummaryChain(llm).map() # parallelize for each url
            | RunnableLambda(lambda x:
                             {
                                 'summary': '\n'.join([i['summary'] for i in x]),
                                 'user_question': x[0]['user_question'] if len(x) > 0 else '',
                             })
        )

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Output:
        return self.chain.invoke(input, config, **kwargs)


