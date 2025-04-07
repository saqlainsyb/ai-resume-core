from fastapi import FastAPI
from contextlib import asynccontextmanager
# from app.api import auth, users, resumes, templates, ai
from app.core.config import settings
from app.db.init_db import init_db
from .middleware import setup_middleware
from .logger import logger

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

# Include API routers
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(users.router, prefix="/api/users", tags=["Users"])
# app.include_router(resumes.router, prefix="/api/resumes", tags=["Resumes"])
# app.include_router(templates.router, prefix="/api/templates", tags=["Templates"])
# app.include_router(ai.router, prefix="/api/ai", tags=["AI Suggestions"])


@app.get("/", tags=["Health"])
def read_root():
    logger.info("Health check endpoint accessed.")
    return {"status": "ok", "message": "AI Resume Builder API is running."}
