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

1. ~~Fidelidad~~ hecha.
2. Revisión de Sebastián: `knowledge/frameworks/structure.md` y `knowledge/business.md`.
3. Revisión final del plan (code reviewer sobre ambos repos) y cerrar el ledger.
4. ~~Minors antes de escalar~~ hechos 2026-11-17 (destilado 33ae8e7): `indice.py` quita "(Part …)", `verificar.py` empareja comillas por tramo. Falsos positivos del piloto: 6 a 3, todos ejemplos originales.
5. Escalar: correr tareas 1–5 con las 55 fichas y crear `brand.md`, `personal.md`, `craft.md`, `data.md`, `science.md`.
6. Plan 2: skills, agentes de QA, evals y publicación (repo público `sebdavila/story-engine`, pedir ok antes de publicar).

## A tener en cuenta

- Cupo: 7 agentes Opus en paralelo agotaron el límite de 5 horas. Para escalar, usar Sonnet en redactores o menos en paralelo.
- `../destilado/` y `../md/` nunca van al repo público.
