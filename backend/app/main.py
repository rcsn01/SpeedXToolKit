from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import files, transform

app = FastAPI(title="Data Processor API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(transform.router, prefix="/transform", tags=["transform"])

@app.get("/health")
async def health():
    return {"status": "ok"}
