from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.init_db import init_db
from .middleware import setup_middleware
from app.api.v1.endpoints.api import api_router
from .logger import logger
from fastapi.staticfiles import StaticFiles
from starlette.middleware.gzip import GZipMiddleware
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    await init_db()
    logger.info("🚀 Application startup complete.")
    yield
    # Shutdown actions
    logger.info("🛑 Application shutdown initiated.")

# FastAPI app initialization
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI Resume Builder API",
    version="1.0.0",
    lifespan=lifespan
)

## Static directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Apply gzip middleware globally
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include Middleware (CORS)
setup_middleware(app)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health"])
def read_root():
    logger.info("Health check endpoint accessed.")
    return {"status": "ok", "message": "AI Resume Builder API is running."}
