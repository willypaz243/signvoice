# SignVoice

**Reconocimiento de señas y conversión a voz — traductor asistido por visión por computadora y
aprendizaje supervisado para la Lengua de Señas Mexicana (LSM).**

Práctica de Inteligencia Artificial · Grupo 11

## Qué hace

Cámara → *landmarks* (MediaPipe Pose + Hands) → ventana `(32, 42, 3)` relativa a la muñeca →
**Transformer encoder** (4 capas, 128 dims, token de clasificación) → glosa LSM → frase en
español (`glossary.yaml` + plantillas deterministas) → **voz offline** (Piper, voz local es_AR).
Interfaz web con webcam (Gradio) y CLI (`typer`). Todo funciona **sin internet** en la demo.

Alcance actual: **10 glosas** de señas aisladas, evaluadas con splits **LOSO** (por señante).
Entrenamiento sobre el dataset público **LSM Glosses** (Zenodo, CC BY); Espejel CES 2024 queda
como evidencia del spike. Sin experto en LSM en el grupo: las etiquetas vienen del dataset, el
vocabulario de glosarios de referencia (GDLSM / FENAS / SIGNA) y el español lo valida un
firmante externo.

## Stack

Python 3.11 · PyTorch (build CUDA, fijado en `uv.lock`) · MediaPipe Tasks (`.task` locales) ·
Transformer encoder · Gradio · `typer` · Piper (voz offline) · config YAML ·
`ruff` + `ty` + `pytest`.

## Comandos

```bash
uv sync --all-groups
python scripts/download_models.py      # una vez: voz piper + .task de MediaPipe
python scripts/download_dataset.py     # una vez: Espejel (evidencia del spike)
python scripts/download_lsm_glosses.py # una vez: LSM Glosses (entrenamiento)
ruff check .
ty check .
pytest -q
python -m g11 demo          # Gradio + webcam + voz (offline)
python -m g11 train --config config/es_MX.yaml
```

## Estructura

Capas de aplicación → datos (cada paquete solo importa de capas inferiores):

| Capa | Paquete | Módulos | Rol |
|---|---|---|---|
| L5 · Aplicación | `src/g11/` | `app` · `speak` · `__main__` | Demo Gradio, voz offline, CLI |
| L4 · Modelo | `src/model/` | `model` · `train` | Transformer encoder, entrenamiento LOSO |
| L3 · Visión | `src/vision/` | `capture` | Webcam → *landmarks* (MediaPipe Tasks) |
| L2 · Datos | `src/data/` | `dataset` · `catalog` | LSM Glosses / Espejel: carga y selección |
| L1 · Lenguaje | `src/language/` | `glossary` · `postprocess` | Glosas → frase en español (YAML) |
| L0 · Características | `src/features/` | `landmarks` · `normalize` | Ventana `(32, 42, 3)` relativa a la muñeca |

Directorios de soporte:

- `glossary/LSM.yaml` — vocabulario (10 glosas) como dato.
- `models/` — `.task` de MediaPipe y voz Piper (versionados: demo sin internet).
- `dataset/` — `espejel/` y `lsm_glosses/` (descargados, no versionados).
- `scripts/` — descargas (modelos, datasets) y extracción de *landmarks*.
- `tests/` — espejo 1:1 de `src/`.
- `docs/informe/` — `entrega1_informe.md` y `entrega2_borrador.md` (el `.docx`/`.pdf` no se versiona).
- `.backlog/` — `backlog.md`, `plan.md`, `stories/`.

Reglas de ingeniería (100 líneas por archivo, ≤ 12 módulos, funciones puras, idioma como
dato): ver `AGENTS.md`.

## Entregas

| Entrega | Fecha | Contenido |
|---|---|---|
| 1.ª | 10/nov/2026 | Informe: introducción, objetivos, marco teórico y referencial |
| 2.ª | 17/nov/2026 | Ingeniería: datos, modelo, métricas, demo |
| 3.ª | — | Demo completa, informe final |

## Licencia y datos

Código con fines académicos. Los datasets públicos (Espejel CES 2024, LSM Glosses) se usan
bajo **CC BY** y deben acreditarse; no se comitean datos, videos, landmarks ni pesos
(`data/`, `*.npz`, `*.pt`).
