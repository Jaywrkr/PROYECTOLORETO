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
| ADR-0002 | 2026-09-04 | ACCEPTED | Autorizar una PoC técnica acotada contra infraestructura propia |

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

## ADR-0002 — Autorizar una PoC técnica acotada contra infraestructura propia

| Campo | Contenido |
| --- | --- |
| ID | ADR-0002 |
| Fecha | 2026-09-04 |
| Estado | ACCEPTED |
| Contexto | `ai/AI-INSTRUCTIONS.md` exige autorización explícita y decisiones de alcance suficientes antes de implementar software; hasta ahora el desarrollo de aplicación estaba fuera de alcance. El responsable del proyecto ahora dispone de infraestructura propia (nube/laboratorio interno) para pruebas y pidió explícitamente avanzar hacia una PoC técnica para validar si el producto tiene sentido. |
| Decisión | Se autoriza construir una PoC de flujo completo —no un producto— limitada a: (1) un Collector que se conecta de forma saliente a las fuentes del laboratorio propio, (2) normalización mínima al modelo canónico (`Asset`, `Observation`, `Relationship`) definido en `CANONICAL-DATA-MODEL.md`, y (3) un reporte o vista simple y legible del resultado. Se ejecuta únicamente contra infraestructura propia del responsable del proyecto, nunca contra datos de un cliente real sin una autorización separada. |
| Razón | Sin un flujo extremo a extremo no puede evaluarse si la fricción de instalación, permisos y tiempo hasta el primer valor es aceptable como producto; el modelo canónico y los planes de piloto ya documentados no pueden validarse solo en papel. |
| Alternativas consideradas | Continuar solo con investigación documental; ejecutar únicamente el script de verificación de solo lectura ya existente sin normalización ni reporte. Ambas se descartaron porque no prueban la experiencia real de instalación ni el modelo canónico en código. |
| Consecuencias | Se introduce código de aplicación en el repositorio (fuera de `research/pilot-scripts`) por primera vez. Sigue sin existir selección de stack, nube, base de datos o proveedor de IA definitiva: el código de la PoC es desechable y no compromete esas decisiones. La PoC no debe conectarse a datos ni credenciales de un cliente real. Cualquier avance de la PoC hacia producto (multi-tenancy real, despliegue, clientes) requiere una decisión de alcance adicional. |

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
