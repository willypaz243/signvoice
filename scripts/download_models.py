"""Download the offline demo models (piper voice and MediaPipe .task)."""

import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"

URLS = {
    "pose_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
        "pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
    ),
    "hand_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
        "hand_landmarker/full/1/hand_landmarker.task"
    ),
}


class ModelDownloader:
    """Fetch the demo models once; the demo itself never downloads."""

    def __init__(self, models_dir):
        self.dir = Path(models_dir)

    def piper_voice(self, name):
        """Download a piper voice into the models directory.

        Args:
            name: Piper voice id (for example, es_AR-daniela-high).
        """
        subprocess.run(
            ["python", "-m", "piper.download_voices", name, "--data-dir", str(self.dir)],
            check=True,
        )

    def mediapipe(self):
        """Download the MediaPipe pose and hand landmarker .task files."""
        self.dir.mkdir(parents=True, exist_ok=True)
        for file_name, url in URLS.items():
            target = self.dir / file_name
            if not target.exists():
                urllib.request.urlretrieve(url, target)
                print(f"downloaded {file_name}")

    def all(self):
        """Download every model the demo needs (piper voice + MediaPipe)."""
        self.piper_voice("es_AR-daniela-high")
        self.mediapipe()


if __name__ == "__main__":
    ModelDownloader(MODELS).all()
