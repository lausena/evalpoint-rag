from typing import Optional, Any

from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda
from langchain_core.runnables.utils import Input, Output

from researchengine.web_utils import web_search
NUM_SEARCH_RESULTS_PER_QUERY = 3


class SearchResultsChain(Runnable):
    def __init__(self):
        self.chain = (
            RunnableLambda(lambda x:
                           [
                               {
                                   'result_url': url,
                                   'search_query': x['search_query'],
                                   'user_question': x['user_question']
                               }
                               for url in web_search(web_query=x['search_query'],
                                                     max_results=NUM_SEARCH_RESULTS_PER_QUERY)
                           ])
        )


    def invoke(self, input: Input, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Output:
        return self.chain.invoke(input, config, **kwargs)
