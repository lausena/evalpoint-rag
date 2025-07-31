from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from researchengine.chains.assistant_instructions_chain import AssistantInstructionsChain
from researchengine.chains.search_and_summarization_chain import SearchAndSummarizationChain
from researchengine.chains.search_result_and_summary_chain import SearchResultAndSummaryChain
from researchengine.chains.search_results_chain import SearchResultsChain
from researchengine.chains.web_searches_chain import WebSearchesChain
from researchengine.llm_utils import get_openai_llm
from dotenv import load_dotenv, find_dotenv
from researchengine.logger import logger
from pydantic import SecretStr
import os

from researchengine.prompts import RESEARCH_REPORT_PROMPT_TEMPLATE
from researchengine.utils import to_obj

_ = load_dotenv(find_dotenv())

NUM_SEARCH_RESULTS_PER_QUERY = 2

def run(question):
    openai_key = SecretStr(os.environ['OPENAI_API_KEY'])
    llm = get_openai_llm(api_key=openai_key, model_name="gpt-4o-mini")

    web_research_chain = (
        AssistantInstructionsChain(llm=llm)
        | WebSearchesChain(llm=llm)
        | SearchAndSummarizationChain(llm=llm).map() # parallelize for each web search
        | RunnableLambda(lambda x:
                         {
                             'research_summary': '\n\n'.join([i['summary'] for i in x]),
                             'user_question': x[0]['user_question'] if len(x) > 0 else ''
                         })
        | RESEARCH_REPORT_PROMPT_TEMPLATE
        | llm
        | StrOutputParser()
    )

    web_research_report = web_research_chain.invoke(question)
    print(web_research_report)




    # # # Search Results Chain
    # logger.info("Preparing search results chain")
    # search_results_chain = SearchResultsChain()
    # result_urls_list = search_results_chain.invoke(web_searches)
    # print(result_urls_list)

    # # test chain invocation
    # result_url_str = '{"result_url": "https://citiesandattractions.com/spain/astorga-spain-uncovering-the-jewels-of-a-hidden-spanish-gem/", "search_query": "Astorga Spain attractions", "user_question": "What can I see and do in the Spanish town of Astorga?"}'
    # result_url_dict = to_obj(result_url_str)
    #
    # search_text_summary = SearchResultAndSummaryChain(llm=llm).invoke(result_url_dict)
    # print(search_text_summary)






    # web_search_str = '{"search_query": "Astorga Spain attractions", "user_question": "What can I see and do in the Spanish town of Astorga?"}'
    # web_search_dict = to_obj(web_search_str)
    # print(web_search_dict)
    # result_urls_list = SearchResultsChain().invoke(web_search_dict)
    # print(result_urls_list)





    # assistant_selection_prompt = ASSISTANT_SELECTION_PROMPT_TEMPLATE.format(user_question=question)
    # assistant_instructions = llm.invoke(assistant_selection_prompt)
    #
    # assistant_instructions_dict = to_obj(assistant_instructions.content)
    # # print(assistant_instructions_dict)
    #
    # # Execute prompt to generate web searches based on the user research question
    # web_search_prompt = WEB_SEARCH_PROMPT_TEMPLATE.format(
    #     assistant_instructions=assistant_instructions_dict['assistant_instructions'],
    #     num_search_queries=NUM_SEARCH_QUERIES,
    #     user_question=assistant_instructions_dict['user_question']
    # )
    #
    # web_search_queries = llm.invoke(web_search_prompt)
    # web_search_queries_dict = to_obj(web_search_queries.content.replace('\n', ''))
    # # print(web_search_queries_dict)
    #
    # searches_and_result_urls = [
    #     {
    #         'result_urls': web_search(
    #             web_query=wg['search_query'],
    #             max_results=NUM_SEARCH_RESULTS_PER_QUERY
    #         ),
    #         'search_query': wg['search_query']
    #     }
    #     for wg in web_search_queries_dict
    # ]
    #
    # # print(searches_and_result_urls)
    #
    # # Flatten the results so each dict contains a search query and just one result URL
    # search_query_and_result_url_list = []
    # for qr in searches_and_result_urls:
    #     search_query_and_result_url_list.extend([
    #         {
    #             'search_query': qr['search_query'],
    #             'result_url': r
    #         }
    #         for r in qr['result_urls']
    #     ])
    #
    # # print(search_query_and_result_url_list)
    #
    # # Start scraping the web pages linked to these URLs
    # result_text_list = [{'result_text': web_scrape(url=re['result_url'])[:RESULT_TEXT_MAX_CHARS],
    #                      'result_url': re['result_url'],
    #                      'search_query': re['search_query']}
    #                     for re in search_query_and_result_url_list]
    #
    # print(result_text_list)
    #
    # # Summarizing the web results:
    # result_text_summary_list = []
    # for rt in result_text_list:
    #     summary_prompt = SUMMARY_PROMPT_TEMPLATE.format(
    #         search_result_text=rt['result_text'],
    #         search_query=rt['search_query']
    #     )
    #
    #     text_summary = llm.invoke(summary_prompt)
    #
    #     result_text_summary_list.append({
    #         'text_summary': text_summary,
    #         'result_url': rt['result_url'],
    #         'search_query': rt['search_query']
    #     })
    #
    # # Generating the research report:
    # stringified_summary_list = [f'Source URL: {sr["result_url"]}\nSummary: {sr["text_summary"]}'
    #                             for sr in result_text_summary_list]
    # appended_result_summaries = '\n'.join(stringified_summary_list)
    #
    # research_report_prompt = RESEARCH_REPORT_PROMPT_TEMPLATE.format(
    #     research_summary=appended_result_summaries,
    #     user_question=question
    # )
    # research_report = llm.invoke(research_report_prompt)
    #
    # print(f'stringified_summary_list: {stringified_summary_list}')
    # print(f'merged_result_summaries: {appended_result_summaries}')
    # print(f'research_report: {research_report}')
