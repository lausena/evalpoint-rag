import argparse

from rag import handle_rag

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("question", type=str, help="Question to ask the LLM.")
args = arg_parser.parse_args()


handle_rag(args.question)