# Especificación funcional del MVP candidato

> **Estado: HYPOTHESIS.** Última actualización: 2026-08-30. Esta especificación describe un prototipo de validación; no autoriza desarrollo ni establece requisitos finales.

## Propósito

Convertir la hipótesis de MVP en una experiencia verificable: permitir que un usuario autorizado de un tenant consulte inventario y salud de fuentes seleccionadas, entienda la procedencia de los datos y explore relaciones directas entre activos.

La referencia visual se mantiene en la conversación y representa únicamente un flujo conceptual; los nombres, conteos y estados mostrados son datos ficticios.

## Usuarios potenciales

| Perfil | Necesidad candidata | Permisos a validar |
| --- | --- | --- |
| Operador de cliente | Comprender inventario, estado y relaciones de su entorno | Lectura dentro de su tenant |
| Especialista de Coresolutions | Apoyar diagnóstico y revisión operativa autorizada | Lectura delegada y auditada dentro del tenant asignado |
| Administrador de tenant | Configurar fuentes y revisar sincronizaciones | Administración solo de su tenant |

No se han definido todavía roles, permisos ni modelo de delegación final.

## Flujo funcional mínimo

### 1. Vista de infraestructura

**HYPOTHESIS:** El usuario ve únicamente el tenant autorizado, sin selector que permita enumerar otros tenants. Puede consultar una lista de activos con:

- nombre o alias del activo;
- tipo de activo;
- estado observado;
- fuente de información;
- última lectura y calidad del dato.

Los filtros candidatos son tecnología/fuente, tipo de activo, estado y antigüedad de lectura. Cualquier filtro debe conservar el alcance del tenant.

### 2. Detalle y relaciones directas

**HYPOTHESIS:** Al seleccionar un activo, el usuario ve sus atributos relevantes, fuente, hora de lectura, calidad y relaciones directas. Cada relación debe indicar si fue observada en una fuente o inferida por una regla futura.

Para el piloto no se requiere un grafo completo, análisis de impacto ni mapa de red. La prioridad es que las relaciones presentadas sean trazables y no induzcan una confianza mayor que la evidencia disponible.

### 3. Configuración de fuentes

**HYPOTHESIS:** Un administrador del tenant puede revisar el estado de preparación de Collector y fuentes, pero la interfaz nunca muestra secretos. La configuración debe representar:

- tenant y límites de retención aprobados;
- estado de Collector, si se usa;
- fuente vCenter/vSphere;
- una fuente de servidores: Lenovo XClarity Administrator o HPE iLO/Redfish;
- última sincronización, errores saneados y resultado de revisión de aislamiento.

La creación real de cuentas, la instalación de un Collector y la modificación de infraestructura siguen fuera de alcance hasta que exista autorización del entorno de piloto.

## Datos que debe mostrar el MVP candidato

| Vista | Datos mínimos candidatos | Evidencia necesaria |
| --- | --- | --- |
| Inventario | Activo, tipo, fuente, estado, última lectura, calidad | Prueba de lectura contra una fuente autorizada |
| Detalle | Atributos permitidos, procedencia, hora, relaciones directas | Mapeo de campos y relaciones observadas |
| Configuración | Fuente, versión, estado de sincronización y errores saneados | Resultado de conectividad, permisos y controles |

## Límites explícitos

- Solo lectura: ninguna acción cambia la infraestructura del cliente.
- No hay alertas automáticas, recomendaciones ni remediación.
- No se expone MCP ni una interfaz a agentes externos.
- No se garantiza descubrimiento de red, lifecycle completo ni cobertura de todos los fabricantes.
- No se define stack, interfaz tecnológica, esquema físico de datos ni proveedor de IA.

## Criterios de éxito de la experiencia piloto

1. Un usuario de tenant autorizado ve solo sus datos.
2. Un activo recuperado muestra fuente y hora de lectura.
3. Al menos un tipo de relación vSphere puede visualizarse con procedencia clara.
4. La fuente de servidores elegida aporta inventario y una señal de salud útil, o registra de forma visible su limitación.
5. Las configuraciones y errores no exponen secretos ni detalles sensibles innecesarios.

## Preguntas abiertas

1. ¿Qué atributos concretos son útiles para cada tipo de activo y cuáles se deben ocultar?
2. ¿Cómo interpreta el usuario los estados `saludable`, `revisar`, `parcial` y `sin datos`?
3. ¿Qué acciones de configuración puede realizar Coresolutions en nombre del cliente?
4. ¿Qué visualización de relaciones aporta valor suficiente antes de construir un grafo completo?

## Documentos relacionados

- [Blueprint de producto](PRODUCT-BLUEPRINT.md)
- [Plan de piloto de solo lectura](../research/PILOT-READONLY-PLAN.md)
- [Modelo canónico de datos](../architecture/CANONICAL-DATA-MODEL.md)
- [Multi-tenancy](../architecture/MULTITENANCY.md)
