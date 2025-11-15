from pydantic import BaseModel
from typing import Optional,List

class DocumentUpload(BaseModel):
    title:str
    content:Optional[str] = None # text content if uploading text
    filename: Optional[str] = None # original filename


class QueryRequest(BaseModel):
    question: str
    top_k:Optional[int] = 5