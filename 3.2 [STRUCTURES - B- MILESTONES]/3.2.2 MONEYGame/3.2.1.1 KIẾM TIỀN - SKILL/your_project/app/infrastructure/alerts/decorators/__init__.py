"""
Alert Decorators Module

Mục đích:
    Cung cấp decorators để tự động gửi alerts khi có errors hoặc timeouts
"""

from .alert_decorator import alert_on_error

__all__ = [
    "alert_on_error",
]

