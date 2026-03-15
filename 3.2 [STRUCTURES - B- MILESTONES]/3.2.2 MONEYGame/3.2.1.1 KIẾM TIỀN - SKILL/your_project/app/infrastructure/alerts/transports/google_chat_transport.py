"""
Google Chat Transport - Google Chat Webhook transport implementation

Mục đích:
    Google Chat Webhook transport implementation với:
    - Async non-blocking send
    - Retry with exponential backoff
    - Timeout protection
"""

import aiohttp
import asyncio
import logging
from typing import Optional
from .base_transport import BaseTransport, AlertMessage, TransportError

logger = logging.getLogger(__name__)


class GoogleChatTransport(BaseTransport):
    """
    Google Chat Webhook transport implementation
    
    Features:
    - Async non-blocking send
    - Retry with exponential backoff
    - Timeout protection
    """
    
    def __init__(
        self,
        webhook_url: str,
        timeout: float = 5.0,
        max_retries: int = 3
    ):
        """
        Initialize Google Chat transport
        
        Args:
            webhook_url: Google Chat webhook URL
            timeout: HTTP request timeout (seconds)
            max_retries: Maximum retry attempts
        """
        self.webhook_url = webhook_url
        self.timeout = timeout
        self.max_retries = max_retries
    
    def is_available(self) -> bool:
        """Check if webhook URL is configured"""
        return bool(self.webhook_url)
    
    async def send(self, message: AlertMessage) -> bool:
        """
        Send alert to Google Chat webhook
        
        Args:
            message: AlertMessage with payload formatted for Google Chat
            
        Returns:
            bool: True if sent successfully
        """
        if not self.is_available():
            logger.warning("Google Chat webhook not configured")
            return False
        
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        last_error = None
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.post(
                        self.webhook_url,
                        json=message.payload,
                        headers=headers
                    ) as response:
                        if response.status == 200:
                            logger.debug(f"Alert sent successfully (attempt {attempt + 1})")
                            return True
                        else:
                            error_text = await response.text()
                            logger.warning(
                                f"Google Chat failed with status {response.status} "
                                f"(attempt {attempt + 1}/{self.max_retries}): {error_text}"
                            )
                            last_error = f"Status {response.status}"
                            
            except asyncio.TimeoutError:
                logger.warning(f"Google Chat timeout (attempt {attempt + 1}/{self.max_retries})")
                last_error = "Timeout"
                
            except Exception as e:
                logger.error(f"Google Chat error (attempt {attempt + 1}/{self.max_retries}): {e}")
                last_error = str(e)
            
            # Exponential backoff
            if attempt < self.max_retries - 1:
                wait_time = 0.5 * (2 ** attempt)
                await asyncio.sleep(wait_time)
        
        logger.error(f"Google Chat failed after {self.max_retries} attempts: {last_error}")
        return False

