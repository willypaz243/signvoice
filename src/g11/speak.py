"""Offline text-to-speech with a local Spanish voice (piper)."""

import logging
import shutil
import subprocess
import wave
from pathlib import Path

LOG = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent.parent
PIPER_MODEL = ROOT / "models" / "es_AR-daniela-high.onnx"
PLAYERS = ("pw-play", "aplay", "paplay")
WAV = "/tmp/signvoice_tts.wav"


class TtsVoice:
    """Speak a phrase offline with the local Spanish female voice (piper)."""

    def __init__(self):
        self.voice = None

    def _player(self):
        """Find the first available audio player (or None)."""
        found = (name for name in PLAYERS if shutil.which(name))
        return next(iter(found), None)

    def _render(self, phrase):
        """Synthesize the phrase to a wav file with the piper model.

        Args:
            phrase: Spanish text to synthesize.
        """
        if self.voice is None:
            from piper import PiperVoice

            self.voice = PiperVoice.load(str(PIPER_MODEL))
        with wave.open(WAV, "wb") as wav:
            self.voice.synthesize_wav(phrase, wav)

    def _play(self):
        """Play the rendered wav with the first available player."""
        player = self._player()
        if player is None:
            raise RuntimeError("no audio player found")
        subprocess.run([player, WAV], check=True)

    def speak(self, phrase):
        """Render the phrase with piper and play it; silent on failure.

        Args:
            phrase: Spanish phrase to read (empty string reads nothing).
        """
        if not phrase:
            return
        try:
            self._render(phrase)
            self._play()
        except Exception as exc:  # noqa: BLE001 - mixed TTS errors
            LOG.warning("TTS failed, staying silent: %s", exc)
