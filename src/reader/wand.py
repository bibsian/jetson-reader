"""Wand tracking using OpenCV HSV color detection."""

import cv2
import numpy as np
from .config import WandConfig

class WandTracker:
    """Tracks a colored wand tip in camera frames."""
    
    def __init__(self, config: WandConfig = None):
        self.config = config or WandConfig()
        self.position: tuple[int, int] | None = None
    
    def update(self, frame: np.ndarray) -> tuple[int, int] | None:
        """
        Process a frame and return wand position (x, y) or None if not found.
        """
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for wand color
        lower = np.array([self.config.hue_low, self.config.sat_low, self.config.val_low])
        upper = np.array([self.config.hue_high, self.config.sat_high, self.config.val_high])
        mask = cv2.inRange(hsv, lower, upper)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            self.position = None
            return None
        
        # Find largest contour above minimum area
        valid = [c for c in contours if cv2.contourArea(c) >= self.config.min_area]
        if not valid:
            self.position = None
            return None
        
        largest = max(valid, key=cv2.contourArea)
        
        # Get centroid
        M = cv2.moments(largest)
        if M["m00"] == 0:
            self.position = None
            return None
        
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        self.position = (cx, cy)
        return self.position
