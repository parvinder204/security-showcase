import secrets

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.models.store import get_user, verify_password

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(payload: LoginRequest, request: Request):
    if not verify_password(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = get_user(payload.username)

    request.session["username"] = user["username"]
    request.session["csrf_token"] = secrets.token_hex(32)

    return {
        "username": user["username"],
        "email": user["email"],
        "balance": user["balance"],
        "csrf_token": request.session["csrf_token"],
    }


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}


@router.get("/me")
def get_current_user(request: Request):
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = get_user(username)
    return {
        "username": user["username"],
        "email": user["email"],
        "balance": user["balance"],
        "csrf_token": request.session.get("csrf_token"),
    }