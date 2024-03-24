from pydantic import BaseModel
from typing import Optional

class ReqBodySearch(BaseModel):
    search_text: str
    collection_name: str

class ReqBodyImageSearch(BaseModel):
    file_path: Optional[str] = None
    search_text: Optional[str] = None
    content: Optional[str] = None
    top: Optional[int] = 20

class ReqBodyAsk(BaseModel):
    prompt: str
    collection_name: str

class ReqBodyIndex(BaseModel):
    index_type: str
    file_path: str
    collection_name: str

class ReqBodyCollection(BaseModel):
    collection_name: str

class ReqBodyCollectionSearch(BaseModel):
    collection_name: str
    prompt: str