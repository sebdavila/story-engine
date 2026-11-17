# Handoff — story-engine (Plan escala cerrado 2026-11-17)

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
2. ~~Escalar~~ hecho 2026-11-17: plan `plans/2026-11-17-scale-run.md`, ledger `.superpowers/sdd/2026-11-17-scale-run/progress.md`. 83 archivos en `knowledge/`: F 381, S 191, T 656, Q 635, R 10. Fidelidad 209/213 (98%, mínimo 90%) en `../destilado/escala/fidelidad.md`. Pasada estricta de ejemplos (no recontar el ejemplo de la ficha) en los 37 archivos de frameworks (~176 reescritos) y los 10 de techniques (~139). Sebastián revisó index, frameworks y dominios: ok; mantener plantilla delgada en story types y frases-instrucción cortas entre comillas. Commits finales: destilado (ver `git log`), story-engine (ver `git log`). Plan original: `indice.py` por lote (5 × 11 fichas, orden alfabético) y en total; `lote.md` ×5; `fusion.md` ×3 (F, S, T); concatenar en `escala/clusters.md` y `escala/drop-log.md`; `fuentes.py`; redactores (Sonnet, máximo 4 en paralelo); `verificar.py` con `--books ../md` y `--allow escala/allow.md`; fidelidad por archivo. Los archivos del piloto en `knowledge/` se reemplazan.
3. ~~Índice y congelar IDs~~ hecho: `knowledge/index.md` lo regenera `verificar.py --index`; IDs solo se agregan (regla en el spec, Knowledge entry format).
4. Plan 2: skills, agentes de QA, evals y publicación (repo público `sebdavila/story-engine`, pedir ok antes de publicar). Antes de publicar: excluir o limpiar `docs/superpowers/` (rutas privadas y prompts de destilado) y revisar la línea Common mistakes de F100 (cita el deck de Parikh).

## A tener en cuenta

- Cupo: 7 agentes Opus en paralelo agotaron el límite de 5 horas. Para escalar, usar Sonnet en redactores o menos en paralelo.
- `../destilado/` y `../md/` nunca van al repo público.
