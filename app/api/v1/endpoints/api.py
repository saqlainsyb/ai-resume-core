# app/api/v1/endpoints/api.py
from fastapi import APIRouter
from app.api.v1.endpoints.auth.router import router as auth_router
from app.api.v1.endpoints.templates.router import router as templates_router
# from app.api.v1.endpoints.users.router import router as users_router
# from app.api.v1.endpoints.resumes.router import router as resumes_router
# from app.api.v1.endpoints.ai.router import router as ai_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(templates_router, prefix="/templates", tags=["Templates"])
# api_router.include_router(users_router, prefix="/users", tags=["Users"])
# api_router.include_router(resumes_router, prefix="/resumes", tags=["Resumes"])
# api_router.include_router(ai_router, prefix="/ai", tags=["AI Suggestions"])
