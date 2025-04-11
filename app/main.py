from fastapi import FastAPI
from contextlib import asynccontextmanager
# from app.api import auth, users, resumes, templates, ai
from app.core.config import settings
from app.db.init_db import init_db
from .middleware import setup_middleware
from app.api.v1.endpoints.api import api_router
from .logger import logger
from fastapi.openapi.utils import get_openapi

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

# Include Middleware (CORS)
setup_middleware(app)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health"])
def read_root():
    logger.info("Health check endpoint accessed.")
    return {"status": "ok", "message": "AI Resume Builder API is running."}
