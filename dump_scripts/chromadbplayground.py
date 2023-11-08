import chromadb

chroma_client = chromadb.Client()

#like mongodb, its where you store your data incl embeddings, metadata and and docs :3
collection = chroma_client.create_collection(name="my_collection")

import chromadb
client = chromadb.PersistentClient(path="./data_storage/") #PERSISTENT DATA STORAGE OMO
# RUN chroma run --path "./data_storage/" TO ACTIVATE THE SERVER!!

client.heartbeat() #checks if homeboy is alive

collection.add(
    documents=["This is a document", "This is another document"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["id1", "id2"]
) #adding docs

collection.add(
    embeddings=[[1.2, 2.3, 4.5], [6.7, 8.2, 9.2]],
    documents=["This is a document", "This is another document"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["id1", "id2"]
) #adding docs with ALREADY GENERATED EMBEDDINGS (if dont have, then ignore)

results = collection.query(
    query_texts=["This is a query document"],
    n_results=2
)
