import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import DistanceStrategy
from langchain_community.vectorstores.pgvector import PGVector

_ = load_dotenv(find_dotenv())

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

