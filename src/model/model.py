"""Small transformer encoder over hand landmark windows (story 04)."""

import math
from typing import TypedDict

import torch
from torch import nn

FRAMES = 32
POINTS = 42
DIM = 3


class Architecture(TypedDict):
    """Pre-registered architecture values for the pilot."""

    layers: int
    d_model: int
    heads: int
    ffn: int
    dropout: float


CONFIG: Architecture = {
    "layers": 4,
    "d_model": 128,
    "heads": 8,
    "ffn": 256,
    "dropout": 0.1,
}


class SignModel(nn.Module):
    """Classify a (32, 42, 3) hand window into gloss logits.

    Args:
        num_classes: Number of gloss labels (10 in the pilot).
        config: Architecture config; defaults to the pre-registered CONFIG.
    """

    def __init__(self, num_classes, config=None):
        super().__init__()
        self.num_classes = num_classes
        self.config: Architecture = CONFIG if config is None else config
        c = self.config
        self.embed = nn.Linear(POINTS * DIM, c["d_model"])
        self.register_buffer("positions", self._positions(c["d_model"]))
        self.cls_token = nn.Parameter(torch.zeros(1, 1, c["d_model"]))
        self.encoder = self._encoder(c)
        self.head = nn.Linear(c["d_model"], num_classes)

    @staticmethod
    def _encoder(c):
        """Stack the encoder layers from the config."""
        layer = nn.TransformerEncoderLayer(
            d_model=c["d_model"],
            nhead=c["heads"],
            dim_feedforward=c["ffn"],
            dropout=c["dropout"],
            batch_first=True,
        )
        return nn.TransformerEncoder(layer, c["layers"])

    @staticmethod
    def _positions(d_model):
        """Sinusoidal positional encoding for the 32-frame window."""
        pe = torch.zeros(FRAMES, d_model)
        position = torch.arange(0, FRAMES, dtype=torch.float).unsqueeze(1)
        div = torch.exp(torch.arange(0, d_model, 2) * (-math.log(2 * math.pi) / d_model))
        pe[:, 0::2] = torch.sin(position * div)
        pe[:, 1::2] = torch.cos(position * div)
        return pe.unsqueeze(0)

    def forward(self, window):
        """Score one batch of hand windows.

        Args:
            window: Tensor of shape (B, 32, 42, 3).

        Returns:
            Tensor of shape (B, num_classes) with the gloss logits.
        """
        x = self.embed(window.reshape(window.shape[0], FRAMES, -1)) + self.positions
        x = torch.cat([self.cls_token.expand(window.shape[0], -1, -1), x], dim=1)
        return self.head(self.encoder(x)[:, 0])
