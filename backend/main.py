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

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
    same_site="lax",
    https_only=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(comments.router, prefix="/api/comments", tags=["comments"])
app.include_router(csrf_demo.router, prefix="/api/csrf", tags=["csrf"])
app.include_router(xss_demo.router, prefix="/api/xss", tags=["xss"])


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Security Showcase API is running"}