# Plan de desarrollo — Traductor LSM → voz (Grupo 11)

> Complementa a `backlog.md`. Fechas reales, qué se entrega en cada una, y los límites que evitan
> sobreingeniería y código espagueti.

## Reglas de alcance (no negociables)

1. **Se evalúa aprender ML supervisado**, no el SOTA. Un experimento chico, honesto y reproducible
   vale más que tres modelos a medias.
2. **Camino único**: una sola ruta de `cámara → landmarks → glosa → español → voz`. Nada de
   "módulo experimental" paralelo.
3. **Etiquetas solo de fuentes públicas** (dataset Espejel) y vocabulario de glosarios GDLSM /
   FENAMAS / SIGNA. Nadie del grupo inventa glosas ni gramática LSM.
4. **Nada de deep learning exótico**: GRU + atención. Sin ST‑GCN, sin Transformer, sin CTC, sin
   pretraining, sin LLM en la ruta crítica.
5. **Sin corpus propio** en la práctica: la grabación y sus permisos se comen el semestre y el
   etiquetado no es verificable sin experto.
6. **Regla de las dos veces**: una abstracción aparece cuando existen **dos usos reales**. Antes de
   eso, se repite el código.
7. **Regla de borrar**: un módulo, config o dependencia que no consume la demo, se elimina.
8. **Límites medibles**: `src/` con **≤ 8 módulos**; **cada archivo de código, 100 líneas o menos**
   (se parte el archivo, nunca se sube el límite); cada commit con `ruff check` y `pytest` en verde.

## Fuera de alcance (explícito, para no discutirlo a mitad del semestre)

Corpus propio · señas continuas/frases con CTC · dactilología · traducción secuencia‑a‑secuencia
(corpus Lara‑Ortiz) · ST‑GCN/Transformer/comparativa de arquitecturas · app móvil · Docker ·
multi‑tenant · i18n de la interfaz · métricas BLEU/chrF · fine‑tuning de MediaPipe · base de datos
de videos · detección de inicio‑fin de seña en streaming.

## Entregas y fases

### Fase 0 — 48 h (8 y 9 nov) → **entrega 1 el 10 nov**

Entregable: **informe impreso** con I. Introducción, II. Objetivos, III. Marco teórico,
IV. Marco referencial. V. Ingeniería se **inicializa** (andamiaje de código visible, sin métricas).

- [ ] **Recortar el informe** a lo indispensable: de ~9 700 palabras a **2 000‑2 500**, en
      **un solo archivo MD** (`docs/informe/entrega1_informe.md`, se recorta sobre sí mismo) con los
      diagramas que sí se usan (máx. 3) y sin gráficas accesorias.
      `docs/investigacion/` **no se imprime**: queda como anexo de estudio para la defensa.
- [ ] **Regla de referencias**: si una fuente no aparece citada en el cuerpo recortado, **sale de
      la bibliografía**. Se resuelven o se eliminan los dos registros pendientes
      (Rodriguez et al. 2025; Becerril‑Carrillo et al. 2025).
- [ ] Portada con integrantes, **índice**, y **borrar** las "Notas de edición".
- [ ] Diagramas exportados a **PNG en modo claro** (variante `'theme':'neutral'` + texto `#333333`
      y `-b white`, ver `docs/README.md`).
- [ ] **`.docx` con GenOffice** (`genoffice`), compatible con Google Docs: títulos nativos de Word,
      fuentes estándar, tablas simples, imágenes incrustadas; sin CSS arbitrario ni HTML crudo.
- [ ] Circulación al equipo para correcciones → **PDF** desde Word/Google Docs.
- [ ] **Andamiaje**: `git init`, `.gitignore`, `README.md`, `pyproject.toml` (deps fijadas),
      `ruff`, `pytest`, `src/` con paquetes y CLI, y la **historia 01** (esqueleto simulado).

### Fase 1 — semana 1: datos (historias 2 y 3)

- Descarga **submuestreada** de Espejel: las 10 glosas elegidas por recuento de imágenes
  (≈ 11 señantes × ~15 frames × 10 palabras ≈ 1 600 imágenes, no las 31 442).
- **Spike de riesgo (día 1 de la fase):** correr MediaPipe Pose + Hands sobre ~20 imágenes del
  dataset. Espejel se grabó con **fondo negro, ropa negra y recortes** → puede que **no encuentre
  el cuerpo** y no haya torso con el que normalizar. Si falla: plan B = solo **Hand Landmarker**
  normalizando por muñeca, o **MSLR** (29 clases, 102 señantes, fondo blanco) como base.
- `landmarks/` en `.npz` por clip, `meta.json` con `senante`/`glosa`/`sesion`, y `splits.json`
  **por señante**.

### Fase 2 — semana 2: modelo y métricas (historias 4, 5 y 7)

- GRU + atención sobre `(B, 32, F, 3)`; AdamW 1e‑3, batch 32, dropout 0,3, semilla 1234.
- **LOSO** con los señantes disponibles; el test ciego **se abre una sola vez** por configuración.
- Salida: `top‑1`, `F1 macro`, matriz de confusión, latencia de inferencia. Meta: **top‑1 ≥ 85 %**
  en señante no visto; si sale 60‑75 %, **se reporta igual** (es un resultado, no un fracaso).

### Fase 3 — semana 3: frase, confianza, offline (historias 6, 8, 9, 10)

- `glossary.yaml` + plantillas; pytest sobre `glosa → frase`; validación de una muestra con un
  firmante externo.
- Umbral de confianza con pedido de repetición; Gradio; `pyttsx3`; `.task` de MediaPipe en el repo.
- Prueba de instalación en una **máquina limpia sin internet**.

### Fase 4 — semana 4: servidor con cuentas y roles (historia 11) + cierre

- **FastAPI + SQLite + login con roles** (administrador/usuario) e historial de frases; inferencia
  en el servidor. El núcleo de ML **no se toca**: la API llama a la misma función `video → frase`.
- Informe de **V. Ingeniería** (2 000‑2 500 palabras) → `.docx` → PDF, y demo.

> **Prioridad honesta:** esta fase es la que más se aleja del objetivo de aprender ML. Si la Fase 2 o
> la 3 se atrasan, **la Fase 4 es la primera en recortarse** (se queda en usuario local único y se
> documenta el porqué en el informe). Se decide en la revisión de la semana 3, no en la última noche.

## Reparto (2 personas programando)

| Persona | Archivos propios | Hace |
|---|---|---|
| **A · Integración y ML** | `src/landmarks`, `src/normalize`, `src/model`, `src/train`, `pyproject.toml` | Pipeline, entrenamiento, métricas, andamiaje |
| **B · Producto y datos** | `src/glossary`, `src/postprocess`, `src/app`, `data/`, `docs/` | Dataset y splits, glosario y plantillas, Gradio + TTS, informe |

Cada quien con su subconjunto de archivos: sin conflictos de fusión y con contribución visible.
Apoyo (sin código): selección de glosas en glosarios, contacto con el firmante validador, revisión
del informe.

## Definition of done (por historia)

`ruff check` y `pytest` en verde **y** la demo corre en CPU de laptop **sin internet** **y** queda
un número o una captura que entra al informe. Sin eso, la historia no está terminada.

## Riesgos principales

| Riesgo | Impacto | Mitigación |
|---|---|---|
| MediaPipe no detecta cuerpo/manos en Espejel (fondo y ropa negras) | Alto: sin landmarks no hay datos | Spike el día 1 de la Fase 1; plan B Hand‑only o MSLR |
| Espejel son **imágenes**, no video (≈15 frames/palabra) → secuencia temporal pobre | Medio: el GRU aprende "firma estática" | Elegir las palabras con más frames; reportar la limitación; el GRU sigue siendo válido |
| top‑1 bajo (p. ej. 55 %) | Medio | Se reporta con matriz de confusión y análisis de confusión entre glosas; es evidencia de aprendizaje supervisado |
| Español de las plantillas suena artificial | Bajo/medio | Plantillas cortas, validadas por firmante; la salida se muestra también en glosas |
| 48 h para informe + código | Alto | El código de la fase 0 es **simulado**: no bloquea la entrega 1 |

## Bitácora de decisiones (nov 2026)

Dataset **Espejel CES 2024** · sin corpus propio · **10 glosas** por disponibilidad · **señas
aisladas** (sin CTC) · **GRU + atención** · **MediaPipe Tasks** Pose+Hands · **CPU** de laptop con
submuestreo **y** GPU+CUDA con versiones fijadas para el entrenamiento final · **Python + PyTorch +
`src/` + ruff/pytest** · **Gradio + `pyttsx3`** · post‑proceso **diccionario + plantillas** ·
**offline** e **instalable** · **cuentas con roles en servidor** (última fase) · **idioma como
dato** · informe de V. Ingeniería **2 000‑2 500 palabras** · informe 1: **un MD → .docx (Google
Docs) → PDF** · **2 personas** programando.
