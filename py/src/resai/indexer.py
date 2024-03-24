# Refs:
# - https://chunkviz.up.railway.app/

import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
# from langchain_community.document_loaders import DirectoryLoader
from resai.pgutil import get_vector_db
from dotenv import load_dotenv, find_dotenv
from PIL import Image
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter


_ = load_dotenv(find_dotenv())

base_path = os.environ['BASE_PATH']

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def index_data(index_type: str, file_path: str, collection_name: str):
    if index_type == "pdf":
        return load_pdf(file_path, collection_name)
    elif index_type == "pdf_dir":
        return load_pdf_dir(file_path, collection_name)
    elif index_type == "jpg":
        return load_jpg(file_path, collection_name)
    elif index_type == "md_dir":
        return load_md_dir(file_path, collection_name)

    return False


def load_pdf(file_path: str, collection_name: str):
    db = get_vector_db(collection_name)
    loader = PyMuPDFLoader(file_path)
    documents = loader.load_and_split()
    db.add_documents(documents)
    return True


def load_pdf_dir(dir_path: str, collection_name: str):
    db = get_vector_db(collection_name)
    loader = DirectoryLoader(dir_path, glob="*.pdf")
    docs = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs_split = text_splitter.split_documents(docs)
    db.add_documents(docs_split)
    return True


def load_md_dir(
        directory_path: str,
        collection_name: str,
        chunk_size=1000,
        chunk_overlap=0
):
    db = get_vector_db(collection_name)

    loader = DirectoryLoader(directory_path)
    documents = loader.load()

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    split_documents = []
    
    for document in documents:
        split_document = splitter.split_text(document.page_content)
        split_documents.extend(split_document)

    db.add_documents(split_documents)
    return True


def load_jpg(file_path: str, collection_name: str):
    image = Image.open(file_path)
    image_embedding = embeddings.embed_image([image])[0]
    db = get_vector_db(collection_name)
    db.add_embeddings([image_embedding])
    return True
