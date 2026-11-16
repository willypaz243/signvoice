"""Gradio one-page demo: sign -> gloss -> phrase -> voice (offline)."""

import gradio as gr

from g11.glossary import Glossary
from g11.postprocess import PhraseBuilder
from g11.simulate import SimulatedPredictor
from g11.speak import TtsVoice


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

    def build(self):
        """Assemble the single-page Gradio layout.

        Returns:
            gr.Blocks page with a button, the gloss, the confidence,
            the phrase and the simulated flag.
        """
        with gr.Blocks(title="SignVoice") as page:
            gr.Markdown("# SignVoice — demo simulada (LSM a voz)")
            button = gr.Button("Simular señal")
            gloss = gr.Textbox(label="Glosa")
            confidence = gr.Number(label="Confianza")
            phrase = gr.Textbox(label="Frase en español")
            flag = gr.Textbox(label="Estado")
            button.click(self.step, outputs=[gloss, confidence, phrase, flag])
        return page

    def launch(self, **kwargs):
        """Open the demo in the browser."""
        self.build().launch(**kwargs)
