from resai.pgutil import get_vector_db_search
from langchain_core.documents import Document
from typing import (
    List,
    Tuple,
)

def similarity_search(search_text: str, collection_name: str, k: int = 10) -> List[Tuple[Document, float]]:
    db = get_vector_db_search(collection_name, pre_delete_collection=False)
    return db.similarity_search_with_score(search_text, k)

def search_response_to_dict(response):
    response_dict = [{"document": {"page_content": doc.page_content, "metadata": doc.metadata}, "score": score} for doc, score in response]
    return response_dict