"""Text-to-speech using Piper (with espeak-ng fallback)."""

import subprocess
import shutil

class TTSEngine:
    """Speaks words aloud."""
    
    def __init__(self):
        self.use_piper = shutil.which("piper") is not None
        self.piper_voice = "~/.local/share/piper/voices/en_US-lessac-medium.onnx"
    
    def speak(self, text: str) -> None:
        """Speak the given text."""
        if self.use_piper:
            self._speak_piper(text)
        else:
            self._speak_espeak(text)
    
    def _speak_piper(self, text: str) -> None:
        """Use Piper TTS."""
        try:
            proc = subprocess.Popen(
                ["piper", "--model", self.piper_voice, "--output-raw"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            audio, _ = proc.communicate(input=text.encode())
            
            # Play audio using aplay
            subprocess.run(
                ["aplay", "-r", "22050", "-f", "S16_LE", "-"],
                input=audio,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"Piper failed: {e}, falling back to espeak")
            self._speak_espeak(text)
    
    def _speak_espeak(self, text: str) -> None:
        """Fallback to espeak-ng."""
        subprocess.run(
            ["espeak-ng", "-v", "en-us", text],
            stderr=subprocess.DEVNULL
        )
