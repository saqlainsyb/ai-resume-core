# app/core/templates.py
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"

latex_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
