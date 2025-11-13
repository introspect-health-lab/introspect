from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter(
    tags=['Frontend']
)

# Setup Jinja2 templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Landing page for introspect"""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/signin", response_class=HTMLResponse)
async def signin(request: Request):
    """Sign in page"""
    return templates.TemplateResponse("signin.html", {"request": request})


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    """Sign up page"""
    return templates.TemplateResponse("signup.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/patients", response_class=HTMLResponse)
async def patients(request: Request):
    """Patients management page"""
    return templates.TemplateResponse("patients.html", {"request": request})


@router.get("/analyze", response_class=HTMLResponse)
async def analyze(request: Request):
    """Blood smear analysis page"""
    return templates.TemplateResponse("analyze.html", {"request": request})

