from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from dotenv import dotenv_values
config = dotenv_values(".env")

'''
    Prompt templates: bundled with user input so you don't have to specify what you want
'''

#openai.api_key = config["OPENAI_APIKEY"]
llm = OpenAI(openai_api_key=config["OPENAI_APIKEY"])

chat_model = ChatOpenAI(openai_api_key=config["OPENAI_APIKEY"])

text = "What would be a good company name for a company that makes colorful socks?"
messages = [HumanMessage(content=text)]

# print(llm.predict_messages(messages))
# >> Feetful of Fun

# print(chat_model.predict_messages(messages))
# >> Socks O'Color

prompt = PromptTemplate.from_template("What is a good name for a team that plays {game}?")
game = input("Write the name of a game: ")
print(prompt.format(game=game))

from langchain.prompts.chat import ChatPromptTemplate

template = "You are a helpful assistant that translates {input_language} to {output_language}."
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

chat_prompt.format_messages(input_language="English", output_language="French", text="I love programming.")


class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""


    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")

CommaSeparatedListOutputParser().parse("hi, bye")
# >> ['hi', 'bye']

