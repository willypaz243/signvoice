"""Tests for LOSO training of the sign model."""

import json

import numpy as np

from model.train import Trainer


def _make_clips(root, signers, glosses):
    """Write synthetic clip npz + json pairs for the Trainer tests."""
    rng = np.random.default_rng(7)
    for signer in signers:
        for gloss in glosses:
            clip_id = f"{gloss}_{signer}"
            window = rng.uniform(0, 1, size=(32, 42, 3)).astype(np.float32)
            np.savez(root / f"clip_{clip_id}.npz", landmarks=window)
            meta = {"glosa": gloss, "senante": signer, "sesion": clip_id, "frames": 32}
            (root / f"clip_{clip_id}.json").write_text(json.dumps(meta))
    return root


def test_los_fold_keeps_held_out_signer_out_of_training(tmp_path):
    """The held-out signer's clips must never enter the training set.

    LOSO is the anti-memorization guarantee of the story: if any clip of
    the excluded signer leaked into training, the reported top-1 would
    measure the model remembering a person, not recognizing a sign.
    """
    root = _make_clips(tmp_path, ("0", "1", "2"), ("SI", "NO"))
    trainer = Trainer(root, tmp_path / "out", ["SI", "NO"])
    fold = trainer.folds()["1"]
    assert all(clip["signer"] != "1" for clip in fold["train"])
    assert all(clip["signer"] == "1" for clip in fold["test"])


def test_trainer_reports_top1_and_f1_macro(tmp_path):
    """One training run must yield top-1 and macro F1 for the fold.

    These are the two numbers the report quotes; they must be floats
    between 0 and 1, computed on the held-out signer only.
    """
    root = _make_clips(tmp_path, ("0", "1", "2"), ("SI", "NO"))
    trainer = Trainer(root, tmp_path / "out", ["SI", "NO"], epochs=2)
    metrics = trainer.fit("1")
    assert 0.0 <= metrics["top1"] <= 1.0
    assert 0.0 <= metrics["f1_macro"] <= 1.0


def test_trainer_writes_weights_and_curve(tmp_path):
    """Training must persist the weights and the training curve.

    The report needs the trained weights (for the demo and the CD) and
    the loss-per-epoch curve (figure); both are written per fold.
    """
    root = _make_clips(tmp_path, ("0", "1"), ("SI", "NO"))
    trainer = Trainer(root, tmp_path / "out", ["SI", "NO"], epochs=2)
    out = trainer.run()
    assert (root / "out" / "model_0.pt").exists()
    assert (root / "out" / "model_1.pt").exists()
    assert isinstance(out["0"]["curve"], list) and len(out["0"]["curve"]) == 2


def test_trainer_measures_inference_latency(tmp_path):
    """The trainer must report inference latency in milliseconds.

    The report quotes how fast one sign window is classified; the
    latency must be a positive float measured on real forward passes.
    """
    root = _make_clips(tmp_path, ("0", "1"), ("SI", "NO"))
    trainer = Trainer(root, tmp_path / "out", ["SI", "NO"], epochs=1)
    out = trainer.run()
    assert isinstance(out["latency_ms"], float) and out["latency_ms"] > 0.0
