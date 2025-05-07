from pydantic import BaseModel
from typing import List, Optional, Dict

class Job(BaseModel):
    role: str
    company: str
    start: str
    end: Optional[str]
    details: List[str]

class Project(BaseModel):
    title: str
    stack: str
    details: List[str]

class Education(BaseModel):
    degree: str
    institution: str
    start: str
    end: str
    notes: Optional[List[str]]

class Skills(BaseModel):
    languages: str
    frameworks: str
    frontend: str
    databases: str
    tools: str
    methodologies: str

class ResumeData(BaseModel):
    name: str
    email: str
    phone: str
    linkedin: str
    github: str
    summary: Optional[str]
    experience: List[Job]
    projects: List[Project]
    education: List[Education]
    skills: Skills