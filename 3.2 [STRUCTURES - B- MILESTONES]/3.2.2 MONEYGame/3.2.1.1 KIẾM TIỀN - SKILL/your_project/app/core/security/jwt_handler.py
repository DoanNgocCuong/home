"""
JWT token handling.

Best Practices:
- Use strong algorithms (HS256 or RS256)
- Include expiration
- Store user context in claims
- Never store sensitive data in token
"""

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import get_settings
from app.core.exceptions import UnauthorizedError

settings = get_settings()


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """
    Create JWT access token.

    Args:
        subject: User ID or identifier
        expires_delta: Custom expiration (default: from settings)
        additional_claims: Extra claims (e.g., role, permissions)

    Returns:
        Encoded JWT token
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta

    claims = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    if additional_claims:
        claims.update(additional_claims)

    return jwt.encode(
        claims,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(subject: str) -> str:
    """Create JWT refresh token with longer expiration."""
    expires_delta = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    return create_access_token(
        subject=subject,
        expires_delta=expires_delta,
        additional_claims={"type": "refresh"},
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and validate JWT token.

    Raises:
        UnauthorizedError: If token is invalid or expired

    Returns:
        Token payload (claims)
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except InvalidTokenError as e:
        raise UnauthorizedError(f"Invalid token: {str(e)}")


def verify_token(token: str) -> dict[str, Any]:
    """
    Verify token and return payload.

    Shorthand for decode_token with explicit error handling.
    """
    return decode_token(token)
