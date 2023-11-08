import chromadb

client = chromadb.HttpClient(host="localhost", port=8000)
'''RUN chroma run --path "./data_storage/" TO ACTIVATE THE SERVER!!'''
# client.reset() doesnt work unless activated in env variables and im too lazy to do that so deal w it LOL

collection = client.get_or_create_collection("tort_law_pdfs")

print(collection.get())