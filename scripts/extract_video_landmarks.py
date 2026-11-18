"""Extract hand landmarks from LSM Glosses videos (story 04).

Batch job: reuses L3 Capture (video mode) and L0 Landmarks/Normalizer;
never becomes a src module. Writes dataset/lsm_glosses/landmarks/ with
one (32, 42, 3) clip per video, its metadata json and splits.json (LOSO).
"""

import json
from pathlib import Path

import cv2
import numpy as np

from data.splits import Splits
from features.landmarks import Landmarks
from features.normalize import Normalizer
from vision.capture import Capture

GLOSSES = [
    "HOLA",
    "SI",
    "NO",
    "GRACIAS",
    "CASA",
    "AMIGO",
    "NOS_VEMOS",
    "POR_FAVOR",
    "DOCTOR",
    "AYUDA",
]
SIGNERS = 12


class VideoExtractor:
    """Extract and normalize hand landmarks for the pilot glosses."""

    def __init__(self, root, out):
        self.root = Path(root)
        self.out = Path(out)
        self.capture = Capture(camera=False, video=True)
        self.landmarks = Landmarks()
        self.normalizer = Normalizer()
        self.out.mkdir(parents=True, exist_ok=True)

    def videos(self):
        """List (gloss, signer, path) for every pilot video."""
        found = []
        for gloss in GLOSSES:
            for signer in range(SIGNERS):
                path = self.root / gloss / f"{gloss}_{signer}.mp4"
                if path.exists():
                    found.append((gloss, str(signer), path))
        return found

    @staticmethod
    def _frames(decoder):
        """Yield the decoded frames of one video."""
        while True:
            ok, frame = decoder.read()
            if not ok:
                break
            yield frame

    def frames(self, path, start_ms):
        """Decode the video and detect hands per frame (video mode).

        Args:
            path: Path of the video to decode.
            start_ms: Timestamp of the first frame; must keep growing
                across videos for the video-mode landmarker.

        Returns:
            Tuple (landmark sequence, next start_ms).
        """
        decoder = cv2.VideoCapture(str(path))
        fps = decoder.get(cv2.CAP_PROP_FPS) or 25.0
        sequence = [
            self.landmarks.stack(self.capture.detect_video(frame, start_ms + int(i * 1000 / fps)))
            for i, frame in enumerate(self._frames(decoder))
        ]
        count = len(sequence)
        decoder.release()
        return np.array(sequence, dtype=np.float32), start_ms + count * 1000 / fps

    def save(self, gloss, signer, sequence):
        """Write one normalized clip with its metadata file.

        Args:
            gloss: Dataset gloss label of the video.
            signer: Signer index (video file suffix).
            sequence: Raw (T, 42, 3) landmark sequence of detected hands.

        Returns:
            The clip id.
        """
        clip_id = f"{gloss}_{signer}"
        window = self.normalizer.normalize(
            self.normalizer.resample(self.normalizer.forward_fill(sequence))
        )
        np.savez(self.out / f"clip_{clip_id}.npz", landmarks=window)
        meta = {"glosa": gloss, "senante": signer, "sesion": clip_id, "frames": sequence.shape[0]}
        (self.out / f"clip_{clip_id}.json").write_text(json.dumps(meta))
        return clip_id

    def run(self):
        """Extract every pilot video; return (clip ids, total videos)."""
        ids, total, stamp = [], 0, 0
        for gloss, signer, path in self.videos():
            total += 1
            sequence, stamp = self.frames(path, int(stamp))
            if sequence.size and sequence.any():
                ids.append(self.save(gloss, signer, sequence))
        return ids, total

    def close(self):
        """Release the landmarker session."""
        self.capture.close()


def main():
    """Extract the pilot videos and write the LOSO splits."""
    out = Path("dataset/lsm_glosses/landmarks")
    extractor = VideoExtractor("dataset/lsm_glosses", out)
    try:
        ids, total = extractor.run()
    finally:
        extractor.close()
    _write_splits(out, ids)
    print(f"videos: {total}, clips extracted: {len(ids)} ({100.0 * len(ids) / total:.1f} % valid)")


def _write_splits(out, ids):
    """Write splits.json with one LOSO fold per signer."""
    clips = [{"id": clip_id, "signer": clip_id.rsplit("_", 1)[1]} for clip_id in ids]
    splits = {s: Splits.losos(clips, {s}) for s in sorted({c["signer"] for c in clips})}
    (out / "splits.json").write_text(json.dumps(splits, indent=2))


if __name__ == "__main__":
    main()
