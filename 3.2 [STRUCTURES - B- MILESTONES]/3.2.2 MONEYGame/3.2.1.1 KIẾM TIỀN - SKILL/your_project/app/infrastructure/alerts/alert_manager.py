"""
Alert Manager - Quản lý alerts với rate limiting và deduplication

Mục đích:
    Central Alert Manager với SOLID design:
    - Orchestrate alert flow
    - Apply rate limiting
    - Apply deduplication
    - Delegate to transport
    
Features:
    - Async non-blocking send
    - Pluggable transports
    - Pluggable formatters
"""

import asyncio
import logging
from typing import Any, Dict, Optional

from .alert_types import AlertType, AlertLevel
from .alert_context import AlertContext
from .transports.base_transport import BaseTransport
from .transports.google_chat_transport import GoogleChatTransport
from .transports.log_transport import LogTransport
from .formatters.base_formatter import BaseFormatter
from .formatters.google_chat_formatter import GoogleChatFormatter
from .rate_limiting.rate_limiter import RateLimiter
from .rate_limiting.deduplicator import Deduplicator

try:
    from app.common.config import settings
except ImportError:
    # Fallback nếu import fail
    import os
    class Settings:
        GOOGLE_CHAT_WEBHOOK_URL = os.getenv("GOOGLE_CHAT_WEBHOOK_URL", "")
    settings = Settings()

logger = logging.getLogger(__name__)


class AlertManager:
    """
    Central Alert Manager with SOLID design
    
    Responsibilities:
    - Orchestrate alert flow
    - Apply rate limiting
    - Apply deduplication
    - Delegate to transport
    
    Features:
    - Async non-blocking send
    - Pluggable transports
    - Pluggable formatters
    """
    
    def __init__(
        self,
        webhook_url: Optional[str] = None,
        transport: Optional[BaseTransport] = None,
        formatter: Optional[BaseFormatter] = None
    ):
        """
        Initialize AlertManager with DI
        
        Args:
            webhook_url: Google Chat webhook URL (for backward compatibility)
            transport: Custom transport (optional, uses GoogleChat/Log)
            formatter: Custom formatter (optional, uses GoogleChat)
        """
        # Get webhook URL from env hoặc parameter
        if not webhook_url:
            webhook_url = getattr(settings, "GOOGLE_CHAT_WEBHOOK_URL", None)
        
        # Setup transport
        if transport:
            self.transport = transport
        elif webhook_url:
            self.transport = GoogleChatTransport(webhook_url=webhook_url)
        else:
            self.transport = LogTransport()
            logger.warning("No webhook URL, alerts will be logged only")
        
        # Store webhook_url for backward compatibility
        self.webhook_url = webhook_url
        
        # Setup formatter
        self.formatter = formatter or GoogleChatFormatter()
        
        # Setup rate limiting & deduplication
        self.rate_limiter = RateLimiter()
        self.deduplicator = Deduplicator()
        
        # Lock để thread-safe (for backward compatibility)
        self._lock = asyncio.Lock()
    
    async def send_alert(
        self,
        alert_type: AlertType,
        level: AlertLevel,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
        conversation_id: Optional[str] = None
    ) -> bool:
        """
        Send alert with rate limiting and deduplication
        
        Args:
            alert_type: Type of alert
            level: Severity level
            message: Alert message
            context: Additional context
            request_id: Request ID for tracing
            conversation_id: Conversation ID if applicable
            
        Returns:
            bool: True if sent or properly handled, False if error
        """
        # Create context object
        alert_context = AlertContext(
            alert_type=alert_type,
            level=level,
            message=message,
            context=context or {},
            request_id=request_id,
            conversation_id=conversation_id
        )
        
        alert_key = alert_context.get_alert_key()
        
        # Check rate limit
        if self.rate_limiter.check_and_record(alert_key, level):
            logger.debug(f"Alert rate limited: {alert_type.value}")
            return True  # Properly handled (rate limited)
        
        # Check deduplication
        should_suppress, count = self.deduplicator.check_and_record(alert_key)
        
        if should_suppress:
            logger.debug(f"Alert deduplicated (count={count}): {alert_type.value}")
            return True  # Properly handled (deduplicated)
        
        # Add count to message if deduplicated
        if count > 1:
            alert_context = AlertContext(
                alert_type=alert_type,
                level=level,
                message=f"{message} (x{count} occurrences in last minute)",
                context={**alert_context.context, "occurrences": count},
                request_id=request_id,
                conversation_id=conversation_id
            )
        
        # Format and send
        try:
            formatted_message = self.formatter.format(alert_context)
            success = await self.transport.send(formatted_message)
            
            if success:
                logger.info(f"Alert sent: {alert_type.value} ({level.value})")
            else:
                logger.error(f"Failed to send alert: {alert_type.value}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending alert: {e}", exc_info=True)
            return False
    
    def send_alert_fire_and_forget(
        self,
        alert_type: AlertType,
        level: AlertLevel,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
        conversation_id: Optional[str] = None
    ) -> asyncio.Task:
        """
        Fire-and-forget alert (non-blocking)
        
        Returns:
            asyncio.Task: Task object (can be ignored)
        """
        return asyncio.create_task(
            self.send_alert(
                alert_type=alert_type,
                level=level,
                message=message,
                context=context,
                request_id=request_id,
                conversation_id=conversation_id
            )
        )


# Singleton accessor (backward compatibility)
_alert_manager: Optional[AlertManager] = None


def get_alert_manager(webhook_url: Optional[str] = None) -> AlertManager:
    """
    Get or create AlertManager singleton
    
    Args:
        webhook_url: Optional webhook URL để override default từ settings
        
    Returns:
        AlertManager instance
    """
    global _alert_manager
    
    if _alert_manager is None:
        # Try to get from settings
        try:
            from app.common.config import settings
            webhook_url = webhook_url or getattr(settings, "GOOGLE_CHAT_WEBHOOK_URL", None)
        except ImportError:
            import os
            webhook_url = webhook_url or os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
        
        _alert_manager = AlertManager(webhook_url=webhook_url)
    elif webhook_url and _alert_manager.webhook_url != webhook_url:
        # Update webhook URL nếu được provide
        _alert_manager.webhook_url = webhook_url
        _alert_manager.transport = GoogleChatTransport(webhook_url=webhook_url)
    
    return _alert_manager
