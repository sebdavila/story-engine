# Handoff — story-engine (Plan 2 cerrado 2026-11-17)

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
4. ~~Plan 2: plugin local~~ hecho 2026-11-17: plan `plans/2026-11-17-plugin.md`, ledger `.superpowers/sdd/2026-11-17-plugin/progress.md`. 5 skills, 2 agentes de QA (knowledge-auditor, story-reviewer), 15 evals (`evals/run.sh`, `evals/check.py`), README, SOURCES, LICENSE.
   - Evals: ronda 1 con fallos de enrutamiento, entrega y checker; ronda 2 10/15 mecánico, calidad aprobada por Sebastián 8/8 (caso 8 "aburrido" pero con buena estructura); ronda 3 15/15 mecánico y 15/15 calificado, tras corregir un falso negativo del checker (caso 15) y la expectativa del caso 7 (aceptar una fila de Goal map de science; ok de Sebastián). Resultados en `../story-engine-workspace/round-N/`.
   - Umbral gate 2: 14/20 se mantiene (textos genéricos 2–11, borradores buenos 14–18).
   - Instalado en local: `claude plugin marketplace add <repo>` + `claude plugin install story-engine@story-engine`; prueba con el caso 6 ok.
   - Funciona completo en Claude Code y Cowork. En el chat de claude.ai cargan las skills pero no los agentes (sin gates).
5. Plan 3: publicación (repo público `sebdavila/story-engine`). Pedir ok explícito antes de crear el repo o hacer push. Checklist:
   - excluir o limpiar `docs/superpowers/` (rutas privadas y prompts de destilado);
   - revisar la línea Common mistakes de F100 (cita el deck de Parikh);
   - historial de git: tiene rutas privadas; publicar desde historial limpio;
   - confirmar titular de LICENSE ("sebdavila");
   - simulacro 2026-11-17: 105 archivos públicos, sin texto privado.

## A tener en cuenta

- Cupo: 7 agentes Opus en paralelo agotaron el límite de 5 horas. Para escalar, usar Sonnet en redactores o menos en paralelo.
- `../destilado/` y `../md/` nunca van al repo público.

## Menores pendientes (revisión final del Plan 2)

La revisión final (Opus) no encontró críticos. Corregidos los 3 importantes (commit 7c62a47): patrón del índice sin escapar, lecturas mal contadas en `evals/check.py`, ruta "ninguna fila del Goal map" sin salida (corregida en texto, sin eval que la ejercite). Quedan, sin arreglar:

- Etiquetas fuera del trace (`## QA pending`, `Auditor verdict`, `Reviewer score`, `[ask: ...]`) no fijadas en inglés; el modelo a veces las traduce y `check.py` no las ve.
- story-draft cambia la pieza después de la última ronda de QA; el veredicto mostrado describe otra versión.
- `check.py` solo verifica IDs dentro del trace (no los de mining, review o QA pending).
- Plan 3: probar la instalación desde git después del push.
- Evals: desinstalar el plugin de usuario antes de correrlas (se carga doble con `--plugin-dir`); los plugins personales de la máquina influyen en el enrutamiento.
- story-review: el bloque de brief contradice "No preamble"; poner el brief después de la línea del puntaje.
- README:41 dice que los agentes "never see how it was made"; falso para el auditor.
- Caso 15 se saltó story-structure; la eval no lo exige.
- `check.py` sin argumento falla con IndexError.
