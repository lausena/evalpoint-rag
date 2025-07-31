from typing import Optional, Any

from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.utils import Input, Output

from researchengine.utils import to_obj
from researchengine.prompts import (
    ASSISTANT_SELECTION_PROMPT_TEMPLATE
)
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

class AssistantInstructionsChain(Runnable):
    def __init__(self, llm):
        self.chain = (
            {'user_question': RunnablePassthrough()}
            | ASSISTANT_SELECTION_PROMPT_TEMPLATE
            | llm
            | StrOutputParser()
            | to_obj
        )

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Output:
        return self.chain.invoke(input, config, **kwargs)