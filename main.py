from dotenv import load_dotenv, find_dotenv
import openai
import os

_ = load_dotenv(find_dotenv())
os.environ['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']
openai.api_key = os.environ['OPENAI_API_KEY']

if __name__ == "__main__":

    # setup FAISS vectorstore

    #
    print(f'Testing')