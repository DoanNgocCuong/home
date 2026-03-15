"""
Send Alert Safe - Helper function to send alerts safely

Mục đích:
    Helper function để gửi alerts một cách an toàn với:
    - Auto-add [doancuong] prefix
    - Event loop handling
    - Error handling
    - Non-blocking send
"""

import asyncio
import logging
from typing import Dict, Any, Optional

from ..alert_types import AlertType, AlertLevel
from ..alert_manager import get_alert_manager

logger = logging.getLogger(__name__)

# Check if alerts enabled (singleton)
_ALERT_ENABLED = None


def _is_alert_enabled() -> bool:
    """Check if alert system is enabled"""
    global _ALERT_ENABLED
    if _ALERT_ENABLED is None:
        try:
            from ..alert_manager import get_alert_manager
            _ALERT_ENABLED = True
        except ImportError:
            _ALERT_ENABLED = False
    return _ALERT_ENABLED


def send_alert_safe(
    alert_type: AlertType,
    level: AlertLevel,
    message: str,
    context: Optional[Dict[str, Any]] = None,
    component: str = "unknown",
    request_id: Optional[str] = None,
    conversation_id: Optional[str] = None
) -> None:
    """
    Send alert safely (non-blocking, with error handling)
    
    Args:
        alert_type: Type of alert
        level: Alert level
        message: Alert message (will auto-add [doancuong] prefix if not present)
        context: Additional context
        component: Component name for logging
        request_id: Request ID for tracing
        conversation_id: Conversation ID if applicable
    """
    if not _is_alert_enabled():
        return
    
    try:
        alert_manager = get_alert_manager()
        
        # Auto-add [doancuong] prefix if not present
        if not message.startswith("[doancuong]"):
            message = f"[doancuong] {message}"
        
        # Ensure context has component
        final_context = context.copy() if context else {}
        final_context.setdefault("component", component)
        
        # Send alert (non-blocking)
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(
                    alert_manager.send_alert(
                        alert_type=alert_type,
                        level=level,
                        message=message,
                        context=final_context,
                        request_id=request_id,
                        conversation_id=conversation_id
                    )
                )
            else:
                # No running loop, schedule for later
                loop.call_soon_threadsafe(
                    lambda: asyncio.run(
                        alert_manager.send_alert(
                            alert_type=alert_type,
                            level=level,
                            message=message,
                            context=final_context,
                            request_id=request_id,
                            conversation_id=conversation_id
                        )
                    )
                )
        except RuntimeError:
            # No event loop, try to create one
            try:
                asyncio.run(
                    alert_manager.send_alert(
                        alert_type=alert_type,
                        level=level,
                        message=message,
                        context=final_context,
                        request_id=request_id,
                        conversation_id=conversation_id
                    )
                )
            except RuntimeError:
                logger.warning(f"[{component}] Cannot send alert - no event loop available")
    except Exception as e:
        logger.warning(f"[{component}] Failed to send alert: {e}", exc_info=True)

