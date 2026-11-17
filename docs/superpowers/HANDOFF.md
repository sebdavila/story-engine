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

1. ~~Antes de escalar~~ hecho 2026-11-17: plan `plans/2026-11-17-pre-scale-fixes.md`, destilado f4c763d..ae6e814. IDs de 3 dígitos, un hogar por ID, cobertura de los tres tipos (incluye sub-ítems en cursiva), `--allow`, `--books` obligatorio, `fuentes.py`, prompts map-reduce (`lote.md`, `fusion.md`), redactores desde fuentes, fidelidad por archivo. Guías de dominio: una por dominio en `knowledge/domains/` (10).
2. Escalar (siguiente plan): `indice.py` por lote (5 × 11 fichas, orden alfabético) y en total; `lote.md` ×5; `fusion.md` ×3 (F, S, T); concatenar en `escala/clusters.md` y `escala/drop-log.md`; `fuentes.py`; redactores (Sonnet, máximo 4 en paralelo); `verificar.py` con `--books ../md` y `--allow escala/allow.md`; fidelidad por archivo. Los archivos del piloto en `knowledge/` se reemplazan.
3. Después del escalado: `knowledge/index.md` (ID → archivo) generado por script, y congelar IDs (solo agregar).
4. Plan 2: skills, agentes de QA, evals y publicación (repo público `sebdavila/story-engine`, pedir ok antes de publicar). Antes de publicar: excluir o limpiar `docs/superpowers/` (rutas privadas y prompts de destilado) y reescribir los ejemplos F21 y F10 (repiten ejemplos de Hall y Parikh).

## A tener en cuenta

- Cupo: 7 agentes Opus en paralelo agotaron el límite de 5 horas. Para escalar, usar Sonnet en redactores o menos en paralelo.
- `../destilado/` y `../md/` nunca van al repo público.
