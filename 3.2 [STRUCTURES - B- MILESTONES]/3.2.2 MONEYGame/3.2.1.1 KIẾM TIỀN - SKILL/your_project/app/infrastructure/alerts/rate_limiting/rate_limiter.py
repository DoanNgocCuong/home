"""
Rate Limiter - Rate limiter for alerts by level

Mục đích:
    Rate limiting logic cho alerts theo level:
    - CRITICAL: No limit
    - HIGH: 5 alerts / 5 minutes
    - MEDIUM: 3 alerts / 10 minutes
    - LOW: 1 alert / 30 minutes
"""

from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
from ..alert_types import AlertLevel


class RateLimiter:
    """
    Rate limiter for alerts by level
    
    Strategy:
    - CRITICAL: No limit
    - HIGH: 5 alerts / 5 minutes
    - MEDIUM: 3 alerts / 10 minutes
    - LOW: 1 alert / 30 minutes
    """
    
    CONFIG = {
        AlertLevel.CRITICAL: {"max_alerts": None, "time_window": None},
        AlertLevel.HIGH: {"max_alerts": 5, "time_window": 300},
        AlertLevel.MEDIUM: {"max_alerts": 3, "time_window": 600},
        AlertLevel.LOW: {"max_alerts": 1, "time_window": 1800}
    }
    
    def __init__(self):
        """Initialize rate limiter"""
        self._history: Dict[str, List[datetime]] = defaultdict(list)
    
    def check_and_record(self, alert_key: str, level: AlertLevel) -> bool:
        """
        Check if alert is within rate limit and record it
        
        Args:
            alert_key: Unique key for alert type
            level: Alert severity level
            
        Returns:
            bool: True if rate limited (should NOT send), False if OK to send
        """
        config = self.CONFIG.get(level)
        
        # No limit for CRITICAL
        if not config or config["max_alerts"] is None:
            self._record(alert_key)
            return False
        
        max_alerts = config["max_alerts"]
        time_window = config["time_window"]
        
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=time_window)
        
        # Clean old entries
        self._history[alert_key] = [
            ts for ts in self._history[alert_key]
            if ts > cutoff_time
        ]
        
        # Check if exceeded
        if len(self._history[alert_key]) >= max_alerts:
            return True  # Rate limited
        
        # Record and allow
        self._record(alert_key)
        return False
    
    def _record(self, alert_key: str):
        """Record alert timestamp"""
        self._history[alert_key].append(datetime.now())

