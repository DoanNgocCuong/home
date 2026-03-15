"""
Base Transport - Abstract base class for alert transports

Mục đích:
    Abstract base class cho alert transports, đảm bảo:
    - OCP: New transports can be added without modifying existing code
    - LSP: All implementations can substitute this base class
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class AlertMessage:
    """
    Message object ready for transport
    
    Attributes:
        payload: Payload dictionary ready for transport
        metadata: Additional metadata (alert_type, level, etc.)
    """
    def __init__(self, payload: Dict[str, Any], metadata: Dict[str, Any] = None):
        self.payload = payload
        self.metadata = metadata or {}


class BaseTransport(ABC):
    """
    Abstract base class for alert transports
    
    Follows:
    - OCP: New transports can be added without modifying existing code
    - LSP: All implementations can substitute this base class
    """
    
    @abstractmethod
    async def send(self, message: AlertMessage) -> bool:
        """
        Send alert message
        
        Args:
            message: AlertMessage object ready for transport
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if transport is configured and available
        
        Returns:
            bool: True if transport is available, False otherwise
        """
        pass


class TransportError(Exception):
    """Base exception for transport errors"""
    pass

