"""Extract hand landmarks from Espejel clips (story 02b, Plan B).

Batch job: reuses L3 Capture and L0 Landmarks/Normalizer; never becomes
a src module. Writes dataset/espejel/landmarks/clip_<sesion>.npz with a
(32, 42, 3) window per clip, its metadata json and splits.json (LOSO).
"""

import glob
import json
from pathlib import Path

import cv2
import numpy as np

from g11.capture import Capture
from g11.catalog import Catalog
from g11.landmarks import Landmarks
from g11.normalize import Normalizer

PILOT = {"001": "good morning", "004": "thank you", "005": "please", "007": "goodbye", "055": "man"}
TEST_SIGNERS = {"11"}


class Extractor:
    """Extract and normalize hand landmarks for the pilot glosses."""

    def __init__(self, root, out):
        self.root = root
        self.out = out
        self.capture = Capture(camera=False)
        self.landmarks = Landmarks()
        self.normalizer = Normalizer()

    def clips(self):
        """List (clip id, gloss, image paths) per signer folder."""
        found = []
        for cls, gloss in sorted(PILOT.items()):
            pattern = f"{self.root}/{cls}/*"
            for folder in sorted(glob.glob(pattern)):
                name = Path(folder).name
                found.append((name, gloss, sorted(glob.glob(f"{folder}/*.jpg"))))
        return found

    def frames(self, paths):
        """Detect hands per image into one (T, 42, 3) sequence."""
        sequence = []
        for path in paths:
            hands = self.capture.detect(cv2.imread(path))
            sequence.append(self.landmarks.stack(hands))
        return np.array(sequence, dtype=np.float32)

    def save(self, clip_id, gloss, count, sequence):
        """Write one normalized clip with its metadata file.

        Args:
            clip_id: Session folder name (signer NN + class CCC).
            gloss: Dataset word label of the clip class.
            count: Number of source images in the clip.
            sequence: Raw (T, 42, 3) landmark sequence.

        Returns:
            The clip id.
        """
        window = self.normalizer.normalize(sequence)
        np.savez(self.out / f"clip_{clip_id}.npz", landmarks=window)
        meta = {
            "clase": clip_id[2:5],
            "glosa": gloss,
            "senante": clip_id[:2],
            "sesion": clip_id,
            "frames": count,
        }
        (self.out / f"clip_{clip_id}.json").write_text(json.dumps(meta))
        return clip_id

    def run(self):
        """Extract every pilot clip; return the extracted clip ids."""
        ids = []
        for clip_id, gloss, paths in self.clips():
            if paths:
                ids.append(self.save(clip_id, gloss, len(paths), self.frames(paths)))
        return ids

    def close(self):
        """Release the landmarker session."""
        self.capture.close()


def main():
    """Extract the pilot clips and write the LOSO splits."""
    out = Path("dataset/espejel/landmarks")
    out.mkdir(parents=True, exist_ok=True)
    extractor = Extractor("dataset/espejel", out)
    try:
        ids = extractor.run()
    finally:
        extractor.close()
    clips = [{"id": clip_id, "signer": clip_id[:2]} for clip_id in ids]
    splits = Catalog.splits(clips, TEST_SIGNERS)
    (out / "splits.json").write_text(json.dumps(splits, indent=2))
    print(f"clips extracted: {len(ids)}")


if __name__ == "__main__":
    main()
