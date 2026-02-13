"""Main entry point - ties all components together."""

import cv2
from .config import Config
from .wand import WandTracker
from .gesture import GestureDetector
from .ocr import OCREngine
from .tts import TTSEngine

def main():
    """Run the reading assistant."""
    config = Config()
    
    # Initialize components
    wand = WandTracker(config.wand)
    gesture = GestureDetector(config.gesture)
    ocr = OCREngine()
    tts = TTSEngine()
    
    # Open camera
    cap = cv2.VideoCapture(config.camera_index)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Reading Assistant started. Press 'q' to quit.")
    print("Double-tap a word with the wand to hear it spoken.")
    
    # Run OCR on first frame to cache word positions
    ocr_interval = 30  # Re-run OCR every N frames
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Periodically update OCR cache
            if frame_count % ocr_interval == 0:
                ocr.process_frame(frame)
            frame_count += 1
            
            # Track wand
            position = wand.update(frame)
            
            # Check for double-tap
            tap_location = gesture.update(position)
            
            if tap_location:
                x, y = tap_location
                word = ocr.get_word_at(x, y)
                if word:
                    print(f"Tapped: {word}")
                    tts.speak(word)
            
            # Draw debug overlay
            debug_frame = frame.copy()
            if position:
                cv2.circle(debug_frame, position, 10, (0, 255, 0), -1)
            
            cv2.imshow("Reading Assistant", debug_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
