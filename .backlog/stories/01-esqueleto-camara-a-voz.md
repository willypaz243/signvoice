# Story 01 — Esqueleto de cámara a voz (walking skeleton)

**Estado:** pendiente · **Fase 0** (8‑9 nov) · **Persona A** (con B en `glossary` y TTS)

## Story

Como señante, quiero señalar una seña frente a la webcam y **escuchar una frase en voz alta**,
aunque la predicción sea simulada, para verificar que el trayecto
cámara → landmarks → glosa → español → voz funciona de punta a punta.

## Acceptance criteria

- [ ] Given corro `python -m g11 demo` (o abro Gradio), when la ventana se abre, then veo mi cámara
      y un panel con: glosa predicha, frase en español y botón/autoplay de voz.
- [ ] Given estoy frente a la cámara, when mantengo una seña 2 s, then el sistema extrae landmarks
      reales de MediaPipe (Pose + Hands) y muestra el conteo de puntos detectados (no ceros).
- [ ] Given que el modelo todavía no existe, when se llena una ventana de 32 frames, then se aplica
      la **predicción simulada** (`simulate.py`: la glosa de mayor confianza de una lista fija o la
      glosa indicada por el botón del vocabulario) y el panel lo indica como `simulado`.
- [ ] Given una secuencia de 2‑3 glosas simuladas, when termino la señal, then veo la frase en
      español producida por `diccionario + plantillas` y escucho la voz con `pyttsx3`.
- [ ] Given sin internet, when corro la demo, then funciona (modelos `.task` locales, voz del sistema).
- [ ] Given `ruff check` y `pytest`, when los ejecuto, then pasan (pruebas de `normalize`,
      `postprocess` y `glossary`; `pytest` no requiere cámara).

## Plan

1. `git init` + `.gitignore` (`data/`, `*.npz`, `.venv`, `__pycache__`, `graphify-out/`) + `README.md`
   (qué es, cómo se corre, 3 comandos).
2. `pyproject.toml`: `torch` (CPU por defecto), `mediapipe`, `gradio`, `pyttsx3`, `typer`, `numpy`,
   `pyyaml`, `pytest`, `ruff`. Python 3.11. `pip install -e .`.
3. `src/g11/` con **6 módulos, sin clases base**:
   `capture` (cámara → frames), `landmarks` (MediaPipe Tasks → `(T,F,3)`), `normalize`
   (relativa al torso, reescalar z, `T=32`), `simulate` (predicción falsa), `postprocess`
   (glosas → español con `glossary.yaml`), `app` (Gradio + `pyttsx3`).
4. Contrato de datos fijo desde el día 1 (dict/`np.ndarray` con `meta{senante, glosa, sesion}`):
   es lo que permite enchufar datos reales en la Fase 1 **sin reescribir** el `app`.
5. `tests/test_normalize.py` (invariancia de traslación/escala) y `tests/test_postprocess.py`
   (3 frases: afirmativa, pregunta, cortesía) con datos sintéticos.
6. Verificar de punta a punta en la laptop: señal real → landmarks no ceros → frase → voz audible.

## Out of scope

Dataset Espejel, selección de glosas y splits (#2) · reconocimiento real (#3, #4, #5) · matriz de
confusión (#7) · umbral de confianza (#8) · instalable en máquina limpia (#9) · config multi‑lengua (#10) ·
servidor, cuentas y roles (#11) · informe V. Ingeniería (#12).
