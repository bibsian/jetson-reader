"""Double-tap gesture detection from wand movement."""

import time
from .config import GestureConfig

class GestureDetector:
    """Detects double-tap gestures from wand position history."""
    
    def __init__(self, config: GestureConfig = None):
        self.config = config or GestureConfig()
        self.history: list[tuple[int, int, float]] = []  # (x, y, timestamp)
        self.last_tap_time: float = 0
        self.tap_count: int = 0
    
    def update(self, position: tuple[int, int] | None) -> tuple[int, int] | None:
        """
        Process wand position, return tap location (x, y) if double-tap detected.
        """
        now = time.time()
        
        # Reset tap count if window expired
        if now - self.last_tap_time > self.config.double_tap_window:
            self.tap_count = 0
        
        if position is None:
            self.history.clear()
            return None
        
        x, y = position
        self.history.append((x, y, now))
        
        # Keep only recent history (last 0.5 seconds)
        self.history = [(hx, hy, ht) for hx, hy, ht in self.history if now - ht < 0.5]
        
        # Detect tap: downward then upward motion
        if self._detect_tap():
            self.tap_count += 1
            self.last_tap_time = now
            
            if self.tap_count >= 2:
                self.tap_count = 0
                return (x, y)
        
        return None
    
    def _detect_tap(self) -> bool:
        """Check if recent motion indicates a tap."""
        if len(self.history) < 5:
            return False
        
        # Look for down-up pattern in y coordinates
        ys = [h[1] for h in self.history[-10:]]
        
        # Find if there's a significant dip
        min_y_idx = ys.index(min(ys))
        if min_y_idx == 0 or min_y_idx == len(ys) - 1:
            return False
        
        before_dip = ys[0]
        at_dip = ys[min_y_idx]
        after_dip = ys[-1]
        
        # Check for significant downward then upward motion
        went_down = before_dip - at_dip > self.config.tap_threshold
        went_up = after_dip - at_dip > self.config.tap_threshold
        
        return went_down and went_up
