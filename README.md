# SignVoice

**Reconocimiento de señas y conversión a voz — traductor asistido por visión por computadora y
aprendizaje supervisado para la Lengua de Señas Mexicana (LSM).**

Práctica de Inteligencia Artificial · Grupo 11

## Qué hace

Cámara → *landmarks* (MediaPipe Pose + Hands) → modelo **GRU + atención temporal** → glosa LSM →
frase en español (diccionario + plantillas) → **voz offline** (`pyttsx3`).
Interfaz web con webcam (Gradio) y CLI (`typer`). Todo funciona **sin internet** en la demo.

Alcance actual: **10 glosas** de señas aisladas del dataset público Espejel CES 2024 (CC BY),
evaluadas con splits **LOSO** (por señante). Sin experto en LSM en el grupo: las etiquetas vienen
del dataset y el español lo valida un firmante externo.

## Stack

Python 3.11 · PyTorch · MediaPipe Tasks · GRU + atención · Gradio · `typer` · `pyttsx3` ·
config YAML · `ruff` + `pytest`.

## Comandos

```bash
pip install -e .
ruff check .
pytest -q
python -m g11 demo          # Gradio + webcam + voz (offline)
python -m g11 train --config config/es_MX.yaml
```

## Estructura

```
src/g11/       capture · landmarks · normalize · model · train · postprocess · glossary · app
glossary/      LSM.yaml
models/        pose_landmarker.task · hand_landmarker.task   (versionados: demo sin internet)
tests/         test_normalize · test_postprocess · test_glossary
docs/informe/  entrega1_informe.md (entregable imprimido)
.backlog/      backlog.md · plan.md · stories/
```

Reglas de ingeniería (límite de 100 líneas por archivo, ≤ 8 módulos, funciones puras, idioma como
dato): ver `AGENTS.md`. El plan por fases y el backlog: `.backlog/`.

## Entregas

| Entrega | Fecha | Contenido |
|---|---|---|
| 1.ª | 10/nov/2026 | Informe: introducción, objetivos, marco teórico y referencial |
| 2.ª | — | Ingeniería: datos, modelo, métricas, demo |
| 3.ª | — | Demo completa, informe final |

## Licencia y datos

Código con fines académicos. El dataset Espejel CES 2024 se usa bajo **CC BY** y debe acreditarse;
no se comitean datos, videos, landmarks ni pesos (`data/`, `*.npz`, `*.pt`).
