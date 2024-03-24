from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
from langchain_community.vectorstores.pgvector import PGVector

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import DistanceStrategy
from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

host= os.environ['POSTGRES_HOST']
port= os.environ['POSTGRES_PORT']
user= os.environ['POSTGRES_USER']
password= os.environ['POSTGRES_PASSWORD']
dbname= os.environ['POSTGRES_DATABASE']

CONNECTION_STRING = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

embedding_func = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_db(collection_name: str, pre_delete_collection: bool = True):
    return PGVector(
        embedding_function = embedding_func,
        collection_name= collection_name,
        distance_strategy = DistanceStrategy.COSINE,
        connection_string=CONNECTION_STRING,
        pre_delete_collection=pre_delete_collection
        )

def get_vector_db_search(collection_name: str, pre_delete_collection: bool = True):
    return PGVector(
        embedding_function = embedding_func,
        collection_name= collection_name,
        distance_strategy = DistanceStrategy.COSINE,
        connection_string=CONNECTION_STRING
        )

db = get_vector_db_search("hedis_spec_test", pre_delete_collection=False)
retriever = db.as_retriever(search_type="mmr")

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

template = """Answer the question based only on the following context:

{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

## Routes
app = FastAPI()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
# add_routes(app, NotImplemented)

add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)

add_routes(
    app,
    chain,
    path="/mychain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
