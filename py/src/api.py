#!/usr/bin/env python
from dotenv import load_dotenv, find_dotenv
import os
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from reqmodel import ReqBodyAsk, ReqBodyIndex, ReqBodySearch, ReqBodyImageSearch
from fastapi.responses import RedirectResponse
from uuid import uuid4
from resai.chat import ask_collection
from resai.storage import upload_file
from resai.azure.storage import get_blob_sas_token
from resai.indexer import index_data
from resai.azure.search import search_data
from resai.azure.vision import get_image_embedding, get_text_embedding

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173"
]

_ = load_dotenv(find_dotenv())

SEARCH_SERVICE_NAME = os.getenv("SEARCH_SERVICE_NAME")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME")


def get_app():
    app = FastAPI(
        title="ResAI API",
        version="0.0.1",
        description="An AI research assistant tool",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def redirect_root_to_docs():
        return RedirectResponse("/docs")

    @app.post("/search")
    async def search(req_body: ReqBodyImageSearch):
        print(req_body)
        try:
            image_embedding = None
            if (req_body.file_path):
                print("API: Getting image embedding")
                image_embedding = get_image_embedding(req_body.file_path)

            content_embedding = None
            if (req_body.content):
                print("API: Getting content embedding")
                content_embedding = get_text_embedding(req_body.content)

            response = search_data(
                search_service_name=SEARCH_SERVICE_NAME,
                index_name=SEARCH_INDEX_NAME,
                image_embedding=image_embedding,
                search_text=req_body.search_text,
                content_embedding=content_embedding,
                content=req_body.content,
                top=req_body.top
            )

            response = update_response_with_sas_token(response)

            return JSONResponse({"success": True, "data": response})
        except Exception as e:
            print("API: Error")
            print(e.text)
            return JSONResponse({"success": False, "error": str(e)})
        
    def update_response_with_sas_token(response):
        for item in response['value']:
            file_path = item['file_path']
            sas_token = get_blob_sas_token(file_path)
            final_path = f"{file_path}?{sas_token}"
            item['file_path'] = final_path
        return response


    @app.post("/ask")
    async def ask(req_body: ReqBodyAsk):
        try:
            response = ask_collection(
                req_body.collection_name, req_body.prompt)
            return JSONResponse({"success": True, "data": response})
        except Exception as e:
            return JSONResponse({"success": False, "error": str(e)})

    @app.post("/upload")
    async def upload(file: UploadFile):
        try:
            ext = file.filename.split(".")[-1]
            file_key = f"{str(uuid4())}.{ext}"

            upload_file(file_key, file.file)

            meta_data = {
                "user_id": 1,
                "file_key": file_key,
                "file_name": file.filename,
                "file_size": file.size,
                "content_type": ext,
            }

            # todo: save meta_data to db

            return JSONResponse({"success": True, "data": meta_data})
        except Exception as e:
            return JSONResponse({"success": False, "error": str(e)})

    @app.post("/index")
    async def index(req_body: ReqBodyIndex):
        resp = index_data(
            req_body.index_type,
            req_body.file_path,
            req_body.collection_name
        )

        return JSONResponse({"success": True, "data": resp})

    return app
