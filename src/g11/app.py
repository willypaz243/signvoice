"""Gradio one-page demo: sign -> gloss -> phrase -> voice (offline)."""

import gradio as gr
import numpy as np

from g11.speak import TtsVoice
from language.glossary import Glossary
from language.postprocess import PhraseBuilder
from vision.capture import Capture


class SimulatedPredictor:
    """Pick a gloss deterministically so the demo runs before the real model.

    Args:
        glosses: Vocabulary of gloss labels the predictor may return.
        seed: Base seed; the clip index is added to it for reproducibility.
    """

    def __init__(self, glosses, seed=1234):
        self.glosses = glosses
        self.seed = seed

    def predict(self, clip_index):
        """Return a deterministic (gloss, confidence) pair for a clip.

        Args:
            clip_index: Zero-based index of the clip in the session.

        Returns:
            Tuple (gloss, confidence); the UI marks the result as simulated.
        """
        rng = np.random.default_rng(self.seed + clip_index)
        gloss = self.glosses[int(rng.integers(len(self.glosses)))]
        return gloss, 0.9


class DemoApp:
    """Build the demo page: a simulated sign becomes a spoken phrase.

    Args:
        glossary_path: Path to the glossary YAML (glossary/LSM.yaml).
    """

    def __init__(self, glossary_path):
        glossary = Glossary(glossary_path)
        self.builder = PhraseBuilder(glossary.words, glossary.markers)
        self.predictor = SimulatedPredictor(list(glossary.words), seed=1234)
        self.voice = TtsVoice()
        self.clip_index = 0
        self.glosses = []
        self.capture = None

    def step(self):
        """Predict the next simulated sign and update the phrase.

        Returns:
            Tuple (gloss, confidence, phrase, flag); the flag marks the
            result as simulated until the real model ships.
        """
        gloss, confidence = self.predictor.predict(self.clip_index)
        self.clip_index += 1
        self.glosses.append(gloss)
        phrase = self.builder.build(self.glosses)
        self.voice.speak(phrase)
        return gloss, confidence, phrase, "simulado"

    def capture_step(self):
        """Capture one webcam frame, run the pipeline and update the phrase.

        Returns:
            Tuple (frame, gloss, confidence, phrase, flag); the flag
            marks the result as simulated until the real model ships.
        """
        if self.capture is None:
            self.capture = Capture()
        ok, frame = self.capture.frame()
        if not ok:
            return None, "sin camara", 0.0, "No hay camara.", "error"
        self.capture.detect(frame)
        gloss, confidence = self.predictor.predict(self.clip_index)
        self.clip_index += 1
        self.glosses.append(gloss)
        phrase = self.builder.build(self.glosses)
        self.voice.speak(phrase)
        return frame, gloss, confidence, phrase, "simulado"

    def build(self):
        """Assemble the single-page Gradio layout.

        Returns:
            gr.Blocks page with a button, the gloss, the confidence,
            the phrase and the simulated flag.
        """
        with gr.Blocks(title="SignVoice") as page:
            gr.Markdown("# SignVoice — demo simulada (LSM a voz)")
            frame = gr.Image(type="numpy", label="Webcam")
            simulate = gr.Button("Simular señal")
            capture = gr.Button("Capturar señal (webcam)")
            gloss = gr.Textbox(label="Glosa")
            confidence = gr.Number(label="Confianza")
            phrase = gr.Textbox(label="Frase en español")
            flag = gr.Textbox(label="Estado")
            simulate.click(self.step, outputs=[gloss, confidence, phrase, flag])
            capture.click(self.capture_step, outputs=[frame, gloss, confidence, phrase, flag])
        return page

    def launch(self, **kwargs):
        """Open the demo in the browser."""
        self.build().launch(**kwargs)
