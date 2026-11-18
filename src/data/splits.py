"""Pure LOSO split logic for signer-holdout evaluation (no I/O)."""


class Splits:
    """Assign clips to train/test by held-out signer (LOSO)."""

    @staticmethod
    def losos(clips, test_signers):
        """Assign clips to train/test by held-out signer (LOSO).

        Args:
            clips: List of clip dicts with "id" and "signer" keys.
            test_signers: Signer names whose clips become the test set.

        Returns:
            Dict {"train": [ids], "test": [ids]}, ids sorted ascending.
        """
        out = {"train": [], "test": []}
        for clip in clips:
            key = "test" if clip["signer"] in test_signers else "train"
            out[key].append(clip["id"])
        return {key: sorted(ids) for key, ids in out.items()}
