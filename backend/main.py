from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.routers import comments, auth, csrf_demo, xss_demo

app = FastAPI(
    title="Security Showcase API",
    description="A hands-on demonstration of CSRF and XSS vulnerabilities and their mitigations.",
    version="1.0.0",
)
