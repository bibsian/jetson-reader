"""Configuration settings for the reading assistant."""

from dataclasses import dataclass

@dataclass
class WandConfig:
    """HSV color range for wand tracking."""
    # Default: bright red wand tip
    hue_low: int = 0
    hue_high: int = 10
    sat_low: int = 120
    sat_high: int = 255
    val_low: int = 100
    val_high: int = 255
    
    # Minimum contour area to consider (filters noise)
    min_area: int = 100

@dataclass
class GestureConfig:
    """Settings for double-tap detection."""
    # Max time between taps (seconds)
    double_tap_window: float = 0.5
    # Min vertical movement to count as a tap (pixels)
    tap_threshold: int = 20
    # How many frames wand must be stationary to register tap
    stationary_frames: int = 3

@dataclass 
class Config:
    """Main configuration."""
    wand: WandConfig = None
    gesture: GestureConfig = None
    camera_index: int = 0
    
    def __post_init__(self):
        self.wand = self.wand or WandConfig()
        self.gesture = self.gesture or GestureConfig()
