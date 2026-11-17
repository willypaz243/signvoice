"""Tests for the Espejel dataset catalog logic (no network)."""

import zipfile

from data.catalog import Catalog

FOLDERS = [
    {"id": "root", "name": "MSLwords1"},
    {"id": "c1", "name": "001", "parent_id": "root"},
    {"id": "s11", "name": "01001", "parent_id": "c1"},
    {"id": "s12", "name": "02001", "parent_id": "c1"},
]

FILES = [
    {"filename": "003001.jpg", "folder_id": "s11"},
    {"filename": "003002.jpg", "folder_id": "s11"},
    {"filename": "003003.jpg", "folder_id": "s12"},
]


def test_path_for_maps_folder_id_to_class_and_signer():
    """Each file must land under <class>/<signer>/<filename>.

    The Mendeley tree is MSLwords1/class/signer; the class and signer
    names come from the folder tree, so the mapping must resolve the
    parent chain of a folder id.
    """
    catalog = Catalog.catalog(FOLDERS, FILES)
    assert catalog["s11"] == ("001", "01001")
    assert catalog["s12"] == ("001", "02001")


def test_manifest_counts_signers_and_frames_per_class():
    """The report needs a real count table: signers and frames per class.

    The manifest must aggregate the file list per class without
    duplicates, so the report never invents numbers.
    """
    manifest = Catalog.manifest(FOLDERS, FILES)
    assert manifest["001"]["signers"] == 2
    assert manifest["001"]["frames"] == 3


def test_pilot_glosses_picks_known_words_with_most_frames():
    """Pilot glosses must be words in our glossary with the most frames.

    Selection crosses the manifest with the pilot glossary; unknown
    words are skipped and the result is sorted by frame count.
    """
    words = {"001": "hola", "002": "adios"}
    manifest = {"001": {"signers": 11, "frames": 165}, "002": {"signers": 9, "frames": 135}}
    picked = Catalog.pilot_glosses(manifest, words, {"hola"}, 5)
    assert picked == [("001", "hola", 165)]


def test_xlsx_rows_read_class_and_word_pairs(tmp_path):
    """The class list xlsx must be readable with the standard library.

    Mendeley ships the 249-word class list as xlsx; a minimal reader
    keeps the demo dependency-free.
    """
    path = tmp_path / "classes.xlsx"
    with zipfile.ZipFile(path, "w") as zip:
        zip.writestr(
            "xl/sharedStrings.xml", '<sst xmlns="x"><si><t>001</t></si><si><t>hola</t></si></sst>'
        )
        zip.writestr(
            "xl/worksheets/sheet1.xml",
            '<worksheet xmlns="x"><sheetData>'
            '<row r="1"><c r="A1"><v>7</v></c>'
            '<c r="B1" t="s"><v>1</v></c></row>'
            "</sheetData></worksheet>",
        )
    rows = Catalog.xlsx_rows(path)
    assert rows == [("7", "hola")]
