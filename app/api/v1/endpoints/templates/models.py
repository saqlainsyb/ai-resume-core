from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    file_path = Column(String, nullable=False)  # Path to the template file (HTML, DOCX, etc.)
    preview_image= Column(String, nullable=False)    # e.g. "/static/previews/modern.png"
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))

    # Define relationship with Resume (if needed)
    # resumes = relationship("Resume", back_populates="template")
