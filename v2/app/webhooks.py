from __future__ import annotations

import hashlib
import hmac
import os
from fastapi import APIRouter, Header, HTTPException, Request

router = APIRouter(prefix="/v1/webhooks", tags=["webhooks"])


def verify_signature(body: bytes, signature: str | None, secret: str | None = None) -> bool:
    secret = secret or os.getenv("GITHUB_WEBHOOK_SECRET")
    if not secret or not signature or not signature.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/github")
async def github_webhook(request: Request, x_hub_signature_256: str | None = Header(default=None)):
    body = await request.body()
    if not verify_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="invalid webhook signature")
    return {"accepted": True, "event": request.headers.get("x-github-event", "unknown")}
