"""
Log Transport - Fallback transport that logs alerts

Mục đích:
    Fallback transport khi không có webhook URL configured.
    Logs alerts to standard logging system.
"""

import logging
from .base_transport import BaseTransport, AlertMessage

logger = logging.getLogger(__name__)


class LogTransport(BaseTransport):
    """
    Fallback transport that logs alerts
    
    Used when no webhook URL is configured or as fallback
    """
    
    def is_available(self) -> bool:
        """Always available"""
        return True
    
    async def send(self, message: AlertMessage) -> bool:
        """
        Log alert message
        
        Args:
            message: AlertMessage object
            
        Returns:
            bool: Always True (logging always succeeds)
        """
        try:
            alert_type = message.metadata.get("alert_type", "unknown")
            level = message.metadata.get("level", "unknown")
            
            logger.warning(
                f"[ALERT] {alert_type} ({level}): {message.payload}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to log alert: {e}")
            return False

