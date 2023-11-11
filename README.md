# Singpaore Tort Law Chatbot! (Tyler)

Tyler is a chatbot that specializes in the law of torts with regards to Singapore's laws. He was made in two stressful days and is slowly being refined as time goes on. Please read further below if you would like to clone and host this bot for yourself.

## Disclaimer

Be sure to thoroughly **read through** ***Limitations*** later. This bot and I **DO NOT** offer any sort of professional legal advice for any issues you might be experiencing. This bot is prone to hallucinations (shamelessly making things up when it is unsure). Do not use this as proper legal advice. Be cautious when you use it as a study tool as it might reflect inaccurate information. 

Once again, **the advice offered by this bot is flawed**. Please do your own research. This bot is nothing but a starter framework for your studies.

## Hosting

There are a few steps you need to take if you would like to host this bot on your own. Follow these through and please do not skip any steps or something will break. Trust me. Many things have broken (and they are all my fault).

* Clone the repository into your selected folder
    * You can clone it from `https://github.com/huitingloke/torty-chatty`
* Make a new terminal and initialize your virtual environment with `virtualenv env`
* Start the virtual environment with
    * Mac/Linux: `source env/bin/activate`
    * Windows: `env/Scripts/activate`
* Create a folder called `pdf_files`
* Create a file called `filelog.txt` and leave it empty
* Create a `.env` file and add your own keys
    * `BotFather`: Create your own Telegram bot, copy the API token and add a line called `TELEGRAM_BOT_TOKEN`
    * `OpenAI`: Obtain your own API key from [Open AI's website](https://platform.openai.com/api-keys), add a line to the `.env` file called `OPENAI_APIKEY`
* Store all `.pdf` files of legal cases into the `./pdf_files/` folder
    * Do not nest them in other folders
* Create a new terminal and enter `chroma run --path "./data_storage/"`
* Run`initialization.py`
* Create another new terminal and *do not close the initial terminal*
* Run `main.py`

As long as `main.py` is running, Tyler will run. The database is technically optional but it would result in much better queries as it obtains information from cases in your `.pdf` files, so I would highly recommend using it.

## Noteworthy libraries + workflow

* `python-telegram-bot`: Fortunately, there was an easy to implement wrapper that allowed me to access Telegram's API only using Python. This is that way. The documentation is not bad. Reference it [here](https://docs.python-telegram-bot.org/en/v20.6/). 
* `langchain`: Simple chain created to optimize the flow of LLM queries through...
* `openai gpt-3.5`: OpenAI API! Using `gpt-3.5-turbo` which has not been fine-tuned yet.
* `chromadb`: A database recommended to me by a friend. It's locally hosted on the machine!

Essentially, any message sent to the bot is registered as a query, which is passed as a question. The question is passed into `chromadb` as a search query and the relevant embeddings are returned into a variable. A prompt template with the question and some instructions are passed into the LLM along with the variable with the information. The response is returned to the user. 

This bot has no conversational memory. That is to say it cannot use previous interactions as context. Perhaps that could be something I look to implement in the future, but right now I have other projects which I need to attend to. 

## Advice

If you want to query this bot, I would recommend providing as much contextual information as possible. While asking general questions are alright (as I assume the bot will be more helpful to the general public rather than specialized legal professionals), the bot will be able to draw more relevant information with more keywords. Not words like "the" or "and", but words in context. 

Adding more `.pdf` files will definitely help with the accuracy of the answer. However, just note that every time you add a file (or remove a file), **you need to rerun initialization.py**. The script amends the database directly. 

## Limitations

### Short responses completely mess it up

Asking queries with a few words e.g. *is it criminal to* will lead the LLM to complete the prompt before answering it with a question. I don't know how to fix this even after prompt engineering.

### Context limitations

Too many words simply will return a negative response from the API. I can't increase the limit unless I swap to a different LLM. The only other LLMs I know are all self hosted as well, and I'm on a Mac so that's out of the question right now. 

However, I did toy around with the idea of using GPT4All and crawling around for some kind of locally hosted API that I could use to link queries but I decided against it because I have known Langchain for approximately 4 days (as of writing) and I don't want to overload myself with more work right now.

### Hallucinations

As with most LLMs that are publicly accessible and relatively cheap, it's prone to creating information where information doesn't exist. I haven't exactly found a way to resolve this yet but my current plan would be to fine tune that model until nothing changes. 

### Small database

Currently it's small because I'm hosting it and I could only find 5 PDFs, including Spandeck! However, if you host this... nothing's stopping you from adding more

### Money!

Seeing that this uses *openai*'s beloved API, it's going to cost money if a lot of people use this. This is a cry for help. Please host this on your own.

## Features that I *might* implement

* **Logging**: Ensure that all user's interactions are logged to prevent misuse
* **Private user access**: Only allow particular people (in a private, saved, *UNCOMMITTED* JSON file) to use the bot, refuse all requests otherwise
* **Rate limiter**: Just to ensure that all this isn't spammable
* **Fine tuning**
    * Currently, the base model and prompt engineering it being utilized. I would like to perhaps implement `ragas` in the future and use it to evaluate the queries of this bot and perhaps fine tune it to allow for more accurate responses as well