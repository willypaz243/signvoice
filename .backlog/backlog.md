# Backlog — Traductor LSM → voz (Grupo 11)

> Stories para el tracker. Este archivo guarda el contexto, la stack y las decisiones caras.
> El plan con fechas y fases está en `plan.md`. La historia 01 está desarrollada en detalle en `stories/`.

## Context

Práctica universitaria de IA: **reconocimiento de señas y conversión a voz** con **aprendizaje
supervisado + visión por computadora** sobre la **Lengua de Señas Mexicana (LSM)**. Una persona señ
frente a una webcam y el sistema produce la frase en español y la **lee en voz alta**.

- **3 entregas.** La 1.ª (10/nov) es el informe I. Introducción, II. Objetivos, III. Marco teórico,
  IV. Marco referencial; la sección **V. Ingeniería se inicia** y es materia de la 2.ª entrega.
- **Regla de la práctica:** se evalúa **aprender ML supervisado**, no el estado del arte. Se gana con
  un experimento chico y **creíble**, no con un sistema grande.
- **Restricción de equipo:** no hay experto en LSM. **Las etiquetas vienen de datasets públicos
  ya etiquetados** y el vocabulario de glosarios de referencia; el español generado lo valida un
  firmante externo. Nada de inventar glosas ni sintaxis.
- **Regla de ingeniería:** lo **más simple y minimalista** con buenas prácticas. Sin capas, sin
  frameworks, sin abstracciones "por si acaso". Un módulo se justifica solo si ya hay dos usos.

**Principio de diseño:** el trayecto completo `cámara → landmarks → glosa → español → voz` existe
desde la primera historia, con predicción simulada; los datos y el modelo se enchufan a un camino
que ya funciona.

**Modelo de dominio:**

- **Glosa** = etiqueta de una seña aislada (viene del dataset). Vocabulario de la práctica: **10 glosas**.
- **Clip** = secuencia de `T=32` frames × `F` landmarks × 3 coordenadas, con metadatos de señante y sesión.
- **Señante** = unidad de validación. El split es **por señante** (LOSO), nunca por clip.
- **Frase** = secuencia de glosas convertida a español por **diccionario + plantillas**.

## Stack

| Pieza | Decisión |
|---|---|
| Lenguaje | **Python 3.11** |
| Datos / experimentos | **PyTorch** (CPU; GPU+CUDA con versiones fijadas para el entrenamiento final) |
| Landmarks | **MediaPipe Tasks**: Pose Landmarker + Hand Landmarker (`.task` locales, sin red) |
| Dataset base | **Espejel-Cabrera et al. 2024** (Mendeley, CC BY 4.0): 249 palabras LSM, 31 442 imágenes, 11 señantes sordos |
| Vocabulario | **10 glosas** elegidas por disponibilidad de clips, validadas en GDLSM/FENAMAS/SIGNA |
| Modelo | **GRU (2 capas) + atención temporal**, salida softmax sobre las 10 glosas |
| Post-proceso | **`glossary.yaml` + plantillas deterministas** (SVO, artículos, conjugación, marca de pregunta) |
| Voz | **`pyttsx3`** (offline, voz del sistema) |
| Interfaz | **Gradio** (webcam en navegador) + **CLI `typer`** para el pipeline por lotes |
| Config | **YAML** (idioma, glosario, cámara, umbral de confianza, voz) |
| Calidad | **git** + **ruff** + **pytest** (módulos deterministas) + `pyproject.toml` con deps fijadas |
| Documentación | `docs/` en Markdown; informe en **1 MD → .docx (Google Docs) → PDF** |

**Migración a servidor** (fase final): el pipeline ya es una función pura `video → frase → wav`;
encima se monta **FastAPI + SQLite + login con roles** sin tocar el núcleo de ML.

## Decisiones caras

- **100 % offline** en la demo: modelos MediaPipe y voces van en el repo/entorno; sin llamadas de red.
- **Instalable en la máquina del público**: entorno con `pyproject.toml` + deps fijadas y una
  `make demo` / un comando; se prueba en una máquina limpia.
- **Multiusuario con cuentas y roles, e inferencia en servidor** — **aplica, pero no es lo primero**:
  es la última fase. El núcleo se escribe sin dependencias de UI ni de sesión para que ese paso
  sea añadir una capa, no reescribir.
- **Preparado para otras lenguas de señas**: el idioma es **dato, no código** (glosario y config por
  lengua). Sin abstracciones de i18n.
- **Un solo dispositivo de captura** (webcam). Sin app móvil, sin sincronización, sin multi-tenant.

## Backlog

1. Como señante, quiero señalar una seña frente a la webcam y **escuchar una frase en voz alta**,
   aunque la predicción sea simulada, para verificar que el trayecto cámara→landmarks→glosa→español→voz
   funciona de punta a punta.
2. Como evaluador, quiero ver de dónde salen los datos (dataset, licencia, las 10 glosas con sus
   clips y señantes), para creerme que el experimento es reproducible. Requires: #1
3. Como señante, quiero que el sistema reconozca **una glosa real** desde mi cámara y la muestre en
   pantalla, para confirmar que los landmarks de mi webcam son compatibles con los del dataset. Requires: #2
4. Como evaluador, quiero ver **top‑1 y F1 macro al dejar fuera a un señante** (LOSO) en el
   entrenamiento, para que el número del modelo no venga de memorizar a la persona. Requires: #3
5. Como señante, quiero que el sistema reconozca **las 10 glosas**, para poder armar mensajes de
   varias palabras. Requires: #4
6. Como oyente, quiero **escuchar una frase de 2‑3 palabras en español** construida con
   diccionario y plantillas, para que el mensaje se entienda. Requires: #5
7. Como evaluador, quiero ver la **matriz de confusión** y los pares de glosas más confundidos,
   para explicar el error con evidencia. Requires: #5
8. Como señante, quiero que el sistema **avise cuando no está seguro** y me pida repetir, para no
   escuchar frases inventadas. Requires: #6
9. Como presentador, quiero **correr toda la demo sin internet y con un comando**, para
   demostrarla en el aula sin conexión ni instalación. Requires: #6
10. Como usuario, quiero **cambiar el glosario/idioma desde la configuración** y que la salida
    cambie, para que el sistema sea reutilizable en otra lengua de señas. Requires: #6
11. Como usuario con cuenta, quiero **iniciar sesión y que el video se procese en el servidor**
    (roles administrador/usuario, historial de frases), para usar el traductor en la práctica
    real sin instalar nada en cada máquina. Requires: #6, #9
12. Como docente, quiero un informe de la sección **V. Ingeniería** (2 000‑2 500 palabras:
    arquitectura, datos, método, métricas, matriz de confusión) entregable como **.docx y PDF**,
    para calificar la 2.ª entrega. Requires: #4, #6

> 12 historias. Lo que no está aquí, no se hace en la práctica (ver `plan.md` → "Fuera de alcance").
