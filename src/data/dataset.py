"""Download the Espejel MSL dataset from the Mendeley public API."""

import gzip
import hashlib
import http.client
import json
import socket
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from data.catalog import Catalog

BASE = "https://data.mendeley.com/public-api/datasets/6rj76z6y3n"
DOI = "10.17632/6rj76z6y3n.1"
LICENSE = "CC BY 4.0"


class EspejelDataset:
    """Fetch, download and catalog the Espejel dataset under a directory."""

    def __init__(self, root):
        self.root = Path(root)
        self.done = 0
        socket.setdefaulttimeout(60)

    def metadata(self):
        """Fetch the file list and folder tree from the public API.

        Returns:
            Tuple (files, folders) as the raw JSON lists.
        """
        data = self._get(BASE)
        return data["files"], self._get(BASE + "/folders/1")

    def _get(self, url, attempts=3):
        """Fetch one JSON resource, retrying transient network errors.

        Args:
            url: Mendeley public API endpoint.
            attempts: Retry count before giving up.

        Returns:
            The decoded JSON body as Python objects.
        """
        for attempt in range(attempts):
            try:
                return self._fetch(url)
            except (OSError, http.client.HTTPException) as error:
                if attempt == attempts - 1:
                    raise
                print(f"retry {attempt + 1}: {error}")

    def _fetch(self, url):
        """Fetch one URL and return its JSON body (gzip aware)."""
        headers = {"User-Agent": "g11", "Accept-Encoding": "gzip"}
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=180) as response:
            body = response.read()
            if response.headers.get("Content-Encoding") == "gzip":
                body = gzip.decompress(body)
        return json.loads(body)

    def download(self):
        """Download every missing file and report the failures."""
        files, folders = self.metadata()
        catalog = Catalog.catalog(folders, files)
        with ThreadPoolExecutor(max_workers=24) as pool:
            results = pool.map(lambda f: self._one(f, catalog), files)
            failed = [(n, e) for n, e in results if e]
        print(f"download complete: {self.done} files, {len(failed)} failed")
        for name, error in failed:
            print(f"FAILED {name}: {error}")

    def _one(self, file, catalog):
        """Download one file under <class>/<signer> with 3 retries.

        Args:
            file: Mendeley file entry with folder_id and content_details.
            catalog: Folder id to (class, signer) mapping.

        Returns:
            Tuple (filename, error); error is None on success.
        """
        cls, signer = catalog.get(file["folder_id"], (None, None))
        parts = [p for p in (cls, signer, file["filename"]) if p]
        dest = self.root.joinpath(*parts)
        if dest.exists() and dest.stat().st_size == file["size"]:
            return file["filename"], None
        error = self._retry(file, dest)
        self.done += 1
        if self.done % 500 == 0:
            print(f"{self.done} files downloaded")
        return file["filename"], error

    def _retry(self, file, dest):
        """Download one file up to 3 times, verifying its sha256 hash."""
        dest.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(3):
            try:
                self._attempt(file, dest)
                return None
            except (OSError, ValueError):
                dest.unlink(missing_ok=True)
                error = f"{dest.name}: attempt {attempt + 1} failed"
        return error

    def _attempt(self, file, dest):
        """Run one download attempt and verify the sha256 hash."""
        url = file["content_details"]["download_url"]
        request = urllib.request.Request(url, headers={"User-Agent": "g11"})
        with urllib.request.urlopen(request) as response:
            dest.write_bytes(response.read())
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()
        if digest != file["content_details"]["sha256_hash"]:
            raise ValueError(f"sha256 mismatch for {dest}")

    def words(self):
        """Read the class-to-word map from the dataset xlsx file."""
        rows = Catalog.xlsx_rows(self.root / "classes.xlsx")
        return {cls: word for cls, word in rows if cls.isdigit()}

    def write_manifest(self, words):
        """Save the manifest with counts, words, DOI and license."""
        files, folders = self.metadata()
        manifest = Catalog.manifest(folders, files)
        manifest["_meta"] = {"doi": DOI, "license": LICENSE, "words": words}
        with open(self.root / "manifest.json", "w", encoding="utf-8") as fp:
            json.dump(manifest, fp, indent=2, sort_keys=True)
