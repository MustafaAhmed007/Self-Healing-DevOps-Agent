import hashlib
import hmac
from app.webhooks import verify_signature


def test_signed_webhook():
    body = b'{"action":"opened"}'
    secret = "test-secret"
    sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_signature(body, sig, secret)


def test_invalid_webhook():
    assert not verify_signature(b"x", "sha256=bad", "test-secret")
