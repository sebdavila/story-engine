# Handoff — story-engine (pausado 2026-11-17)

Para retomar: abrir Claude Code en `/Users/sdavila/Desktop/Storytelling/story-engine` y decir "retoma story-engine desde el HANDOFF".

## Dónde va

Plan 1 (piloto de conocimiento, negocio): `docs/superpowers/plans/2026-11-13-knowledge-pipeline-pilot.md`
Ledger con decisiones (Ruling 1–12) y avance: `.superpowers/sdd/2026-11-13-knowledge-pipeline-pilot/progress.md`

| Tarea | Estado |
|---|---|
| 1. Índice de fichas | Hecha |
| 2. Verificador | Hecha |
| 3. Clusters (F46, S23, T108) | Hecha |
| 4. 13 archivos en `knowledge/` | Hecha (commit 8c0d63d) |
| 5. Fidelidad | Hecha 2026-11-17: 16/20 en la primera pasada, 20/20 tras corregir F08, F16, F25, S15 y etiquetar la convención de rubric.md. Detalle en `../destilado/piloto/fidelidad.md` |

Fichas: las 55 están hechas con Gemini (`../destilado/fichas-gemini/`).

## Siguientes pasos

Piloto cerrado 2026-11-17: Sebastián aprobó structure.md y business.md; revisión final "con arreglos" (los arreglos bloquean el escalado, no el piloto).

1. Antes de escalar a 55 fichas (de la revisión final; 614 encabezados de framework vs 101 del piloto):
   - IDs de 3 dígitos para F y S (`F001`): hoy `ID_RE` en `verificar.py` es `F\d\d` y F100+ pasaría sin verificar. Cambiar regex, prompt de clusters y test.
   - Chequeo inverso en `ids()`: cada ID de clusters definido exactamente una vez en knowledge/ (hoy un cluster recortado por presupuesto pasa en silencio).
   - Partir techniques, story-types y questions por familia, como frameworks (Ruling 8); ya están al límite de 5K tokens.
   - Clustering por lotes (secciones.md sería ~230k palabras) y `coverage()` también para Story types y Techniques.
   - `--allow FILE` para falsos positivos aceptados de comillas, y `--books` obligatorio con `--knowledge`.
   - Regla en el prompt de redactores: cada paso debe salir de una ficha. Muestra de fidelidad por archivo, no 20 en total.
   - Parametrizar prompts (hoy dicen `piloto/` y "11 books").
   - Decidir dónde van oral, leadership, marketing y sales (22–31 fichas cada uno).
2. Escalar: tareas 1–5 con las 55 fichas; crear `brand.md`, `personal.md`, `craft.md`, `data.md`, `science.md` (ojo: nombres chocan con `frameworks/data.md` y `frameworks/brand.md` en la salida del verificador).
3. Después del escalado: `knowledge/index.md` (ID → archivo) generado por script, y congelar IDs (solo agregar).
4. Plan 2: skills, agentes de QA, evals y publicación (repo público `sebdavila/story-engine`, pedir ok antes de publicar). Antes de publicar: excluir o limpiar `docs/superpowers/` (rutas privadas y prompts de destilado) y reescribir los ejemplos F21 y F10 (repiten ejemplos de Hall y Parikh).

## A tener en cuenta

- Cupo: 7 agentes Opus en paralelo agotaron el límite de 5 horas. Para escalar, usar Sonnet en redactores o menos en paralelo.
- `../destilado/` y `../md/` nunca van al repo público.
