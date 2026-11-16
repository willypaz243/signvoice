# Story 03 — Una glosa real desde la webcam (stretch)

**Estado:** pendiente (stretch) · **Entrega 2** (solo si sobra tiempo) · **T2** (B)

## Story

Como señante, quiero que el sistema reconozca **una glosa real** desde mi cámara y la muestre
en pantalla, para confirmar que los landmarks de mi webcam son compatibles con los del dataset.

## Acceptance criteria

- [ ] `app.py` usa el modelo entrenado de la story 04 (reemplaza a `simulate.py` para la
      glosa piloto) y etiqueta la salida como `real` (no `simulado`).
- [ ] Una glosa del piloto se reconoce frente a la webcam y la captura va al informe.

## Cuándo se hace

Solo si el modelo de la story 04 está entrenado **antes de la noche del 16/11**. Si no, se
aplaza a la entrega 3 sin drama: la demo del hackathon corre con predicción simulada (story 01).

## Out of scope

Las 10 glosas (story 05) · umbral de confianza (story 08) · streaming continuo.
