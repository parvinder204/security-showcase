import bleach
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()

ALLOWED_TAGS = ["b", "i", "u", "em", "strong", "p", "br"]
ALLOWED_ATTRIBUTES: dict = {}


class CommentRequest(BaseModel):
    content: str


@router.post("/comment/vulnerable")
def post_comment_vulnerable(payload: CommentRequest, request: Request):
    """
    This endpoint is intentionally vulnerable to Stored XSS.
    User input is stored and returned without any sanitization.
    When the frontend renders this content as raw HTML, any injected scripts execute.
    """
    from app.models.store import add_comment_unsafe

    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    comment = add_comment_unsafe(author=username, content=payload.content)

    return {
        "comment": comment,
        "warning": "Content was stored without sanitization. XSS payloads will execute on render.",
    }


@router.post("/comment/secure")
def post_comment_secure(payload: CommentRequest, request: Request):
    """
    This endpoint is protected against XSS.
    Content is sanitized with bleach before being stored.
    Only a limited set of safe HTML tags are permitted.
    """
    from app.models.store import add_comment_safe

    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    sanitized = bleach.clean(
        payload.content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )

    comment = add_comment_safe(
        author=username,
        raw_content=payload.content,
        sanitized_content=sanitized,
    )

    return {
        "comment": comment,
        "info": "Content was sanitized before storage. Script tags and event handlers are stripped.",
    }


@router.get("/comments/vulnerable")
def get_comments_vulnerable():
    from app.models.store import get_comments_unsafe
    return get_comments_unsafe()


@router.get("/comments/secure")
def get_comments_secure():
    from app.models.store import get_comments_safe
    return get_comments_safe()