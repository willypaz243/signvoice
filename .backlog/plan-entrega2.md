# Plan de la entrega 2 — V. Ingeniería (comprimido)

> Comprime las fases 0‑2 de `plan.md` en una línea de tiempo que arranca el **16/11/2026**.
> Objetivo: informe impreso con **números reales** y repo que corre con 3 comandos.
> Regla de la práctica: vale un experimento chico y honesto, no un sistema grande.

## Qué se entrega (historia 12)

- **V. Ingeniería** (2 000‑2 500 palabras): arquitectura, datos, método, métricas y
  matriz de confusión, con figuras y tablas numeradas.
- Código visible en GitHub: `pip install -e .`, `python -m g11 train`, `python -m g11 demo`.
- Historias que se cierran: **1, 2, 4, 6, 7** (la 12 requiere la 4 y la 6); la **3** y la
  **5** en la medida que den tiempo.
- **Se aplazan a la entrega 3:** #8 (umbral de confianza), #9 (máquina limpia),
  #10 (config multi‑lengua), #11 (servidor con cuentas). Si la 2 se entrega tarde, la #5
  también se aplaza y el informe se cierra con las glosas que queden entrenadas.

## Camino crítico (lo más rápido hacia un número)

| Días | Pista A · pipeline/ML | Pista B · datos/producto |
|---|---|---|
| D1 | Entorno conda `signvoice` (py 3.11) + esqueleto (story 01): `pyproject.toml`, `src/g11` (6 módulos), `simulate`, pytest | Espejel: descarga en Mendeley + conteo de imágenes por glosa → **lista de las 10 glosas** |
| D1‑D2 | **Spike de riesgo (lo primero):** MediaPipe Pose+Hands sobre ~20 imágenes de Espejel (fondo/ropa negras) | Apoyo al conteo y curado de clips |
| D2‑D4 | — | Landmarks del subconjunto → `landmarks/` (`.npz` por clip) + `meta.json` + `splits.json` **por señante** (story 2) |
| D4‑D7 | Entrenamiento GRU+atención, **LOSO**, top‑1, F1 macro, **matriz de confusión** (stories 4 y 7) | `glossary/LSM.yaml` (10 glosas) + plantillas + pytest de glosa→frase (story 6) |
| D8‑D10 | Integración: `demo` real (cámara → glosa → frase → voz); capturas de pantalla | Redacción de V. Ingeniería con los números y figuras |
| D10‑D12 | Revisión del equipo, `.docx` (genoffice), impresión | — |

Si la entrega 2 cae después del D12: #5 (10 glosas de punta a punta), #8 (umbral de
confianza), #9 (prueba en máquina limpia sin internet).

## Reparto (6 estudiantes)

| Rol | Hace |
|---|---|
| **A · código (pipeline/ML)** | Esqueleto, `landmarks`, `normalize`, `model`, `train`, métricas LOSO |
| **B · código (datos/producto)** | Dataset y splits, `glossary`, `postprocess`, `app` (Gradio+TTS), capturas |
| **C · datos/glosario** | Valida las 10 glosas en GDLSM/FENAMAS/SIGNA; cura Espejel (conteo de clips y señantes) |
| **D · informe** | Redacta V. Ingeniería, figuras, tablas y referencias |
| **E · validación/demo** | Contacto con el firmante externo; pruebas de punta a punta; ensaya la demo |
| **F · QA** | `ruff`+`pytest` en verde por commit, revisa el docx, exporta PDF |

Si C, D o E saben programar, F o D se lleva la story 6 (`postprocess` son funciones puras,
fáciles de testear) para aliviar a B.

## Definition of done diaria

- `ruff check` + `pytest` en verde en cada commit; **un commit por historia**.
- Cada historia deja un **número o una captura** que entra al informe (conteo de landmarks,
  top‑1 por señante excluido, F1 macro, latencia, frase de ejemplo).
- El estado de cada historia se actualiza aquí y en `stories/`.

## Riesgos principales (solo los que paran el plan)

| Riesgo | Acción |
|---|---|
| MediaPipe no detecta cuerpo en fondo/ropa negras | Spike en D1; plan B: solo Hand Landmarker (normaliza por la muñeca) o **MSLR** (29 clases, 102 señantes, fondo blanco) como base |
| Espejel son imágenes estáticas (≈15 frames/palabra) | Elegir glosas con más frames; reportar la limitación en V. Ingeniería |
| `torch-env` (py 3.13) no encaja con `mediapipe` | Entorno nuevo conda `signvoice` con **Python 3.11** |
| top‑1 sale bajo (60‑75 %) | Se reporta igual, con matriz de confusión y pares de glosas más confundidas: es evidencia de aprendizaje supervisado, no fracaso |

## Qué hace la entrega "visible" aunque no sea perfecta

1. Informe con **números reales** (aunque sean bajos) + matriz de confusión = evidencia de
   que hubo entrenamiento supervisado de verdad.
2. Esqueleto que corre con predicción simulada = la figura de arquitectura tiene sustento.
3. Repo con 3 comandos en el README + `.task` locales = reproducible y 100 % offline.

## Pendientes de cerrar antes del D1

- [ ] Fecha exacta de la entrega 2 (para fijar los D1‑D12 en calendario).
- [ ] Acceso al dataset Espejel CES 2024 en Mendeley (quién descarga y a qué URL).
- [ ] Confirmar quiénes son A y B (los 2 programadores) y a quién se suma como tercer codificador.
- [ ] Máquina principal de entrenamiento (laptop CPU; el `torch-env` actual sirve solo como referencia).
