from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import dotenv_values
config = dotenv_values(".env")
#openai.api_key = config["OPENAI_APIKEY"]
llm = OpenAI(openai_api_key=config["OPENAI_APIKEY"])

chat_model = ChatOpenAI(openai_api_key=config["OPENAI_APIKEY"])

print(llm.predict("hi!"))

print(chat_model.predict("hi!"))