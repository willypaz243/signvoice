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

- **Every code file: 60 lines or fewer.** If it goes over, split the file or remove
  functionality; **never raise the limit**.
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

## Structure

```
src/g11/  capture.py  landmarks.py  normalize.py  model.py  train.py
          postprocess.py  glossary.py  app.py
glossary/ LSM.yaml
models/   pose_landmarker.task  hand_landmarker.task   (versioned: offline demo)
tests/    test_normalize.py  test_postprocess.py  test_glossary.py
```

`pyproject.toml` with pinned dependencies (locked in `uv.lock`). One module per small
file: if a module grows beyond 60 lines, it is split (`model_gru.py`,
`model_attention.py`, …).

## Commands

```bash
uv sync --all-groups
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
