"""
Base Formatter - Abstract base class for alert formatters

Mục đích:
    Abstract base class cho alert formatters, đảm bảo:
    - OCP: New formatters can be added without modifying existing code
    - LSP: All implementations can substitute this base class
"""

from abc import ABC, abstractmethod
from ..alert_context import AlertContext
from ..transports.base_transport import AlertMessage


class BaseFormatter(ABC):
    """
    Abstract base class for alert formatters
    
    Follows:
    - OCP: New formatters can be added without modifying existing code
    - LSP: All implementations can substitute this base class
    """
    
    @abstractmethod
    def format(self, context: AlertContext) -> AlertMessage:
        """
        Format AlertContext into AlertMessage ready for transport
        
        Args:
            context: AlertContext with alert details
            
        Returns:
            AlertMessage: Formatted message ready for transport
        """
        pass

