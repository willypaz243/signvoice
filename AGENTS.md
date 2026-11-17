# AGENTS.md — SignVoice · LSM → speech translator (Group 11)

Guide for agents and members writing code or documents in this repository.
The plan and the stories live in `.backlog/` (`backlog.md`, `plan.md`, `stories/`).

## Context

- **Project name: SignVoice** (repo `signvoice`). The name appears on the cover, README and
  diagrams; the Python package is `g11` and is not renamed.
- University AI practice: **sign recognition (LSM) and conversion to speech** with
  **supervised learning + computer vision**.
- **3 deliverables.** Deliverable 1 (Nov 10, 2026) is report I. Introduction, II. Objectives,
  III. Theoretical framework, IV. Referential framework → `docs/informe/entrega1_informe.md`.
  Section **V. Engineering** is initialized and is the subject of deliverable 2.
- **What is evaluated is learning supervised ML, not the state of the art.** A small and
  honest experiment is worth more than three half-built models.
- **No LSM expert in the group:** labels come from already-labeled public datasets, the
  vocabulary from reference glossaries (GDLSM / FENAS / SIGNA), and the generated Spanish is
  validated by an external signer. Nobody invents glosses or syntax.
- `docs/investigacion/` is **outside the repo** (gitignored): a study annex for the defense,
  not printable material.

## Stack (not changed without an explicit group decision)

Python 3.11 · PyTorch (CPU by default; CUDA with pinned versions for the final training) ·
MediaPipe **Tasks** Pose + Hands (local `.task` files) · dataset **Espejel CES 2024**
(249 LSM words, CC BY) · **GRU + temporal attention** over **10 glosses** of **isolated**
signs · `glossary.yaml` + **deterministic templates** for gloss→Spanish · `pyttsx3`
(offline voice) · **Gradio** (webcam) + CLI `typer` · configuration in **YAML** ·
`ruff` + `ty` + `pytest`.

## Code rules (hard)

- **Every code file: 100 lines or fewer (hard limit), 60 lines (suggested), excluding
  docstring lines.** Over 60: try to split the file; over 100: split it or remove
  functionality; **never raise the hard limit**.
- **Every function: 9 lines or fewer** (body, excluding signature and docstring).
- **Programming standard: object-oriented.** Business logic always lives in classes, never
  in loose functions. One concrete class per concern; no base classes, no inheritance,
  no factories, no dependency injection, no plugins, no "service layers".
- `src/` with **≤ 12 modules**.
- **Two-times rule:** an abstraction appears only when two real uses exist; before that,
  duplicate the code.
- **Delete rule:** a module, config, or dependency that the demo does not consume is
  removed.
- **No internet in the demo:** no downloads at runtime. `.task` models and voices live in
  the repo or the environment.
- **Pure logic** for `normalize`, `splits`, `postprocess`, and metrics: no I/O, tested with
  `pytest` without camera, network, or GPU.
- **Quality gate:** `ruff check` and `ty check` must pass on every commit. `ty` runs with a
  pragmatic configuration (`pyproject.toml`): consistent typing of the first-party code,
  without blocking on third-party libraries that ship no type stubs.
- **Test docstrings:** every test has an English docstring explaining what it tests and why
  it matters, so any developer can understand it.
- **Core docstrings:** business-logic (core) classes and methods use **Google-style**
  docstrings: one-line summary, then `Args:` and `Returns:` sections.
- The core is a **`frames → glosses → phrase`** function. The API with accounts and roles
  (phase 4) **calls it**, it does not rewrite it: the ML core does not import HTTP,
  sessions, or a database.
- **Language is data, not code:** `config.yaml` + `glossary/<language>.yaml`. No
  `if language == …` inside the logic.
- **Code is written in English**: identifiers, comments, docstrings, logs, error messages
  and test names. **Spanish only appears in data shown to the user**: the translated
  phrase, the interface texts, the TTS text, and the values of `glossary/LSM.yaml`.
  LSM domain terms (`glosa`, `señante`) are explained in English in the docstrings and
  live in Spanish only in the documentation (`docs/`, report).

## Structure (layered, ≤ 12 modules)

Layers go **top → bottom**; modules only import from lower layers, never upward.

| Layer | Modules | Role | Depends on |
|---|---|---|---|
| L5 · Application | `app` (incl. simulated predictor), `speak`, `__main__` | Gradio demo, voice, CLI | L0–L4 |
| L4 · Model | `model`, `train` | GRU + attention, LOSO training, metrics | L0 |
| L3 · Vision | `capture` | webcam → pose + hands (MediaPipe Tasks) | — |
| L2 · Data | `dataset`, `catalog` | Espejel download + counts / gloss selection | — |
| L1 · Language | `glossary`, `postprocess` | glosses → Spanish phrase (YAML data) | — |
| L0 · Features | `landmarks`, `normalize` | (75, 3) stack → (32, 75, 3) torso-relative window | nothing (numpy) |

- **Steady state is exactly 12 modules.** Batch/one-shot jobs live in `scripts/`,
  not `src/`: dataset download, `.task`/voice download, landmark extraction
  (`scripts/extract_landmarks.py` reuses L3 + L0 classes; it never becomes a module).
- **One module = one business class**: `Capture`, `Landmarks`, `Normalizer`,
  `Glossary`, `PhraseBuilder`, `Catalog`, `EspejelDataset`, `TtsVoice`, `DemoApp`,
  `SignModel`, `Trainer`.
- **L0/L1/L2 are pure logic**: testable with `pytest` without camera, network, or GPU.
- **When the real model ships (story 04):** `simulate` merges into `app` (single
  consumer; delete rule) in the same commit as `model.py` + `train.py`.
- **`tests/` mirrors `src/` 1:1** (`test_<module>.py`), flat, no subpackages.
- **If a module grows:** over 60 lines split it (`model_gru.py`,
  `model_attention.py`); over 100, split or cut. If wiring the pipeline pushes
  `app` past 100, extract `pipeline.py` (L5, class `Pipeline`) and merge `speak`
  into `app` to stay at 12.

```
src/g11/  app.py  speak.py  __main__.py            # L5
          model.py  train.py                       # L4
          capture.py                               # L3
          dataset.py  catalog.py                   # L2
          glossary.py  postprocess.py              # L1
          landmarks.py  normalize.py               # L0
glossary/ LSM.yaml
models/   (downloaded, gitignored; see scripts/download_models.py)
dataset/  (downloaded, gitignored)
          espejel/     Espejel CES 2024 images (see scripts/download_dataset.py)
          lsm_glosses/ LSM Glosses videos, candidate/future work (Zenodo 18330565)
scripts/  download_models.py  download_dataset.py  extract_landmarks.py
tests/    test_<module>.py (mirrors src/g11/)
```

`pyproject.toml` with pinned dependencies (locked in `uv.lock`). One module per small
file: if a module grows beyond 60 lines, it is split (`model_gru.py`,
`model_attention.py`, …).

## Commands

```bash
uv sync --all-groups
python scripts/download_models.py   # one-time: piper voice + MediaPipe .task
python scripts/download_dataset.py   # one-time: Espejel dataset (2 GB) into dataset/espejel/
python scripts/download_lsm_glosses.py  # one-time: LSM Glosses videos (2.7 GB) into dataset/lsm_glosses/
ruff check .
ty check .
pytest -q
python -m g11 demo          # Gradio + webcam + voice
python -m g11 train --config config/es_MX.yaml
```

## Mermaid diagram style (this repo is read in a dark-theme viewer)

- Color **on the border only**, no fill: `style Node fill:none,stroke:#e8b339,stroke-width:2.5px`.
- Every `mermaid` block starts with the **light-text** base line
  (`'theme':'dark'` + `themeVariables` + `themeCSS` with `.nodeLabel{color:#e6e6e6 !important}`);
  the full version and the rules are in `docs/README.md`.
- Inside `themeCSS` **only class and attribute selectors survive**: tag selectors
  (`text`, `tspan`, `path`) or selectors with `>` make DOMPurify drop the whole CSS block.
- For printing on white paper: `'theme':'neutral'` with text `#333333` and `-b white`.

## Workflow

- **One story at a time** from `.backlog/backlog.md`; the phase order is in
  `.backlog/plan.md`.
- **Conventional commits**, one commit per story, with `ruff check`, `ty check` and
  `pytest` green.
- `docs/informe/entrega1_informe.md` is the printed deliverable: **do not reformat** it
  without notice.
- The report goes **MD → .docx (GenOffice, Google Docs compatible) → PDF**; `.docx`/`.pdf`
  and exported files are not committed.
- Data, videos, landmarks, and weights are not committed (`data/`, `*.npz`, `*.pt`).
  Publishing data requires prior consent and anonymization.
