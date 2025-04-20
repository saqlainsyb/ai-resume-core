# app/core/templates.py
from pathlib import Path
from fastapi.templating import Jinja2Templates

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # .../app
TEMPLATES_DIR = PROJECT_ROOT.parent / "templates"      # .../templates

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
