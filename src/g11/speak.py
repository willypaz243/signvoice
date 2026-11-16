"""Offline text-to-speech with the system voice (pyttsx3)."""

import logging

import pyttsx3

LOG = logging.getLogger(__name__)


class TtsVoice:
    """Speak a phrase offline with the default system voice."""

    def __init__(self):
        self.engine = None

    def _init_engine(self):
        """Create the TTS engine with the first Spanish voice available.

        Returns:
            pyttsx3 engine configured for Spanish; falls back to the
            default voice when no Spanish one is installed.
        """
        engine = pyttsx3.init()
        for voice in engine.getProperty("voices"):
            if any(code.startswith("es") for code in voice.languages):
                engine.setProperty("voice", voice.id)
                break
        return engine

    def speak(self, phrase):
        """Read the phrase aloud; silent when no audio device is available.

        Args:
            phrase: Spanish phrase to read (empty string reads nothing).
        """
        if not phrase:
            return
        try:
            if self.engine is None:
                self.engine = self._init_engine()
            self.engine.say(phrase)
            self.engine.runAndWait()
        except Exception as exc:  # noqa: BLE001 - pyttsx3 raises mixed errors
            LOG.warning("TTS unavailable, staying silent: %s", exc)
