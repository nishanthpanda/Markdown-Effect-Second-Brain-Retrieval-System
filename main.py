import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from app.models import SearchRequest, SearchResponse, SyncRequest, SyncResponse, DocumentResponse
from app.db import search_documents
from app.ingest import ingest_directory
from app.db import get_collection

app = FastAPI(title="Second Brain Retrieval System")

@app.post("/sync", response_model=SyncResponse)
def sync_directory(request: SyncRequest):
    if not os.path.isdir(request.directory_path):
        raise HTTPException(status_code=400, detail="Invalid directory path")
        
    try:
        result = ingest_directory(request.directory_path)
        return SyncResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    # Build Chroma where clause
    where_conditions = []
    
    if request.date_from:
        where_conditions.append({"created_date": {"$gte": request.date_from}})
    if request.date_to:
        where_conditions.append({"created_date": {"$lte": request.date_to}})
        
    if request.tags_include:
        for tag in request.tags_include:
            where_conditions.append({"tags": {"$contains": tag}})
            
    if request.tags_exclude:
        for tag in request.tags_exclude:
            where_conditions.append({"tags": {"$not_contains": tag}})

    where = None
    if len(where_conditions) == 1:
        where = where_conditions[0]
    elif len(where_conditions) > 1:
        where = {"$and": where_conditions}

    try:
        results = search_documents(
            query=request.query,
            top_k=request.top_k,
            where=where
        )
        
        response_docs = []
        # results is a dict: {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}
        if results and results["ids"] and len(results["ids"]) > 0:
            for i in range(len(results["ids"][0])):
                doc_id = results["ids"][0][i]
                content = results["documents"][0][i]
                metadata = results["metadatas"][0][i] or {}
                distance = results["distances"][0][i] if "distances" in results else None
                
                response_docs.append(
                    DocumentResponse(
                        id=doc_id,
                        content=content,
                        metadata=metadata,
                        distance=distance
                    )
                )
                
        return SearchResponse(results=response_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/document")
def delete_document(doc_id: str):
    collection = get_collection()
    collection.delete(ids=[doc_id])
    return {"status": "success", "deleted_id": doc_id}
