# Contexto del proyecto para humanos y agentes

> **Leer antes de trabajar.** Última actualización: 2026-08-29.

## Misión del repositorio

Ser la fuente oficial de verdad para el descubrimiento de Proyecto Loreto, manteniendo el contexto verificable y transferible entre Coresolutions, desarrolladores humanos y agentes de IA.

## Estado actual

- **CONFIRMED:** El trabajo actual es descubrimiento, definición y arquitectura conceptual.
- **CONFIRMED:** No se debe desarrollar el producto ni escribir código de aplicación todavía.
- **HYPOTHESIS:** El producto podría ser una capa inteligente para infraestructura heterogénea de clientes de Coresolutions.
- **CONFIRMED:** El aislamiento de información entre clientes es un requisito de diseño.
- **HYPOTHESIS:** Podría existir un Collector en la infraestructura del cliente y una plataforma central multi-tenant.
- **HYPOTHESIS:** Algunos clientes podrían requerir una instalación completamente on-premise.

## Convenciones de estado

| Estado | Uso |
| --- | --- |
| `CONFIRMED` | Hecho o requisito proporcionado, validado o explícitamente aprobado. |
| `HYPOTHESIS` | Suposición plausible pendiente de validación. |
| `TO INVESTIGATE` | Tema que requiere investigación, evidencia o análisis. |
| `OPEN QUESTION` | Pregunta sin respuesta y con impacto potencial. |
| `REJECTED` | Alternativa considerada y descartada, con razón documentada. |
| `DEPRECATED` | Contexto histórico que ya no guía el trabajo actual. |
| `NOT STARTED` | Trabajo previsto que aún no se ha iniciado. |
| `COMPLETED` | Trabajo documental o de investigación que terminó, con evidencia enlazada. |

Los estados de ADR son distintos y se definen en [DECISIONS.md](../development/DECISIONS.md).

## Fuente y precedencia

1. Instrucciones explícitas y recientes de los responsables del producto.
2. Decisiones `ACCEPTED` en [DECISIONS.md](../development/DECISIONS.md).
3. Evidencia enlazada y documentos del dominio correspondiente.
4. Este contexto y el handoff más reciente.
5. Hipótesis claramente etiquetadas.

Si existe conflicto, no inventes una reconciliación: señálalo, conserva el historial y solicita o registra una decisión.

## Navegación rápida

- Intención y alcance: [PRODUCT-BLUEPRINT.md](../product/PRODUCT-BLUEPRINT.md)
- Casos de uso: [USE-CASES.md](../product/USE-CASES.md)
- Arquitectura: [ARCHITECTURE.md](../architecture/ARCHITECTURE.md)
- Seguridad y aislamiento: [SECURITY.md](../architecture/SECURITY.md), [MULTITENANCY.md](../architecture/MULTITENANCY.md)
- Conectores: [CONNECTORS.md](../architecture/CONNECTORS.md)
- Investigación inicial: [README.md](../research/README.md)
- Decisiones: [DECISIONS.md](../development/DECISIONS.md)
- Estado de sesión: [HANDOFF.md](HANDOFF.md)
