import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import dotenv_values
import openai
from langchain.llms import OpenAI

# initialization
config = dotenv_values(".env")
telegram_bot_token = config["TELEGRAM_BOT_TOKEN"]
openai.api_key = config["OPENAI_APIKEY"]

context_statement = f"""
    You are a helpful legal assistant that answers questions based on the questions that users provide.
    If the question does not concern legal issues, decline to answer.
    Answer in the context of Singapore tort law if possible. If it is not possible, state that you are answering under the context of a different genre of law.
"""

messages = [
    {"role": "system", "content": context_statement}
]

# telegram bot handling
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"🟢 {update.message.from_user.__getattribute__('username')}:{update.effective_chat.id} - {update.message.text}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ask me questions about Torts and I shall do my best to answer! Do /help if you need assistance!")

async def conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global messages, context_statement

    print(f"🟢 {update.message.from_user.__getattribute__('username')}:{update.effective_chat.id} - {update.message.text}")
    question = update.message.text
    messages.append({"role": "user", "content": question})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.3
    )

    response = completion.choices[0].message.content
    print(f"🟢👌RESPONSE TO {update.message.from_user.__getattribute__('username')}:{update.effective_chat.id} - {response}")
    _ = messages.pop()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == '__main__':
    application = ApplicationBuilder().token(telegram_bot_token).build()
    
    #command handler loop
    start_handler = CommandHandler('start', start)
    question_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), conversation)

    application.add_handler(start_handler)
    application.add_handler(question_handler)
    
    application.run_polling()