from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.models.store import get_transfer_log, get_user, log_transfer

router = APIRouter()


class TransferRequest(BaseModel):
    recipient: str
    amount: float


class SecureTransferRequest(BaseModel):
    recipient: str
    amount: float
    csrf_token: str


@router.post("/transfer/vulnerable")
def transfer_vulnerable(payload: TransferRequest, request: Request):
    """
    This endpoint is intentionally vulnerable to CSRF.
    It relies only on session cookies with no CSRF token validation.
    An attacker can forge a cross-site request and this endpoint will accept it.
    """
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = get_user(username)

    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if payload.amount > user["balance"]:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    entry = log_transfer(
        sender=username,
        recipient=payload.recipient,
        amount=payload.amount,
        method="VULNERABLE (no CSRF protection)",
    )

    return {
        "message": f"Transfer of ${payload.amount} to {payload.recipient} completed.",
        "warning": "This transfer was processed without any CSRF validation.",
        "transfer_id": entry["id"],
    }


@router.post("/transfer/secure")
def transfer_secure(payload: SecureTransferRequest, request: Request):
    """
    This endpoint is protected against CSRF attacks.
    It validates the CSRF token from the request body against the one stored in the session.
    An attacker cannot read the session token from a different origin, so forged requests fail.
    """
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session_csrf_token = request.session.get("csrf_token")
    if not session_csrf_token or session_csrf_token != payload.csrf_token:
        raise HTTPException(
            status_code=403,
            detail="CSRF token validation failed. Request blocked.",
        )

    user = get_user(username)

    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if payload.amount > user["balance"]:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    entry = log_transfer(
        sender=username,
        recipient=payload.recipient,
        amount=payload.amount,
        method="SECURE (CSRF token validated)",
    )

    return {
        "message": f"Transfer of ${payload.amount} to {payload.recipient} completed.",
        "info": "This transfer was validated with a CSRF token.",
        "transfer_id": entry["id"],
    }


@router.get("/transfers")
def get_transfers(request: Request):
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")

    all_transfers = get_transfer_log()
    user_transfers = [t for t in all_transfers if t["sender"] == username]
    return user_transfers