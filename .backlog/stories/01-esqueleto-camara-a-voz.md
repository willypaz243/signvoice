# Story 01 — Setup completo y esqueleto de cámara a voz (walking skeleton)

**Estado:** completa (17/11) · **Entrega 2** (hackathon 16/11) · **T1** (A + F, con el asistente de IA)

## Story

Como desarrollador, quiero clonar el repositorio y tener el entorno completo
(Python 3.11, librerías fijadas) y el esqueleto de punta a punta corriendo, para que
cualquier integrante del equipo pueda empezar a contribuir sin instalar nada a mano.

## Acceptance criteria

- [x] Given clono el repo y corro el setup y el comando de demo, when la página se
      abre, then veo mi webcam y un panel con la glosa predicha (marcada como
      simulada), la frase en español y la reproducción de voz.
- [x] Given estoy frente a la cámara, when mantengo una seña 2 s, then el panel
      muestra un conteo de landmarks detectados distinto de cero y la frase se lee
      en voz alta.
- [x] Given la máquina no tiene internet, when corro la demo, then funciona
      (modelos locales y voz del sistema).

## Reglas de esta story

- **Código 100 % en inglés** (identificadores, docstrings, logs, errores, tests); el
  español solo en los datos que ve u oye el usuario (frase, textos de interfaz, TTS,
  valores del glosario).
- **Programación orientada a objetos:** una clase concreta por preocupación, **sin
  herencia, sin clases base, sin factories ni inyección de dependencias**.
- **Cada función de 9 líneas o menos; cada archivo de 60 líneas o menos.** Si se pasa,
  se parte el archivo (nunca se sube el límite).

## Plan

1. Entorno Python 3.11 con **uv** (`uv python install 3.11` + `uv venv`), librerías
   fijadas y lockfile `uv.lock` versionado; `ruff` y `pytest` como deps de desarrollo
   (DoD global: verde en cada commit).
2. Partir el trayecto completo (cámara → landmarks → glosa → frase → voz) en módulos
   pequeños orientados a objetos. Guía inicial (se parte si un archivo supera 60
   líneas): `capture`, `landmarks`, `normalize`, `simulate`, `postprocess`, `app`,
   más `__init__` y `__main__` (CLI). El contrato de datos fijo —`(32, 75, 3)` +
   `meta{senante, glosa, sesion}`— se mantiene desde el día 1 para enchufar datos
   reales en la Fase 1 sin reescribir.
3. Modelos MediaPipe locales (pose + manos, `.task` en `models/`): landmarks reales
   de la webcam, normalizados al torso.
4. Predicción de glosa simulada (lista fija), diccionario español de las glosas
   piloto (`glossary/LSM.yaml`), plantillas deterministas y voz offline (`pyttsx3`).
5. Interfaz web con un solo comando (webcam en el navegador) y el trayecto de punta
   a punta funcionando sin internet.

## Out of scope

- Dataset Espejel, selección de glosas y splits (story 02) · reconocimiento real
  (stories 03‑05) · matriz de confusión (07) · umbral de confianza (08) ·
  instalación en máquina limpia (09) · config multi‑lengua (10) · servidor con
  cuentas (11) · informe V. Ingeniería (12).
