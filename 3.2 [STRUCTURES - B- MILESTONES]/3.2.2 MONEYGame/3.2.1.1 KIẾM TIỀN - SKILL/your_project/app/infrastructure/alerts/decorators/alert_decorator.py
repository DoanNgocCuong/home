"""
Alert Decorator - Decorator to send alert on function error or timeout

Mục đích:
    Decorator để tự động gửi alerts khi function:
    - Timeout
    - Raise exception
"""

import functools
import asyncio
import time
import logging
from typing import Optional, Callable, Any
from ..alert_types import AlertType, AlertLevel
from ..alert_manager import get_alert_manager

logger = logging.getLogger(__name__)


def alert_on_error(
    alert_type: AlertType,
    level: AlertLevel = AlertLevel.HIGH,
    timeout: Optional[float] = None,
    message_prefix: str = "[doancuong]"
):
    """
    Decorator to send alert on function error or timeout
    
    Usage:
        @alert_on_error(AlertType.WORKFLOW_EXECUTION_FAILURE, timeout=8.0)
        async def process_workflow(...):
            ...
    
    Args:
        alert_type: Type of alert to send
        level: Alert severity level
        timeout: Optional timeout in seconds
        message_prefix: Prefix for alert message
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            try:
                if timeout:
                    result = await asyncio.wait_for(
                        func(*args, **kwargs),
                        timeout=timeout
                    )
                else:
                    result = await func(*args, **kwargs)
                
                return result
                
            except asyncio.TimeoutError:
                duration = time.time() - start_time
                alert_manager = get_alert_manager()
                
                asyncio.create_task(
                    alert_manager.send_alert(
                        alert_type=alert_type,
                        level=level,
                        message=f"{message_prefix} {func.__name__} timeout after {duration:.2f}s",
                        context={
                            "function": func.__name__,
                            "timeout": f"{timeout}s",
                            "duration": f"{duration:.2f}s"
                        }
                    )
                )
                raise
                
            except Exception as e:
                duration = time.time() - start_time
                alert_manager = get_alert_manager()
                
                asyncio.create_task(
                    alert_manager.send_alert(
                        alert_type=alert_type,
                        level=level,
                        message=f"{message_prefix} {func.__name__} failed",
                        context={
                            "function": func.__name__,
                            "duration": f"{duration:.2f}s",
                            "error_type": type(e).__name__,
                            "error": str(e)[:500]
                        }
                    )
                )
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            # For sync functions, run in asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, we can't use run_until_complete
                    # Create task instead
                    task = asyncio.create_task(async_wrapper(*args, **kwargs))
                    # Wait for result (blocking)
                    return asyncio.run_coroutine_threadsafe(async_wrapper(*args, **kwargs), loop).result()
                else:
                    return loop.run_until_complete(async_wrapper(*args, **kwargs))
            except RuntimeError:
                # No event loop, create new one
                return asyncio.run(async_wrapper(*args, **kwargs))
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator

