from pdf_to_text import *
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter

# MAIN
print(">> STEP 1: Ensure you have all the required PDF files inside the 'pdf_files' folder.")

check = input("Do you have them installed? [Y/N]: ")
if check.lower() == "n":
    print("Go get some content, nerd.")
    exit()

print(">> STEP 2: There was only 1 step. Commencing data yoinking.")
received_list = folder_pdf_to_text("./pdf_files/")
if len(received_list) == 0:
    print("There was an error! I don't know what it is, just open a pull request or something.")
    exit()

print(">> List received! Now adding to Vector Database!")

# client = chromadb.PersistentClient(path="./data_storage/") #PERSISTENT DATA STORAGE OMOchroma_client = chromadb.HttpClient(host="localhost", port=8000)
client = chromadb.HttpClient(host="localhost", port=8000)
'''RUN chroma run --path "./data_storage/" TO ACTIVATE THE SERVER!!'''
# client.reset() doesnt work unless activated in env variables and im too lazy to do that so deal w it LOL

collection = client.get_or_create_collection("tort_law_pdfs")

text_splitter = RecursiveCharacterTextSplitter( # this is a function lol
    # Set a really small chunk size, just to show.
    chunk_size = 150,
    chunk_overlap  = 15,
    length_function = len,
    add_start_index = True,
)

num_count = 1
for item in received_list:
    formatted_docs = text_splitter.create_documents(item)

    other_num = 1
    for doc in formatted_docs:
        collection.add(
            documents=doc.page_content,
            ids=f"id{num_count}_{other_num}",
        )
        other_num += 1
    num_count += 1
    
print(">> Done! Now run langchainvaraiant.py =)")