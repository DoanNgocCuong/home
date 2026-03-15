"""
Google Chat Formatter - Format AlertContext into Google Chat Card format

Mục đích:
    Format AlertContext thành Google Chat Card format với:
    - Color-coded cards by severity
    - Structured context display
    - Timestamp and metadata
"""

from datetime import datetime
from typing import Any, Dict
from .base_formatter import BaseFormatter
from ..alert_context import AlertContext
from ..transports.base_transport import AlertMessage


class GoogleChatFormatter(BaseFormatter):
    """
    Format AlertContext into Google Chat Card format
    
    Features:
    - Color-coded cards by severity
    - Structured context display
    - Timestamp and metadata
    """
    
    LEVEL_MAP = {
        "critical": {"emoji": "🚨", "color": "RED"},
        "high": {"emoji": "⚠️", "color": "ORANGE"},
        "medium": {"emoji": "⚡", "color": "YELLOW"},
        "low": {"emoji": "ℹ️", "color": "BLUE"}
    }
    
    def format(self, context: AlertContext) -> AlertMessage:
        """
        Format AlertContext into Google Chat card message
        
        Args:
            context: AlertContext with alert details
            
        Returns:
            AlertMessage ready for Google Chat transport
        """
        level_info = self.LEVEL_MAP.get(context.level.value, self.LEVEL_MAP["medium"])
        emoji = level_info["emoji"]
        
        # Format title
        title = f"{emoji} {context.level.value.upper()}: {context.alert_type.value.replace('_', ' ').title()}"
        
        # Format context
        context_text = self._format_context(context.context)
        
        # Build full message
        full_message = context.message
        if context_text:
            full_message = f"{context.message}<br><br>{context_text}"
        
        # Build card payload
        payload = {
            "cards": [{
                "header": {
                    "title": title,
                    "subtitle": context.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
                },
                "sections": [{
                    "widgets": [{
                        "textParagraph": {
                            "text": full_message
                        }
                    }]
                }]
            }]
        }
        
        return AlertMessage(
            payload=payload,
            metadata={
                "alert_type": context.alert_type.value,
                "level": context.level.value
            }
        )
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """
        Format context dictionary as HTML
        
        Args:
            context: Context dictionary
            
        Returns:
            str: Formatted HTML string
        """
        if not context:
            return ""
        
        items = []
        for key, value in context.items():
            # Truncate long values
            value_str = str(value)
            if len(value_str) > 200:
                value_str = value_str[:200] + "..."
            items.append(f"<b>{key}:</b> {value_str}")
        
        return "<br>".join(items)

