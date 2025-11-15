from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.query import router as query_router

app = FastAPI(title="AI Document Q&A")

app.include_router(upload_router)
app.include_router(query_router)

@app.get("/")
def root():
    return {"status":"ok","service":"AI Document Q&A"}
