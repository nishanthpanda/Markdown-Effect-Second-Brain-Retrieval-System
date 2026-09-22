# 🧠 Markdown Effect: Second Brain Retrieval System

This project is a powerful "Second Brain" backend service that intelligently syncs, embeds, and retrieves your local Markdown files using semantic search and metadata filtering. It effectively turns a directory of markdown notes into a queryable vector database.

## Tech Stack Used
**Backend & API:** Python, FastAPI, Uvicorn, Pydantic | **Database & AI:** ChromaDB, Google GenAI | **Document Processing:** Python Frontmatter, Hashlib

## Project Overview

- **Automated Document Ingestion**: Implemented a `/sync` API endpoint to recursively scan directories for **Markdown Files**, extract YAML **Frontmatter Metadata**, and compute **MD5 Hashes** to efficiently sync only added, updated, or deleted files.
- **Vector Embeddings & Storage**: Leveraged the **Google GenAI** API to generate rich semantic embeddings for markdown content, seamlessly storing the text and metadata in a local, high-performance **ChromaDB Vector Database**.
- **Advanced Semantic Search**: Built a dynamic `/search` endpoint that combines semantic vector search with advanced **Metadata Filtering**, allowing users to find documents by meaning while strictly filtering by **Tags** (include/exclude) and **Date Ranges**.
- **Robust API Backend**: Designed a scalable and asynchronous **FastAPI** server, utilizing strict **Pydantic Models** for request/response validation and structured error handling.

## Setup Instructions

1. Install the dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file and add your Google API key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

3. Run the FastAPI server:
```bash
uvicorn app.main:app --reload
```
*The API will be available at `http://localhost:8000`*
