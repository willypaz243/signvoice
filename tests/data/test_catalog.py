"""Tests for the pure Espejel catalog logic (splits LOSO)."""

from data.catalog import Catalog

CLIPS = [
    {"id": "01001", "signer": "01"},
    {"id": "01002", "signer": "01"},
    {"id": "02001", "signer": "02"},
    {"id": "03001", "signer": "03"},
]


def test_splits_holds_out_signers_for_loso():
    """Every clip of a held-out signer must go to the test set.

    Leave-One-Signer-Out keeps all clips of one person together, so the
    model is scored on an unseen signer instead of memorized hands.
    """
    splits = Catalog.splits(CLIPS, {"02"})
    assert splits["test"] == ["02001"]
    assert splits["train"] == ["01001", "01002", "03001"]


def test_splits_is_deterministic():
    """Running the split twice must give the same assignment.

    The extraction script writes splits.json once; a deterministic
    order keeps the report and any later training run comparable.
    """
    assert Catalog.splits(CLIPS, {"02"}) == Catalog.splits(CLIPS, {"02"})
