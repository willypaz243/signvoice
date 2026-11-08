# AGENTS.md — SignVoice · Traductor LSM → voz (Grupo 11)

Guía para agentes e integrantes que escriban código o documentos en este repositorio.
El plan y las historias viven en `.backlog/` (`backlog.md`, `plan.md`, `stories/`).

## Contexto

- **Nombre del proyecto: SignVoice** (repo `signvoice`). El nombre va en portada, README y
  diagramas; el paquete Python es `g11` y no se renombra.

- Práctica universitaria de IA: **reconocimiento de señas (LSM) y conversión a voz** con
  **aprendizaje supervisado + visión por computadora**.
- **3 entregas.** La 1.ª (10/nov/2026) es el informe I. Introducción, II. Objetivos, III. Marco
  teórico, IV. Marco referencial → `docs/informe/entrega1_informe.md`. La sección **V. Ingeniería**
  se inicializa y es materia de la 2.ª entrega.
- **Se evalúa aprender ML supervisado, no el estado del arte.** Un experimento chico y honesto vale
  más que tres modelos a medias.
- **No hay experto en LSM en el grupo:** las etiquetas vienen de datasets públicos ya etiquetados,
  el vocabulario de glosarios de referencia (GDLSM / FENAMAS / SIGNA) y el español generado lo
  valida un firmante externo. Nadie inventa glosas ni sintaxis.
- `docs/investigacion/` está **fuera del repositorio** (gitignored): es anexo de estudio para la
  defensa, no material imprimible.

## Stack (no se cambia sin decisión explícita del grupo)

Python 3.11 · PyTorch (CPU por defecto; CUDA con versiones fijadas para el entrenamiento final) ·
MediaPipe **Tasks** Pose + Hands (archivos `.task` locales) · dataset **Espejel CES 2024**
(249 palabras LSM, CC BY) · **GRU + atención temporal** sobre **10 glosas** de señas **aisladas** ·
`glossary.yaml` + **plantillas deterministas** para glosa→español · `pyttsx3` (voz offline) ·
**Gradio** (webcam) + CLI `typer` · configuración en **YAML** · `ruff` + `pytest`.

## Reglas de código (duras)

- **Cada archivo de código: 100 líneas o menos.** Si se pasa, se parte el archivo o se elimina
  funcionalidad; **no se sube el límite**.
- `src/` con **≤ 8 módulos**. Sin clases base, sin herencia, sin factories, sin inyección de
  dependencias, sin plugins, sin "capas de servicio".
- **Regla de las dos veces:** una abstracción aparece solo cuando existen dos usos reales; antes de
  eso, se repite el código.
- **Regla de borrar:** un módulo, config o dependencia que la demo no consume, se elimina.
- **Sin internet en la demo:** nada de descargas en tiempo de ejecución. Modelos `.task` y voces
  van en el repo o en el entorno.
- **Funciones puras** para `normalize`, `splits`, `postprocess` y métricas: se prueban con `pytest`
  sin cámara, sin red y sin GPU.
- El núcleo es una función **`frames → glosas → frase`**. La API con cuentas y roles (fase 4) la
  **llama**, no la reescribe: el núcleo de ML no importa HTTP, sesiones ni base de datos.
- **El idioma es dato, no código:** `config.yaml` + `glossary/<lengua>.yaml`. Sin `if lengua == …`
  dentro de la lógica.
- Identificadores en inglés; términos de dominio LSM en español (`glosa`, `señante`) en comentarios,
  docstrings y documentación.

## Estructura

```
src/g11/  capture.py  landmarks.py  normalize.py  model.py  train.py
          postprocess.py  glossary.py  app.py
glossary/ LSM.yaml
models/   pose_landmarker.task  hand_landmarker.task   (versionados: demo offline)
tests/    test_normalize.py  test_postprocess.py  test_glossary.py
```

`pyproject.toml` con dependencias fijadas. Un archivo por módulo pequeño: si un módulo crece más de
100 líneas, se divide (`model_gru.py`, `model_attention.py`, …).

## Comandos

```bash
pip install -e .
ruff check .
pytest -q
python -m g11 demo          # Gradio + webcam + voz
python -m g11 train --config config/es_MX.yaml
```

## Estilo de diagramas Mermaid (este repo se lee en visor de tema oscuro)

- Color **solo en el borde**, sin relleno: `style Nodo fill:none,stroke:#e8b339,stroke-width:2.5px`.
- Cada bloque `mermaid` empieza con la línea de base de **texto claro**
  (`'theme':'dark'` + `themeVariables` + `themeCSS` con `.nodeLabel{color:#e6e6e6 !important}`);
  la versión completa y las reglas están en `docs/README.md`.
- Dentro de `themeCSS` **solo sobreviven selectores de clase y de atributo**: los de etiqueta
  (`text`, `tspan`, `path`) o con `>` hacen que DOMPurify descarte todo el CSS del bloque.
- Para imprimir en papel blanco: `'theme':'neutral'` con texto `#333333` y `-b white`.

## Flujo de trabajo

- **Una historia a la vez** desde `.backlog/backlog.md`; el orden de fases está en `.backlog/plan.md`.
- Commits **conventional commits**, un commit por historia, con `ruff check` y `pytest` en verde.
- `docs/informe/entrega1_informe.md` es el entregable imprimido: **no reformatear** sin avisar.
- El informe sale **MD → .docx (GenOffice, compatible con Google Docs) → PDF**; no se comitean
  `.docx`/`.pdf` ni los exportados.
- No se comitean datos, videos, landmarks ni pesos (`data/`, `*.npz`, `*.pt`). Publicar datos
  exige consentimiento y anonimización previos.
