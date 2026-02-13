"""OCR integration using Tesseract."""

import pytesseract
import numpy as np
from dataclasses import dataclass

@dataclass
class WordBox:
    """A detected word with its bounding box."""
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float

class OCREngine:
    """Extracts text from images using Tesseract."""
    
    def __init__(self):
        self._cached_boxes: list[WordBox] = []
        self._cache_valid = False
    
    def process_frame(self, frame: np.ndarray) -> list[WordBox]:
        """
        Run OCR on frame, return list of detected words with positions.
        """
        data = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
        
        boxes = []
        for i, word in enumerate(data['text']):
            word = word.strip()
            if not word:
                continue
            
            conf = int(data['conf'][i])
            if conf < 0:  # Tesseract uses -1 for invalid
                continue
            
            boxes.append(WordBox(
                text=word,
                x=data['left'][i],
                y=data['top'][i],
                width=data['width'][i],
                height=data['height'][i],
                confidence=conf / 100.0
            ))
        
        self._cached_boxes = boxes
        self._cache_valid = True
        return boxes
    
    def get_word_at(self, x: int, y: int) -> str | None:
        """
        Return the word at position (x, y), or None if no word found.
        Uses cached OCR results.
        """
        if not self._cache_valid:
            return None
        
        for box in self._cached_boxes:
            if (box.x <= x <= box.x + box.width and
                box.y <= y <= box.y + box.height):
                return box.text
        
        return None
    
    def invalidate_cache(self):
        """Mark cache as stale (call when book/page changes)."""
        self._cache_valid = False
