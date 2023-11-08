import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import dotenv_values
import openai
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, BaseOutputParser
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts.chat import ChatPromptTemplate
import chromadb

# initialization

client = chromadb.PersistentClient(path="./data_storage/") #PERSISTENT DATA STORAGE OMO
# RUN chroma run --path "./data_storage/" TO ACTIVATE THE SERVER!!
# client.reset() doesnt work unless activated in env variables and im too lazy to do that so deal w it LOL

# langchain split docs, chroma parse into vectordb
# pypdf vibes
config = dotenv_values(".env")

path_to_folder = "./pdf_files/"

start_message = "🌟🌟 Ask me questions about Torts and I shall do my best to answer! Do /help if you need assistance! 🌟🌟"

credits_message = """
Created by Beth (C&L 2022/2023) in 2 sleepless nights for class participation grades!
❤️❤️❤️ Please I am very desperate 🌟🌟🌟"""

help_message = """
Ask whatever questions you have about Singapore Tort Law here and I shall try my best to help 🐍

🌟 Other available commands 🌟
/start - begin!
/help - learn how to use me!
/credits - see who's behind this garbage!
"""

# telegram bot handling
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# UTILITY FUNCTION PORTION
def get_relevant_content(question:str) -> str:
    collection = client.get_or_create_collection("tort_law_pdfs")
    content = ""

    return content

def get_response(question:str) -> str:
    global config

    response = "There was an error in processing! Please contact @dobesquiddy if you believe this to be an error."

    telegram_bot_token = config["TELEGRAM_BOT_TOKEN"]
    #openai.api_key = config["OPENAI_APIKEY"]
    llm = OpenAI(openai_api_key=config["OPENAI_APIKEY"])

    relevant_sentences = get_relevant_content(question)

    system_template = """
        You are a helpful legal assistant that answers questions based on what the user asks.
        If the question does not concern legal issues, decline to answer.
        Do not encourage the user to harm him or herself or anyone else.
        Answer in the context of Singapore tort law if possible. If it is not possible, state that you are answering under the context of a different genre of law.
    """
    # add {content} later

    human_template = "{question}"

    class ResponseParser(BaseOutputParser):
        """Return the output as a string. Simply complete the chain"""

        def parse(self, text: str):
            """Parse the output of an LLM call."""
            return text


    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template),
    ])

    chain = chat_prompt | llm | ResponseParser()
    try:
        response = chain.invoke({"question": question})
    except:
        print("There was an error! Sending default error response to the user!")

    return response[10:] #because it says System: at the start and i dont like that >:(



# MAIN PORTION
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

async def credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=credits_message)


async def conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global messages, context_statement
    question = update.message.text
    print(f"🟢 {update.message.from_user.__getattribute__('username')}:{update.effective_chat.id} - {update.message.text}")
    response = get_response(question)
    print(f"🟢🟢🟢 {update.message.from_user.__getattribute__('username')}:{update.effective_chat.id} - {response}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == '__main__':

    application = ApplicationBuilder().token(config["TELEGRAM_BOT_TOKEN"]).build()
    
    #command handler loop
    handlers = [
        CommandHandler('start', start),
        CommandHandler('help', help),
        CommandHandler('credits', credits),
        MessageHandler(filters.TEXT & (~filters.COMMAND), conversation)
    ]

    for item in handlers:
        application.add_handler(item)
    
    application.run_polling()