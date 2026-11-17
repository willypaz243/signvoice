"""Download the LSM Glosses dataset (Zenodo record 18330565).

One-time, fully automated: fetches the record metadata from the Zenodo
public API (no token), downloads the single 7z archive with resume
support, verifies its md5, extracts it with the system 7z binary and
writes <target>/manifest.json with the real counts. Re-runnable: skips
everything when the dataset is already extracted.

Usage:
    python scripts/download_lsm_glosses.py [target_dir]
    (default target: dataset/lsm_glosses)
"""

import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

CHUNK = 1 << 20


class LsmGlosses:
    """Fetch, verify, extract and catalog the LSM Glosses dataset."""

    def __init__(self, root):
        self.root = Path(root)
        self.archive = self.root.with_suffix(".7z")
        self.tmp = self.root.parent / ".lsm_tmp"

    def run(self):
        """Run every step, skipping the ones already done."""
        if (self.root / "manifest.json").exists():
            print(f"already present: {self.root}")
            return
        meta = self._api()
        self._download(meta)
        self._extract()
        self._manifest(meta)
        self.archive.unlink(missing_ok=True)
        print(f"lsm_glosses complete: {self.root}")

    def _api(self):
        """Fetch the Zenodo record and return the archive file entry."""
        api = "https://zenodo.org/api/records/18330565"
        request = urllib.request.Request(api, headers={"User-Agent": "g11"})
        with urllib.request.urlopen(request, timeout=180) as response:
            record = json.load(response)
        key = "Mexican Sign Language Glosses.7z"
        files = [f for f in record["files"] if f["key"] == key]
        if len(files) != 1:
            raise RuntimeError("archive not found in Zenodo record 18330565")
        return files[0]

    def _download(self, file):
        """Download the archive if needed, then verify its md5."""
        if not self._ready(file):
            self._attempt(file)
        self._verify(file)

    def _ready(self, file):
        """Report whether the local archive is fully downloaded."""
        return self.archive.exists() and self.archive.stat().st_size == file["size"]

    def _attempt(self, file, attempts=3):
        """Stream the archive until its size matches, resuming on errors."""
        for attempt in range(attempts):
            start = self.archive.stat().st_size if self.archive.exists() else 0
            try:
                self._stream(file, start)
            except OSError as error:
                print(f"resume {attempt + 1}: {error}")
            if self._ready(file):
                return
        raise RuntimeError(f"download failed after {attempts} attempts")

    def _stream(self, file, start):
        """Append the missing archive bytes from the published URL."""
        headers = {"User-Agent": "g11"}
        if start:
            headers["Range"] = f"bytes={start}-"
        request = urllib.request.Request(file["links"]["self"], headers=headers)
        with (
            urllib.request.urlopen(request, timeout=180) as response,
            open(self.archive, "ab" if start else "wb") as dest,
        ):
            shutil.copyfileobj(response, dest, CHUNK)

    def _verify(self, file):
        """Raise unless the local archive matches the published md5."""
        digest = hashlib.md5()
        with open(self.archive, "rb") as source:
            for block in iter(lambda: source.read(CHUNK), b""):
                digest.update(block)
        if digest.hexdigest() != file["checksum"].removeprefix("md5:"):
            raise ValueError(f"md5 mismatch for {self.archive}")

    def _extract(self):
        """Extract the archive into the target folder with the system 7z."""
        binary = shutil.which("7z")
        if not binary:
            raise RuntimeError("7z binary not found (install p7zip-full)")
        self.tmp.mkdir(parents=True, exist_ok=True)
        args = [binary, "x", str(self.archive), f"-o{self.tmp}", "-y"]
        subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
        shutil.rmtree(self.root, ignore_errors=True)
        (self.tmp / "Mexican Sign Language Glosses").rename(self.root)
        self.tmp.rmdir()

    def _manifest(self, file):
        """Write and print the manifest with per-gloss counts."""
        glosses = {p.name: self._counts(p) for p in sorted(self.root.iterdir()) if p.is_dir()}
        manifest = self._record(file, glosses)
        with open(self.root / "manifest.json", "w", encoding="utf-8") as fp:
            json.dump(manifest, fp, indent=2, ensure_ascii=False)
        videos = sum(v["videos"] for v in glosses.values())
        print(f"manifest: {len(glosses)} glosses, {videos} videos")

    def _record(self, file, glosses):
        """Build the manifest dictionary for the extracted dataset."""
        return {
            "source": "LSM Glosses dataset (Zenodo record 18330565)",
            "doi": "10.5281/zenodo.18330565",
            "license": file.get("license") or "cc-by-4.0",
            "paper": "Navarrete-Lopez et al. 2026, Front. Artif. Intell. 9:1794923",
            "status": "candidate/future work: face visible, full pose+hands pipeline",
            "per_gloss": glosses,
        }

    def _counts(self, folder):
        """Count the videos and signers of one gloss folder."""
        videos = [p for p in folder.iterdir() if p.suffix.lower() in (".mp4", ".mov")]
        return {"videos": len(videos), "signers": len({p.stem.rsplit("_", 1)[-1] for p in videos})}


def main():
    """Run the downloader against the target directory."""
    target = sys.argv[1] if len(sys.argv) > 1 else "dataset/lsm_glosses"
    LsmGlosses(target).run()


if __name__ == "__main__":
    main()
