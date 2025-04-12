# app/db/base.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# explicitly import models for alembic migrations
from app.api.v1.endpoints.auth.models import User 
from app.api.v1.endpoints.resumes.models import Resume
from app.api.v1.endpoints.templates.models import Template
