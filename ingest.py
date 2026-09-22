import os
import hashlib
import frontmatter
from pathlib import Path
from app.db import get_collection

def compute_hash(content: str) -> str:
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def ingest_directory(directory_path: str):
    collection = get_collection()
    
    # Get existing documents to handle deletions
    existing_docs = collection.get(include=["metadatas"])
    existing_ids = set(existing_docs["ids"])
    existing_hashes = {
        doc_id: meta.get("content_hash") 
        for doc_id, meta in zip(existing_docs["ids"], existing_docs["metadatas"] or [])
        if meta
    }
    
    current_ids = set()
    added = 0
    updated = 0
    
    path = Path(directory_path)
    for file_path in path.rglob("*.md"):
        doc_id = str(file_path.absolute())
        current_ids.add(doc_id)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            post = frontmatter.loads(content)
            # Combine frontmatter and content for hashing
            doc_hash = compute_hash(content)
            
            if doc_id in existing_hashes and existing_hashes[doc_id] == doc_hash:
                continue # unchanged
                
            if doc_id in existing_hashes:
                updated += 1
            else:
                added += 1
                
            # Prepare metadata
            metadata = {
                "source": doc_id,
                "content_hash": doc_hash,
            }
            
            # Add other frontmatter to metadata (Chroma requires string, int, float or bool)
            for k, v in post.metadata.items():
                if isinstance(v, list):
                    # Store lists (like tags) as comma separated strings or handle properly
                    # Wait, ChromaDB doesn't support list metadata natively for filtering via $in directly on list field,
                    # well actually in recent versions it might, but usually we just store them as strings or handle them manually.
                    # Let's stringify lists for storage, though we might need special handling for tag filtering.
                    pass # We will handle tags specially
                
            # Clean up metadata for Chroma
            for k, v in post.metadata.items():
                if isinstance(v, (str, int, float, bool)):
                    metadata[k] = v
                elif isinstance(v, list):
                    # ChromaDB currently supports strings, ints, floats, bools
                    metadata[k] = ",".join([str(x) for x in v])
                    
            # Upsert document
            collection.upsert(
                ids=[doc_id],
                documents=[post.content],
                metadatas=[metadata]
            )
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    # Handle deletions
    deleted_ids = existing_ids - current_ids
    if deleted_ids:
        collection.delete(ids=list(deleted_ids))
        
    return {
        "added": added,
        "updated": updated,
        "deleted": len(deleted_ids),
        "total_documents": len(current_ids)
    }
