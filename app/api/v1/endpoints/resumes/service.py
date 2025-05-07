import os
import uuid
import subprocess
import time
import traceback
from fastapi.responses import FileResponse
from urllib.parse import urlparse
from jinja2 import Environment, FileSystemLoader
from app.logger import logger


OUTPUT_DIR = "/tmp"


def _escape_latex(text: str) -> str:
    replacements = {
        "&": "\\&", "%": "\\%", "$": "\\$", "#": "\\#",
        "_": "\\_", "{": "\\{", "}": "\\}", "~": "\\textasciitilde{}",
        "^": "\\textasciicircum{}", "\\": "\\textbackslash{}"
    }
    return ''.join(replacements.get(c, c) for c in text)

def escape_latex_filter(text):
    replacements = {
        "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
        "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}", "\\": r"\textbackslash{}"
    }
    return ''.join(replacements.get(c, c) for c in text)


def _prepare_context(data: dict) -> dict:
    def safe_escape_list(lst):
        return [_escape_latex(item) for item in lst]
    
    def latex_link_parts(url):
        parsed = urlparse(url)
        return {
            "url": url,
            "text": _escape_latex(parsed.netloc + parsed.path)
        }
    
    ctx = {
        "name": _escape_latex(data.get("name", "")),
        "phone": _escape_latex(data.get("phone", "")),
        "email": _escape_latex(data.get("email", "")),

        "linkedin_url": "",
        "linkedin_text": "",
        "github_url": "",
        "github_text": "",

        "experiences": data.get("experiences", []),
        "projects": data.get("projects", []),
        "education": data.get("education", []),
        "skills": data.get("skills", {})
    }

    if linkedin := data.get("linkedin"):
        link = latex_link_parts(linkedin)
        ctx["linkedin_url"] = link["url"]
        ctx["linkedin_text"] = link["text"]

    if github := data.get("github"):
        link = latex_link_parts(github)
        ctx["github_url"] = link["url"]
        ctx["github_text"] = link["text"]

    return ctx


async def generate_resume_pdf(data: dict):
    start_time = time.time()
    tmp_id = uuid.uuid4().hex
    # tmp_dir = os.path.join(OUTPUT_DIR, tmp_id)
    # os.makedirs(tmp_dir, exist_ok=True)
    base_data_dir = os.path.join(os.getcwd(), "data")
    tmp_dir = os.path.join(base_data_dir, tmp_id)
    os.makedirs(tmp_dir, exist_ok=True)
    template_dir = "templates"
    template_filename = "resume.tex.j2"

    try:
        context = _prepare_context(data)
        
        env = Environment(
            block_start_string='<BLOCK>',
            block_end_string='</BLOCK>',
            variable_start_string='<VAR>',
            variable_end_string='</VAR>',
            comment_start_string='<#',
            comment_end_string='#>',
            trim_blocks=True,
            autoescape=False,
            loader=FileSystemLoader('templates')
        )
        env.filters['escape_latex'] = escape_latex_filter
        template = env.get_template(template_filename)
        rendered = template.render(**context)

    except Exception as e:
        return {
            "error": "Template rendering failed",
            "details": str(e),
            "trace": traceback.format_exc()
        }

    tex_file = os.path.join(tmp_dir, "resume.tex")
    with open(tex_file, "w") as f:
        f.write(rendered)

     # Start measuring LaTeX compilation time
    latex_start_time = time.time()
    try: 
        cmd = [
            "docker", "exec", "resume_compiler", 
            "pdflatex", "-interaction=nonstopmode", "-file-line-error", "-output-directory", f"/tex_files/{tmp_id}", f"/tex_files/{tmp_id}/resume.tex"
        ]
        subprocess.run(cmd, timeout=30, check=True, capture_output=True, text=True)
        
        latex_end_time = time.time()
        latex_process_time = latex_end_time - latex_start_time
        print(f"LaTeX compilation time: {latex_process_time:.4f} seconds")
    except subprocess.CalledProcessError as e:
        return {
            "error": "LaTeX compilation failed",
            "docker_stderr": e.stderr or "No stderr output",
            "docker_stdout": e.stdout or "No stdout output",
            "status_code": 500
        }
    except subprocess.TimeoutExpired:
        return {"error": "Compilation timed out"}
    print("Path", tmp_dir)
    pdf_path = os.path.join(tmp_dir, "resume.pdf")
    if os.path.exists(pdf_path):
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename="resume.pdf"
        )
    else:
        return {"error": "PDF was not created"}




# async def create_resume(session: AsyncSession, resume: ResumeCreate, user_id: int):
#     new_resume = Resume(user_id=user_id, **resume.dict())
#     session.add(new_resume)
#     await session.commit()
#     await session.refresh(new_resume)
#     return new_resume

# async def get_resume(session: AsyncSession, resume_id: int, user_id: int):
#     result = await session.execute(
#         select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
#     )
#     return result.scalar_one_or_none()

# async def get_resumes(session: AsyncSession, user_id: int):
#     result = await session.execute(
#         select(Resume).where(Resume.user_id == user_id)
#     )
#     return result.scalars().all()

# async def update_resume(session: AsyncSession, resume_id: int, user_id: int, resume_data: ResumeUpdate):
#     resume = await get_resume(session, resume_id, user_id)
#     if resume:
#         for key, value in resume_data.dict(exclude_unset=True).items():
#             setattr(resume, key, value)
#         await session.commit()
#         await session.refresh(resume)
#     return resume

# async def delete_resume(session: AsyncSession, resume_id: int, user_id: int):
#     resume = await get_resume(session, resume_id, user_id)
#     if resume:
#         await session.delete(resume)
#         await session.commit()
#         return True
#     return False
