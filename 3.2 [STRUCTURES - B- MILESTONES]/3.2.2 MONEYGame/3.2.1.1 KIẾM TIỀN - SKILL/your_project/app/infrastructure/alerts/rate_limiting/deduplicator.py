"""
Deduplicator - Deduplicate similar alerts within time window

Mục đích:
    Deduplicate similar alerts trong time window:
    - Group similar alerts within 60 seconds
    - First occurrence: send immediately
    - Second occurrence: send with count
    - Third+ occurrence: suppress, log only
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple


class Deduplicator:
    """
    Deduplicate similar alerts within time window
    
    Strategy:
    - Group similar alerts within 60 seconds
    - First occurrence: send immediately
    - Second occurrence: send with count
    - Third+ occurrence: suppress, log only
    """
    
    WINDOW_SECONDS = 60
    
    def __init__(self):
        """Initialize deduplicator"""
        self._cache: Dict[str, Tuple[datetime, int]] = {}
    
    def check_and_record(self, alert_key: str) -> Tuple[bool, int]:
        """
        Check if alert should be deduplicated
        
        Args:
            alert_key: Unique key for alert
            
        Returns:
            Tuple[bool, int]: (should_suppress, occurrence_count)
                - should_suppress: True if should NOT send (3rd+ occurrence)
                - occurrence_count: Number of occurrences in window
        """
        now = datetime.now()
        
        if alert_key in self._cache:
            last_time, count = self._cache[alert_key]
            
            # Within window
            if (now - last_time).total_seconds() < self.WINDOW_SECONDS:
                count += 1
                self._cache[alert_key] = (last_time, count)
                
                # 3rd+ occurrence: suppress
                if count > 2:
                    return (True, count)
                
                # 2nd occurrence: send with count
                return (False, count)
            
            # Outside window: reset
            self._cache[alert_key] = (now, 1)
            return (False, 1)
        
        # First occurrence
        self._cache[alert_key] = (now, 1)
        return (False, 1)
    
    def cleanup_old_entries(self):
        """Clean up entries older than window"""
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=self.WINDOW_SECONDS * 2)
        
        self._cache = {
            k: v for k, v in self._cache.items()
            if v[0] > cutoff
        }

