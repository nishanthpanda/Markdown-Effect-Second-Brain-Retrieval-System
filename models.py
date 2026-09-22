from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    date_from: Optional[str] = None # format YYYY-MM-DD
    date_to: Optional[str] = None   # format YYYY-MM-DD
    tags_include: Optional[List[str]] = None
    tags_exclude: Optional[List[str]] = None

class DocumentResponse(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    distance: Optional[float] = None

class SearchResponse(BaseModel):
    results: List[DocumentResponse]

class SyncRequest(BaseModel):
    directory_path: str = Field(description="The path to the directory containing markdown files to ingest")

class SyncResponse(BaseModel):
    added: int
    updated: int
    deleted: int
    total_documents: int
