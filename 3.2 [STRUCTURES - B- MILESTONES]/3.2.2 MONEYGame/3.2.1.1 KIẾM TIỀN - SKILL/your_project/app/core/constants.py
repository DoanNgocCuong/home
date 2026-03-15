"""
App-wide constants.

Best Practices:
- Use ALL_CAPS for constants
- Group related constants with comments
- Document why constants exist
"""

# ============== Pagination ==============
MAX_PAGE_SIZE: int = 100
DEFAULT_PAGE_SIZE: int = 20

# ============== Timeouts (seconds) ==============
DEFAULT_REQUEST_TIMEOUT: int = 30
LONG_REQUEST_TIMEOUT: int = 300  # For async operations
EXTERNAL_API_TIMEOUT: int = 10

# ============== Retry ==============
MAX_RETRY_ATTEMPTS: int = 3
RETRY_BACKOFF_FACTOR: float = 2.0  # Exponential backoff

# ============== Cache TTL (seconds) ==============
CACHE_TTL_SHORT: int = 60       # 1 minute
CACHE_TTL_MEDIUM: int = 3600     # 1 hour
CACHE_TTL_LONG: int = 86400     # 24 hours
CACHE_TTL_USER_PROFILE: int = 1800  # 30 minutes

# ============== Business Rules ==============
MIN_PASSWORD_LENGTH: int = 8
MAX_PASSWORD_LENGTH: int = 128
PASSWORD_COMPLEXITY_REGEX: str = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"

MAX_FILE_SIZE_MB: int = 10
ALLOWED_FILE_EXTENSIONS: list[str] = [".jpg", ".jpeg", ".png", ".pdf"]

# ============== API Rate Limits ==============
RATE_LIMIT_AUTH: int = 5         # per minute - login attempts
RATE_LIMIT_API: int = 60        # per minute - general API
RATE_LIMIT_UPLOAD: int = 10     # per minute - file uploads
