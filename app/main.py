import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router
from app.api.dependencies import AppContainer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application lifecycle...")
    try:
        AppContainer.initialize()
        logger.info("Application container successfully initialized on startup.")
    except Exception:
        logger.exception("Critical failure during application startup")
        raise
        
    yield
    
    logger.info("Shutting down application lifecycle...")
    try:
        AppContainer.shutdown()
        logger.info("Application container components cleaned up successfully.")
    except Exception:
        logger.exception("Error during application shutdown resource cleanup")

app = FastAPI(
    title="Enterprise Knowledge Base Copilot",
    description="A production-grade modular Retrieval-Augmented Generation (RAG) backend engine.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/", tags=["Root Operations"])
def read_root():
    return {
        "application": "Enterprise Knowledge Base Copilot",
        "version": "1.0.0",
        "status": "running"
    }
