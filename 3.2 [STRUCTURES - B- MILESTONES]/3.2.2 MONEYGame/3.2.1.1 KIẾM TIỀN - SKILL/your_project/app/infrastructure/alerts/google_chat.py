"""
Google Chat Webhook Client

Mục đích:
    Client để gửi messages đến Google Chat webhook.
    Hỗ trợ format text đơn giản và card format (rich message).

Features:
    - Simple text message
    - Card format với color coding
    - Error handling với retry
    - Async non-blocking send
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class GoogleChatClient:
    """
    Client để gửi alerts đến Google Chat webhook
    
    Attributes:
        webhook_url: URL của Google Chat webhook
        timeout: Timeout cho HTTP request (default: 5s)
        max_retries: Số lần retry tối đa (default: 3)
    """
    
    def __init__(
        self,
        webhook_url: str,
        timeout: float = 5.0,
        max_retries: int = 3
    ):
        """
        Initialize Google Chat client
        
        Args:
            webhook_url: URL của Google Chat webhook
            timeout: Timeout cho HTTP request (seconds)
            max_retries: Số lần retry tối đa khi gửi fail
        """
        self.webhook_url = webhook_url
        self.timeout = timeout
        self.max_retries = max_retries
    
    async def send_text(self, text: str) -> bool:
        """
        Gửi text message đơn giản đến Google Chat
        
        Args:
            text: Nội dung message cần gửi
            
        Returns:
            bool: True nếu gửi thành công, False nếu fail
        """
        payload = {"text": text}
        return await self._send(payload)
    
    async def send_card(
        self,
        title: str,
        message: str,
        level: str = "info",
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Gửi card message (rich format) đến Google Chat
        
        Args:
            title: Tiêu đề của card
            message: Nội dung message chính
            level: Mức độ (critical/high/medium/low) - dùng để set color
            context: Dict chứa context bổ sung (sẽ format thành text)
            
        Returns:
            bool: True nếu gửi thành công, False nếu fail
        """
        # Map level to emoji và color
        level_map = {
            "critical": {"emoji": "🚨", "color": "RED"},
            "high": {"emoji": "⚠️", "color": "ORANGE"},
            "medium": {"emoji": "⚡", "color": "YELLOW"},
            "low": {"emoji": "ℹ️", "color": "BLUE"}
        }
        
        level_info = level_map.get(level.lower(), level_map["medium"])
        emoji = level_info["emoji"]
        color = level_info["color"]
        
        # Format title với emoji
        title_with_emoji = f"{emoji} {title}"
        
        # Format context nếu có
        context_text = ""
        if context:
            context_items = []
            for key, value in context.items():
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 100:
                    value_str = value_str[:100] + "..."
                context_items.append(f"<b>{key}:</b> {value_str}")
            context_text = "<br>".join(context_items)
        
        # Combine message và context
        full_message = message
        if context_text:
            full_message = f"{message}<br><br>{context_text}"
        
        # Format timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build card payload
        payload = {
            "cards": [{
                "header": {
                    "title": title_with_emoji,
                    "subtitle": timestamp
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
        
        return await self._send(payload)
    
    async def _send(self, payload: Dict[str, Any]) -> bool:
        """
        Gửi payload đến Google Chat webhook với retry logic
        
        Args:
            payload: Payload JSON để gửi
            
        Returns:
            bool: True nếu gửi thành công, False nếu fail
        """
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        # Retry logic
        last_error = None
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.post(
                        self.webhook_url,
                        json=payload,
                        headers=headers
                    ) as response:
                        if response.status == 200:
                            logger.debug(f"Google Chat alert sent successfully (attempt {attempt + 1})")
                            return True
                        else:
                            error_text = await response.text()
                            logger.warning(
                                f"Google Chat alert failed with status {response.status} "
                                f"(attempt {attempt + 1}/{self.max_retries}): {error_text}"
                            )
                            last_error = f"Status {response.status}: {error_text}"
                            
            except asyncio.TimeoutError:
                logger.warning(
                    f"Google Chat alert timeout (attempt {attempt + 1}/{self.max_retries})"
                )
                last_error = "Timeout"
                
            except Exception as e:
                logger.error(
                    f"Google Chat alert error (attempt {attempt + 1}/{self.max_retries}): {str(e)}",
                    exc_info=True
                )
                last_error = str(e)
            
            # Wait before retry (exponential backoff)
            if attempt < self.max_retries - 1:
                wait_time = 0.5 * (2 ** attempt)  # 0.5s, 1s, 2s
                await asyncio.sleep(wait_time)
        
        # All retries failed
        logger.error(f"Google Chat alert failed after {self.max_retries} attempts. Last error: {last_error}")
        return False

