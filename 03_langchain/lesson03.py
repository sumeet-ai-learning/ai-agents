import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(override=True)
api_key = os.getenv("GOOGLE_API_KEY")
template = PromptTemplate(input_variables=["country"],template="What is the capital of {country}")
formatted_prompt = template.format(country="India")

chat_model = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL"), api_key=api_key)
response = chat_model.invoke(formatted_prompt).text
print(response)


