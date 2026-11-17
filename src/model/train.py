"""LOSO training of the sign model with pre-registered config (story 04)."""

import json
import time

import numpy as np
import torch

from data.catalog import Catalog
from model.model import SignModel


class Trainer:
    """Train one fold per signer; report top-1, macro F1, curve and latency.

    Args:
        clips_dir: Directory with the clip npz and json pairs.
        out_dir: Directory for the weights and metrics.json.
        glosses: Gloss vocabulary (class names).
        epochs: Training epochs per fold (pre-registered).
    """

    def __init__(self, clips_dir, out_dir, glosses, epochs=25, lr=1e-3, device="cpu", seed=1234):
        self.clips_dir = clips_dir
        self.out_dir = out_dir
        self.glosses = list(glosses)
        self.epochs = epochs
        self.lr = lr
        self.device = torch.device(device)
        self.class_to_index = {gloss: i for i, gloss in enumerate(glosses)}
        torch.manual_seed(seed)
        out_dir.mkdir(parents=True, exist_ok=True)

    def _clips(self):
        """Load the metadata (id, signer, gloss) of every clip."""
        clips = []
        for meta in sorted(self.clips_dir.glob("clip_*.json")):
            data = json.loads(meta.read_text())
            clips.append({"id": data["sesion"], "signer": data["senante"], "gloss": data["glosa"]})
        return clips

    def folds(self):
        """Group the clips into one train/test fold per signer (LOSO).

        Returns:
            Dict signer to {"train": [clip], "test": [clip]}.
        """
        clips = self._clips()
        by_id = {c["id"]: c for c in clips}
        out = {}
        for signer in sorted({c["signer"] for c in clips}):
            split = Catalog.splits(clips, {signer})
            out[signer] = {k: [by_id[i] for i in v] for k, v in split.items()}
        return out

    def _batch(self, fold):
        """Load a fold's clips into (train, test) tensor pairs.

        Args:
            fold: One value of folds() with train and test clip lists.

        Returns:
            Pair of (windows, labels) tuples, the train pair first.
        """
        return self._tensors(fold["train"]), self._tensors(fold["test"])

    def _tensors(self, clips):
        """Load one part's clips as (windows, labels) on the device."""
        windows, labels = [], []
        for clip in clips:
            data = np.load(self.clips_dir / f"clip_{clip['id']}.npz")
            windows.append(data["landmarks"])
            labels.append(self.class_to_index[clip["gloss"]])
        return (
            torch.from_numpy(np.stack(windows)).to(self.device),
            torch.tensor(labels).to(self.device),
        )

    def fit(self, signer):
        """Train on one fold, save its weights, return its metrics.

        Args:
            signer: Signer id held out as the test set.

        Returns:
            Dict with top1, f1_macro and curve (loss per epoch).
        """
        fold = self.folds()[signer]
        (train_w, train_l), (test_w, test_l) = self._batch(fold)
        model = SignModel(len(self.glosses)).to(self.device)
        optimizer = torch.optim.Adam(model.parameters(), lr=self.lr)
        losses = self._train(model, optimizer, train_w, train_l)
        torch.save(model.state_dict(), self.out_dir / f"model_{signer}.pt")
        metrics = self._score(model, test_w, test_l)
        metrics["curve"] = losses
        return metrics

    def _train(self, model, optimizer, windows, labels):
        """Run the training epochs; return the loss per epoch."""
        losses = []
        for _ in range(self.epochs):
            loss = torch.nn.functional.cross_entropy(model(windows), labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach()))
        return losses

    def _score(self, model, test_w, test_l):
        """Score the held-out clips; return top-1 and macro F1."""
        with torch.no_grad():
            predicted = model(test_w).argmax(dim=1)
        correct = int((predicted == test_l).sum())
        return {"top1": correct / len(test_l), "f1_macro": self._f1(predicted, test_l)}

    def _f1(self, predicted, labels):
        """Macro-averaged F1 over the gloss classes."""
        scores = []
        for index in range(len(self.glosses)):
            tp, fp, fn = self._counts(predicted, labels, index)
            precision = tp / (tp + fp) if tp + fp else 0.0
            recall = tp / (tp + fn) if tp + fn else 0.0
            f1_score = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
            scores.append(f1_score)
        return float(np.mean(scores))

    @staticmethod
    def _counts(predicted, labels, index):
        """Count true/false positives and false negatives for one class."""
        tp = float(((labels == index) & (predicted == index)).sum())
        fp = float((predicted == index).sum()) - tp
        fn = float((labels == index).sum()) - tp
        return tp, fp, fn

    def _latency(self):
        """Time forward passes of the architecture (ms per clip)."""
        model = SignModel(len(self.glosses)).to(self.device).eval()
        windows = torch.zeros(16, 32, 42, 3, device=self.device)
        start = time.perf_counter()
        with torch.no_grad():
            for _ in range(5):
                model(windows)
        if self.device.type == "cuda":
            torch.cuda.synchronize()
        return (time.perf_counter() - start) * 1000.0 / 80

    def run(self):
        """Train every fold, write metrics.json, return all metrics."""
        out = {}
        for signer in self.folds():
            out[signer] = self.fit(signer)
        out["latency_ms"] = self._latency()
        (self.out_dir / "metrics.json").write_text(json.dumps(out, indent=2))
        return out
