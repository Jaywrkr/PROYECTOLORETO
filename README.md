# Proyecto Loreto — documentación de descubrimiento

> **Estado del proyecto: HYPOTHESIS.** Este repositorio documenta la exploración de un producto de Coresolutions; no contiene ni autoriza todavía desarrollo de aplicación.

## Propósito

Proyecto Loreto explora una capa inteligente para que Coresolutions y sus clientes comprendan infraestructura tecnológica heterogénea. La hipótesis abarca descubrimiento, inventario, relaciones, consultas en lenguaje natural y exposición autorizada a agentes mediante MCP. No sustituye las herramientas de administración de los fabricantes.

Este repositorio es la fuente oficial de verdad para personas y agentes de IA. Su función es conservar contexto, distinguir decisiones de hipótesis y hacer visible qué investigar después.

## Antes de contribuir

1. Lee [PROJECT-CONTEXT.md](ai/PROJECT-CONTEXT.md), [DECISIONS.md](development/DECISIONS.md) y [HANDOFF.md](ai/HANDOFF.md).
2. Usa los estados definidos en [PROJECT-CONTEXT.md](ai/PROJECT-CONTEXT.md#convenciones-de-estado).
3. No presentes una hipótesis como una decisión ni desarrolles software sin una decisión documentada que cambie el alcance.
4. Al terminar trabajo significativo, actualiza HANDOFF y CHANGELOG; registra las decisiones relevantes en DECISIONS.

Las instrucciones completas para agentes están en [AI-INSTRUCTIONS.md](ai/AI-INSTRUCTIONS.md).

## Mapa de documentación

| Área | Documento de entrada | Contenido |
| --- | --- | --- |
| Producto | [MVP-SPECIFICATION.md](product/MVP-SPECIFICATION.md) | Experiencia, límites y criterios del MVP candidato. |
| Arquitectura | [CANONICAL-DATA-MODEL.md](architecture/CANONICAL-DATA-MODEL.md) | Modelo conceptual de tenant, fuentes, activos, observaciones y relaciones. |
| Investigación | [README.md](research/README.md) | Evidencia externa, análisis inicial y límites de las conclusiones. |
| Desarrollo | [PILOT-CHARTER.md](development/PILOT-CHARTER.md) | Alcance, roles, puertas y decisión posterior al piloto. |
| Continuidad | [HANDOFF.md](ai/HANDOFF.md) | Estado de la última sesión y siguiente paso recomendado. |

## Límites actuales

- No hay código de aplicación, proveedor cloud, esquema de datos, APIs ni integraciones seleccionados.
- Las capacidades por fabricante, la competencia, el modelo comercial, costos y viabilidad son temas por investigar.
- La separación estricta entre clientes es un requisito de diseño a preservar; su implementación concreta permanece abierta.

## Historial

Consulta [CHANGELOG.md](development/CHANGELOG.md) para cambios documentales y [DECISIONS.md](development/DECISIONS.md) para decisiones de arquitectura, producto y proceso.
