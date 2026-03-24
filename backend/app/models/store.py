import secrets
from datetime import datetime
from typing import Optional

# Simulated user store - in a real app this would be a database
USERS: dict[str, dict] = {
    "alice": {
        "username": "alice",
        "password": "password123",
        "balance": 10000.00,
        "email": "alice@example.com",
    },
    "bob": {
        "username": "bob",
        "password": "password123",
        "balance": 5000.00,
        "email": "bob@example.com",
    },
}

# Simulated comment store
# Each comment has: id, author, content, safe_content, created_at
COMMENTS_UNSAFE: list[dict] = []
COMMENTS_SAFE: list[dict] = []

# Simulated transfer log
TRANSFER_LOG: list[dict] = []


def get_user(username: str) -> Optional[dict]:
    return USERS.get(username)


def verify_password(username: str, password: str) -> bool:
    user = USERS.get(username)
    if not user:
        return False
    return user["password"] == password


def add_comment_unsafe(author: str, content: str) -> dict:
    comment = {
        "id": secrets.token_hex(6),
        "author": author,
        "content": content,
        "created_at": datetime.utcnow().isoformat(),
    }
    COMMENTS_UNSAFE.append(comment)
    return comment


def add_comment_safe(author: str, raw_content: str, sanitized_content: str) -> dict:
    comment = {
        "id": secrets.token_hex(6),
        "author": author,
        "content": sanitized_content,
        "raw_content": raw_content,
        "created_at": datetime.utcnow().isoformat(),
    }
    COMMENTS_SAFE.append(comment)
    return comment


def get_comments_unsafe() -> list[dict]:
    return COMMENTS_UNSAFE


def get_comments_safe() -> list[dict]:
    return COMMENTS_SAFE


def log_transfer(sender: str, recipient: str, amount: float, method: str) -> dict:
    entry = {
        "id": secrets.token_hex(6),
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "method": method,
        "created_at": datetime.utcnow().isoformat(),
    }
    TRANSFER_LOG.append(entry)
    return entry


def get_transfer_log() -> list[dict]:
    return TRANSFER_LOG