# Modelo canónico de datos — candidato para el MVP

> **Estado: HYPOTHESIS.** Última actualización: 2026-08-30. Es un modelo conceptual para orientar la prueba de factibilidad; no es un esquema de base de datos ni una decisión de implementación.

## Objetivo

Dar un lenguaje común a fuentes distintas sin ocultar de dónde proviene cada dato. El modelo debe permitir que la misma pantalla muestre información de vSphere y de una fuente de servidores, preservando tenant, fuente, hora de lectura y calidad.

## Principios

1. Todo dato operativo pertenece a un único tenant.
2. Un dato canónico no elimina su procedencia: debe poder rastrearse a fuente, identificador externo y lectura.
3. Las relaciones observadas se distinguen de relaciones inferidas.
4. Los campos ausentes, obsoletos o incompatibles son resultados visibles, no valores silenciosamente inventados.
5. El modelo separa identidad de activo, observaciones de una fuente y estado derivado para evitar sobreescribir historia.

## Entidades conceptuales

| Entidad | Propósito | Campos mínimos candidatos | Estado |
| --- | --- | --- | --- |
| `Tenant` | Límite de aislamiento y propiedad de datos | `tenant_id`, alias no sensible, estado | CONFIRMED como necesidad de aislamiento; campos HYPOTHESIS |
| `Source` | Representa una fuente autorizada, por ejemplo vCenter o iLO | `source_id`, `tenant_id`, familia, versión, estado, última lectura | HYPOTHESIS |
| `Collector` | Representa un agente local si el despliegue lo requiere | `collector_id`, `tenant_id`, versión, estado, última conexión | HYPOTHESIS |
| `SyncRun` | Describe una ejecución de lectura de una fuente | `sync_run_id`, `tenant_id`, `source_id`, inicio, fin, resultado saneado | HYPOTHESIS |
| `Asset` | Identidad canónica de un componente dentro de un tenant | `asset_id`, `tenant_id`, tipo, alias, estado derivado | HYPOTHESIS |
| `Observation` | Afirma que una fuente observó un atributo de un activo en un momento | `observation_id`, `tenant_id`, `asset_id`, `source_id`, campo, valor permitido, hora, calidad | HYPOTHESIS |
| `Relationship` | Conecta dos activos del mismo tenant | `relationship_id`, `tenant_id`, origen, destino, tipo, método, fuente, hora, confianza | HYPOTHESIS |
| `DataQuality` | Expresa completitud, actualidad y errores sin ocultarlos | estado, motivo saneado, hora de evaluación | HYPOTHESIS |

## Relaciones entre entidades

```text
Tenant
 ├─ Source ──> SyncRun
 ├─ Collector (opcional)
 └─ Asset ──> Observation <── Source
       └─ Relationship ──> Asset
```

`tenant_id` es obligatorio en todas las entidades que contengan datos operativos. Una relación nunca puede enlazar activos de tenants distintos.

## Tipos de activo iniciales

**HYPOTHESIS:** El piloto intentará normalizar únicamente los siguientes tipos, si la fuente los expone:

| Dominio | Tipos candidatos | Fuente inicial probable |
| --- | --- | --- |
| Virtualización | datacenter, cluster, host, VM, datastore | vCenter/vSphere |
| Hardware | servidor físico, controlador de gestión | Lenovo XClarity o HPE iLO/Redfish |

Otros tipos —switch, firewall, storage, backup, aplicación, servicio y usuario— quedan fuera del modelo del piloto hasta contar con evidencia y una decisión de alcance.

## Tipos de relación iniciales

| Relación | Ejemplo | Regla de visualización |
| --- | --- | --- |
| `contains` | cluster contiene host | Mostrar solo si la fuente lo observa |
| `runs_on` | VM se ejecuta en host/cluster | Mostrar con fuente y hora |
| `uses_storage` | VM usa datastore | Mostrar con fuente y hora |
| `managed_by` | servidor físico gestionado por una fuente | Mostrar como relación técnica, no como propiedad comercial |

Los tipos `depends_on`, `impacts` y `connected_to` son **TO INVESTIGATE**: no deben aparecer como hechos en el MVP sin una fuente o regla explícita.

## Procedencia y calidad

Cada atributo y relación que llegue a una vista debe poder responder, como mínimo:

- ¿de qué `Source` provino?
- ¿cuándo se leyó?
- ¿qué `SyncRun` lo produjo?
- ¿está completo, parcial, obsoleto o con error?
- ¿fue observado directamente o inferido?

**HYPOTHESIS:** Estados de calidad candidatos: `COMPLETE`, `PARTIAL`, `STALE`, `UNAVAILABLE` y `ERROR`. Sus umbrales de tiempo y significado se definirán después de probar las fuentes.

## Reglas de identidad y consolidación

- Un `Asset` puede tener múltiples identificadores externos de fuentes distintas, pero la consolidación automática es **TO INVESTIGATE**.
- Durante el piloto, si no existe una coincidencia inequívoca, los activos deben permanecer separados y la ambigüedad debe mostrarse.
- Nunca usar una dirección IP, nombre o serial por sí solo como prueba universal de identidad entre fuentes.
- Los secretos, tokens, contraseñas y payloads completos no forman parte de este modelo canónico.

## Mapeo de prueba propuesto

| Fuente | Objeto de origen | `Asset` candidato | Relación candidata | Riesgo a validar |
| --- | --- | --- | --- | --- |
| vCenter/vSphere | VM | máquina virtual | `runs_on`, `uses_storage` | Cobertura y permisos por versión |
| vCenter/vSphere | host / cluster / datastore | host / cluster / datastore | `contains` | Semántica y actualidad de relaciones |
| XClarity o iLO/Redfish | servidor gestionado | servidor físico | `managed_by` | Cobertura por generación y firmware |

## Fuera de alcance del modelo actual

- Esquema físico, API, motor de grafos, base de datos o estrategia de deduplicación definitiva.
- Retención de payloads de origen y políticas detalladas de residencia de datos.
- Eventos, alertas, configuración histórica, lifecycle, vulnerabilidades o acciones automatizadas.
- Permisos completos de usuario, aunque toda entidad conserva el límite de tenant.

## Validación requerida

El [plan de piloto de solo lectura](../research/PILOT-READONLY-PLAN.md) debe confirmar qué campos y relaciones son recuperables. Al finalizar, registrar un ADR si se aprueba o modifica este modelo para un MVP real.
