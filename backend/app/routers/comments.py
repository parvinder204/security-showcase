from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_comments():
    from app.models.store import get_comments_safe, get_comments_unsafe
    return {
        "vulnerable": get_comments_unsafe(),
        "safe": get_comments_safe(),
    }