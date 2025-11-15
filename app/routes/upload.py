from fastapi import APIRouter,File,UploadFile, Form
from app.db import documents_col
from app.utils import extract_text_from_pdf_bytes,chunk_text
from datetime import datetime
import uuid

router = APIRouter(prefix="/docs",tags=["documents"])

@router.post("/upload")
async def upload_document(title:str=Form(...),file:UploadFile=File(...)):
    """
    Accepts a file upload (pdf or text) and stores:
    - original filename
    - content
    - chunkslist
    - metadata
    """

    contents  =await file.read()

    if file.content_type == "application/pdf":
        text = extract_text_from_pdf_bytes(contents)

    else:
        try:
            text = contents.decode("utf-8")
        except:
            text= ""

    
    # chunks text for retrival

    chunks = chunk_text(text,chunk_size=1200,overlap=200)

    doc = {
        "_id" : str(uuid.uuid4()),
        "title" : title,
        "filename" : file.filename,
        "content" : text,
        "chunks" : chunks,
        "created_at" : datetime.utcnow()
    }

    documents_col.insert_one(doc)

    return {"message":"uploaded","id":doc["_id"],"num_chunks":len(chunks)}