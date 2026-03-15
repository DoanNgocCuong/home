"""
Alert Context - Immutable context object for alerts

Mục đích:
    Immutable dataclass để chứa thông tin alert, đảm bảo:
    - SRP: Chỉ chứa alert data
    - Immutability: Prevent accidental modification
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional
from .alert_types import AlertType, AlertLevel


@dataclass(frozen=True)
class AlertContext:
    """
    Immutable context object for alerts
    
    Follows:
    - SRP: Only holds alert data
    - Immutable: Prevents accidental modification
    """
    alert_type: AlertType
    level: AlertLevel
    message: str
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    request_id: Optional[str] = None
    conversation_id: Optional[str] = None
    
    def get_alert_key(self) -> str:
        """
        Generate unique key for rate limiting/deduplication
        
        Returns:
            str: Unique key based on alert type and important context fields
        """
        key = str(self.alert_type.value)
        
        # Add important context fields
        important_fields = ["provider", "model", "service", "host", "path"]
        context_parts = [
            f"{k}={v}" for k, v in self.context.items()
            if k in important_fields and v
        ]
        if context_parts:
            key = f"{key}_{'_'.join(context_parts)}"
        
        return key
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization
        
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        return {
            "alert_type": self.alert_type.value,
            "level": self.level.value,
            "message": self.message,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "request_id": self.request_id,
            "conversation_id": self.conversation_id,
        }

