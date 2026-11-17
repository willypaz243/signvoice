"""Download the Espejel MSL dataset into the dataset/espejel directory.

One-time, fully automated: fetches the file list and folder tree from
the Mendeley public API (no token), downloads every file with sha256
verification and writes dataset/espejel/manifest.json with the real counts.

Usage:
    python scripts/download_dataset.py
"""

from g11.dataset import EspejelDataset

ROOT = "dataset/espejel"


def main():
    """Download the dataset and write the manifest with pilot glosses."""
    dataset = EspejelDataset(ROOT)
    dataset.download()
    words = dataset.words()
    dataset.write_manifest(words)
    print("dataset complete:", ROOT)
    print("words:", len(words))


if __name__ == "__main__":
    main()
