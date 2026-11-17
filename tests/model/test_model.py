"""Tests for the small transformer encoder over hand windows."""

import torch

from model.model import SignModel


def test_sign_model_maps_window_to_gloss_logits():
    """One (32, 42, 3) window per clip must produce 10 gloss logits.

    The model input is the normalized hand-landmark window and the
    output is an unnormalized score per gloss; softmax is applied by
    the caller that needs probabilities.
    """
    model = SignModel(num_classes=10).eval()
    window = torch.zeros(3, 32, 42, 3)
    with torch.no_grad():
        logits = model(window)
    assert logits.shape == (3, 10)


def test_sign_model_uses_pre_registered_config():
    """The default architecture must match the pre-registered pilot.

    The story 04 decision fixes a single configuration (no retunes):
    4 encoder layers, 128 dimensions, 8 heads, feed-forward 256 and
    dropout 0.1, mirroring the dataset paper's most stable transformer.
    """
    config = SignModel(num_classes=10).config
    assert config["layers"] == 4
    assert config["d_model"] == 128
    assert config["heads"] == 8
    assert config["ffn"] == 256
    assert config["dropout"] == 0.1


def test_sign_model_is_deterministic_with_fixed_seed():
    """Two models built with the same seed must give the same logits.

    The single pre-registered run must be reproducible for the report;
    seeding the construction and feeding the same window must yield
    identical outputs.
    """
    torch.manual_seed(1234)
    first = SignModel(num_classes=10).eval()
    torch.manual_seed(1234)
    second = SignModel(num_classes=10).eval()
    window = torch.zeros(2, 32, 42, 3)
    with torch.no_grad():
        assert torch.equal(first(window), second(window))
