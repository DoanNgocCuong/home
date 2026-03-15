"""
Alert System Module

Mục đích:
    Module này cung cấp hệ thống alerting cho toàn bộ ứng dụng.
    Hỗ trợ gửi alerts đến Google Chat với rate limiting và deduplication.

Components:
    - alert_manager: Alert manager với rate limiting
    - alert_types: Enum định nghĩa các loại alert (47 types)
    - alert_context: Immutable context object
    - transports: Transport implementations (GoogleChat, Log)
    - formatters: Formatter implementations (GoogleChat)
    - rate_limiting: Rate limiting và deduplication logic
"""

from .alert_manager import AlertManager, get_alert_manager
from .alert_types import AlertLevel, AlertType
from .alert_context import AlertContext
from .alert_level_mapping import get_default_level

# Backward compatibility: Export GoogleChatClient from old location
try:
    from .google_chat import GoogleChatClient
except ImportError:
    # If google_chat.py is removed, import from transports
    from .transports.google_chat_transport import GoogleChatTransport as GoogleChatClient

__all__ = [
    "AlertManager",
    "get_alert_manager",
    "AlertLevel",
    "AlertType",
    "AlertContext",
    "get_default_level",
    "GoogleChatClient",  # Backward compatibility
]

