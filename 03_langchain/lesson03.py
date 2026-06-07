import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model

load_dotenv(override=True)
api_key = os.getenv("GOOGLE_API_KEY")
chatgpt_api_key = os.getenv("OPENAI_API_KEY")

def basic_chains(arg:dict[str, Any]):

    prompt = ChatPromptTemplate.from_template("You are a helpful assistant. Answer this {question} in detail.")
    model = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL"), api_key=api_key)
    parser = StrOutputParser()
    chain = prompt | model | parser
    return chain.invoke(arg)

def batch_chains(inputs:list[dict[str, str]]) -> None:
    prompt = ChatPromptTemplate.from_template("Translate in Hindi {text} ")
    model = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL"), api_key=api_key)
    parser = StrOutputParser()
    chain = prompt | model | parser
    result = chain.batch(inputs)

    for text in zip(inputs,result):
        print(f"questison  {text[0]['text']}\nanswer:\n{text[1]}")

def stream_chains(question:dict[str, str]) -> None:
    prompt = ChatPromptTemplate.from_template("Explain or answer the {text} ")
    model = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL"), api_key=api_key)
    parser = StrOutputParser()
    chain = prompt | model | parser
    for chunk in chain.stream(question):
        print(chunk,end="",flush=True)

def parallel_chain():
    answer_prompt = ChatPromptTemplate.from_template("Explain or answer the {text} ")
    tone_prompt = ChatPromptTemplate.from_template("What is the tone of the {text} ")

    model = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL"), api_key=api_key)
    parser = StrOutputParser()


    parallel_chain = RunnableParallel(chain1 = answer_prompt | model | parser,
    chain2 = tone_prompt | model | parser)

    text={"text":"AI is the future of development and coding is obselette but not engineering"}
    result = parallel_chain.invoke(text)
    print(result['chain1'])
    print("*"*50)
    print(result['chain2'])

#chain_result = basic_chains({"question": "What is 2+2"})
#print("Results from AI with basic chaining:\n" + chain_result)
#print("*"*50)

# inputs = [{"text": "How are you?"}, {"text": "What is your name?"}, {"text": "What is your favorite color?"}]
# batch_chains(inputs)
# stream_chains({"text":"Why did Newton invented Calculus"})
#
# def any_model():
#     init_chat_model(model="gpt-5-4-mini",provider="openai", api_key=chatgpt_api_key)

parallel_chain()