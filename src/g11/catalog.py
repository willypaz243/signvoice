"""Pure catalog logic for the Espejel MSL dataset (no I/O)."""

import xml.etree.ElementTree as ET
import zipfile


class Catalog:
    """Count and select glosses from the Mendeley file and folder lists."""

    @staticmethod
    def catalog(folders, files):
        """Map each folder id to its (class, signer) names.

        Args:
            folders: Folder tree list with id, name, parent_id entries.
            files: File list with folder_id entries.

        Returns:
            Dict folder id to (class, signer); the root maps to (None, None).
        """
        by_parent = {}
        for folder in folders:
            by_parent.setdefault(folder.get("parent_id"), []).append(folder)
        root = next(f["id"] for f in folders if not f.get("parent_id"))
        out = {root: (None, None)}
        for cls in by_parent[root]:
            out.update({s["id"]: (cls["name"], s["name"]) for s in by_parent[cls["id"]]})
        return out

    @staticmethod
    def manifest(folders, files):
        """Count signers and frames per class for the report table.

        Args:
            folders: Folder tree list with id, name, parent_id entries.
            files: File list with folder_id entries.

        Returns:
            Dict class to {"signers": int, "frames": int}.
        """
        catalog = Catalog.catalog(folders, files)
        grouped = {}
        for file in files:
            cls, signer = catalog.get(file["folder_id"], (None, None))
            if cls is None:
                continue
            entry = grouped.setdefault(cls, {"signers": set(), "frames": 0})
            entry["signers"].add(signer)
            entry["frames"] += 1
        return Catalog._counts(grouped)

    @staticmethod
    def _counts(grouped):
        """Convert the grouped signer sets to plain int counts."""
        return {
            c: {"signers": len(g["signers"]), "frames": g["frames"]} for c, g in grouped.items()
        }

    @staticmethod
    def pilot_glosses(manifest, words, allowed, limit):
        """Pick pilot glosses: known words with the most frames.

        Args:
            manifest: Class counts from manifest().
            words: Dict class to Spanish word.
            allowed: Set of pilot glossary words.
            limit: Maximum number of glosses to pick.

        Returns:
            List of (class, word, frames) sorted by frames, descending.
        """
        picked = [
            (cls, words[cls], manifest[cls]["frames"])
            for cls in words
            if cls in manifest and words[cls] in allowed
        ]
        return sorted(picked, key=lambda item: -item[2])[:limit]

    @staticmethod
    def splits(clips, test_signers):
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

    @staticmethod
    def xlsx_rows(path):
        """Read (class, word) rows from the first sheet of an xlsx.

        Args:
            path: Path to the xlsx file.

        Returns:
            List of (class, word) string pairs, one per data row.
        """
        with zipfile.ZipFile(path) as zip:
            shared = Catalog._shared(zip)
            root = ET.fromstring(zip.read("xl/worksheets/sheet1.xml"))
        rows = []
        for row in root.iter():
            if not row.tag.endswith("}row"):
                continue
            values = []
            for cell in row:
                value = cell.findtext("{*}v")
                if value is None:
                    continue
                text = shared[int(value)] if cell.get("t") == "s" else value
                values.append(text)
            if len(values) >= 2:
                rows.append((values[0], values[1]))
        return rows

    @staticmethod
    def _shared(zip):
        """Collect the shared string table of an xlsx archive."""
        root = ET.fromstring(zip.read("xl/sharedStrings.xml"))
        return [
            "".join(t.text or "" for t in si.iter() if t.tag.endswith("}t"))
            for si in root
            if si.tag.endswith("}si")
        ]
