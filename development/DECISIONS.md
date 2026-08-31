# Registro de decisiones

> Este registro usa un formato ADR ligero. Solo se registran decisiones explícitas; las hipótesis y preguntas permanecen en sus documentos de origen hasta que se decidan.

## Cómo usar este registro

- Asigna un ID secuencial (`ADR-0001`, `ADR-0002`, ...).
- Añade fecha ISO 8601 y uno de los estados: `PROPOSED`, `ACCEPTED`, `REJECTED`, `DEPRECATED`, `SUPERSEDED`.
- No edites el contenido histórico de una decisión aceptada para cambiar su sentido; crea una nueva decisión y enlázala.
- Registra razón, evidencia, alternativas y consecuencias, incluidas las negativas.

## Índice

| ID | Fecha | Estado | Título |
| --- | --- | --- | --- |
| ADR-0001 | 2026-08-29 | ACCEPTED | Usar el repositorio como fuente de verdad de descubrimiento |

---

## ADR-0001 — Usar el repositorio como fuente de verdad de descubrimiento

| Campo | Contenido |
| --- | --- |
| ID | ADR-0001 |
| Fecha | 2026-08-29 |
| Estado | ACCEPTED |
| Contexto | El proyecto necesita continuidad entre personas y distintos agentes de IA antes de iniciar desarrollo. |
| Decisión | Mantener en este repositorio la documentación de producto, arquitectura, proceso, decisiones, cambios y handoffs. |
| Razón | Centraliza el contexto versionado, hace explícita la incertidumbre y facilita la revisión. |
| Alternativas consideradas | Notas dispersas o decisiones mantenidas solo en conversaciones. |
| Consecuencias | Cada cambio relevante debe actualizar los documentos afectados, CHANGELOG y HANDOFF; no se debe borrar contexto histórico relevante sin justificación. |

## Plantilla

```md
## ADR-NNNN — Título

| Campo | Contenido |
| --- | --- |
| ID | ADR-NNNN |
| Fecha | AAAA-MM-DD |
| Estado | PROPOSED / ACCEPTED / REJECTED / DEPRECATED / SUPERSEDED |
| Contexto | Problema y evidencia disponible. |
| Decisión | Decisión explícita. |
| Razón | Por qué se toma. |
| Alternativas consideradas | Opciones y por qué no se eligen. |
| Consecuencias | Efectos, riesgos, coste y trabajo posterior. |
```
