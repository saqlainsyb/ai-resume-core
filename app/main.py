from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.init_db import init_db
from .middleware import setup_middleware
from app.api.v1.endpoints.api import api_router
from .logger import logger
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4
from weasyprint import HTML
import base64
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

# Use Jinja2Templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Include Middleware (CORS)
setup_middleware(app)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health"])
def read_root():
    logger.info("Health check endpoint accessed.")
    return {"status": "ok", "message": "AI Resume Builder API is running."}

# sample_data = {
#         "user": {
#             "name": "Veronica Harrison",
#             "title": "Graphic Designer",
#             "photo": "images\Photo.png",
#             # "photo": "",
#             "email": "veronicaharr@gmail.com",
#             "phone": "+1 273 931 3743",
#             "location": "Los Angeles, CA, 92383",
#             "linkedin": "https://linkedin.com/in/veronika-harrison",
#             "summary": "Graphic designer with +8 years of experience in branding and print design. Skilled at Adobe Creative Suite (Photoshop, Illustrator, InDesign) as well as sketching and hand drawing.",
#             "skills": ["Figma", "Sketch", "Adobe Photoshop", "Adobe Illustrator", "Premiere Pro", "After Effects"],
#             "experience": [
#                 {
#                     "title": "UI Designer",
#                     "company": "Market Studios",
#                     "start_date": "Oct 2012",
#                     "end_date": "Sep 2015",
#                     "location": "Los Angeles",
#                     "description": "Successfully translated subject matter into concrete design for newsletters, promotional materials, and sales collateral. Created design graphics for marketing and sales presentations, training videos, and corporate websites."
#                 },
#                 {
#                     "title": "Graphic Designer",
#                     "company": "FireWeb",
#                     "start_date": "Oct 2015",
#                     "end_date": "Jan 2018",
#                     "location": "San Francisco",
#                     "description": "Created new design themes for marketing and collateral materials. Collaborated with creative team to design and produce computer-generated artwork for marketing and promotional materials."
#                 }
#             ],
#             "education": [
#                 {
#                     "institution": "Iowa University",
#                     "start_date": "Nov 2005",
#                     "end_date": "Sep 2010",
#                     "degree": "Bachelor of Fine Arts in Graphic Design",
#                     "gpa": "3.4/4.0"
#                 },
#                 {
#                     "institution": "Iowa University",
#                     "start_date": "Aug 2010",
#                     "end_date": "Sep 2012",
#                     "degree": "Master of Graphic Design",
#                     "gpa": "3.8/4.0"
#                 }
#             ]
#         }
#     }

# sample_data = {
#   "user": {
#     "name": "Amaan Shannon",
#     "title": "Web-Designer",
#     # "photo": "images/Photo.png",
#     "photo": "",
#     "summary": "Graphic designer with +8 years of experience in branding and print design. Skilled at Adobe Creative Suite (Photoshop, Illustrator, InDesign) as well as sketching and hand drawing.",
#     "contacts": [
#       "2207 Beach Avenue, Los Angeles",
#       "amaan@designer.com",
#       "(414) 799-6342",
#       "shannonportfolio.com"
#     ],
#     "education": [
#       {
#         "institution": "Iowa University",
#         "start_date": "2005",
#         "end_date": "2007",
#         "degree": "Bachelor of Fine Arts in Graphic Design, GPA: 3.4/4.0"
#       },
#       {
#         "institution": "New York University",
#         "start_date": "2007",
#         "end_date": "2010",
#         "degree": "Master of Graphic Design, GPA: 3.8/4.0"
#       }
#     ],
#     "experience": [
#       {
#         "title": "UI Designer",
#         "company": "Market Studios",
#         "start_date": "2012",
#         "end_date": "2015",
#         "description": "Successfully translated subject matter into concrete design for newsletters, promotional materials and sales collateral. Created design graphics for marketing and sales presentations, training videos, and corporate websites."
#       },
#       {
#         "title": "Graphic Designer",
#         "company": "FireWeb",
#         "start_date": "2015",
#         "end_date": "Present",
#         "description": "Developed numerous marketing programs (logos, brochures, newsletters, infographics, presentations, and advertisements) and guaranteed that they exceeded the expectations of our clients."
#       }
#     ],
#     "technologies": [
#       "HTML5",
#       "CSS3",
#       "JavaScript",
#       "React"
#     ]
#   }
# }

sample_data = {
  "user": {
    "name": "Barry Lucero",
    "title": "Web-Designer",
    "photo": "images/Photo.png",
    "location": "2207 Beach Avenue, Los Angeles",
    "email": "barry@design",
    "phone": "(914) 479-6342",
    "website": "www.barry.design",
    "profile": "Graphic designer with +8 years of experience in branding and print design. Skilled at Adobe Creative Suite (Photoshop, Illustrator, InDesign) as well as sketching and hand drawing. Supervised 23 print design projects that resulted in increased branding awareness by 30%.",
    "education": [
      {
        "institution": "Los Angeles University",
        "start_date": "2009",
        "end_date": "2013",
        "degree": "Bachelor of Fine Arts in Graphic Design, GPA: 3.1/4.0"
      },
      {
        "institution": "New York University",
        "start_date": "2013",
        "end_date": "2015",
        "degree": "Master of Graphic Design, GPA: 3.5/4.0"
      }
    ],
    "experience": [
      {
        "title": "UI Designer",
        "company": "Market Studios",
        "start_date": "2015",
        "end_date": "2016",
        "location": "Los Angeles",
        "description": "Created design for newsletters, promotional materials, and sales collateral. Collaborated with product teams to deliver cohesive branding."
      },
      {
        "title": "Graphic Designer",
        "company": "FireWeb",
        "start_date": "2016",
        "end_date": "2018",
        "location": "New York",
        "description": "Created new design themes for marketing and collateral materials. Worked on branding, advertising campaigns, and corporate identity."
      },
      {
        "title": "Senior Designer",
        "company": "STech",
        "start_date": "2018",
        "end_date": "Present",
        "location": "San Francisco",
        "description": "Developed numerous marketing programs (logos, brochures, newsletters, infographics, presentations) and guaranteed that they exceeded client expectations."
      }
    ],
    "skills": {
      "professional": [
        "Figma",
        "Sketch App",
        "Adobe Photoshop",
        "Adobe Illustrator",
        "HTML/CSS",
        "Premiere Pro",
        "After Effects"
      ],
      "personal": [
        "Communication",
        "Time management",
        "Teamwork",
        "Creativity",
        "Attention to detail",
        "Meeting deadlines"
      ]
    }
  }
}



@app.get("/render-preview/{id}", response_class=HTMLResponse)
def render_preview(id, request: Request):
    static_dir = os.path.join(BASE_DIR, "static")
    photo_path = os.path.join(static_dir, sample_data["user"]["photo"])

    # Embed image as base64
    if sample_data["user"]["photo"] and os.path.exists(photo_path):
        with open(photo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        photo_base64 = f"data:image/png;base64,{encoded_string}"
    else:
        photo_base64 = ""

    context = {
        "request": request,
        **sample_data,
        "photo_base64": photo_base64
    }
    # logger.info(f"Context: {context}")
    return templates.TemplateResponse(f'template0{id}.jinja2', context)



@app.get("/generate-pdf")
async def generate_pdf(request: Request):

    static_dir = os.path.join(BASE_DIR, "static")
    photo_path = os.path.join(static_dir, sample_data["user"]["photo"])

    # Embed image as base64
    if sample_data["user"]["photo"] and os.path.exists(photo_path):
        with open(photo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        photo_base64 = f"data:image/png;base64,{encoded_string}"
    else:
        photo_base64 = ""

    context = {
        "request": request,
        **sample_data,
        "photo_base64": photo_base64
    }

    html_content = templates.get_template("template03.jinja2").render(context)
    pdf = HTML(string=html_content, base_url=BASE_DIR).write_pdf()

    save_dir = os.path.join(BASE_DIR, "generated_resumes")
    os.makedirs(save_dir, exist_ok=True)
    filename = f"resume_{uuid4().hex}.pdf"
    file_path = os.path.join(save_dir, filename)

    with open(file_path, "wb") as pdf_file:
        pdf_file.write(pdf)

    logger.info(f"Resume saved at: {file_path}")

    return {"status": "PDF generated", "file_path": file_path}
