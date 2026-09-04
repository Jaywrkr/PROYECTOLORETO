# Opciones estructurales: aislamiento multi-tenant y arquitectura del Collector

> **Estado: TO INVESTIGATE.** Investigación de escritorio realizada el 2026-09-04. No sustituye una prueba técnica ni una decisión de arquitectura. No selecciona tecnología ni proveedor.

## Propósito

`architecture/MULTITENANCY.md` y `architecture/CONNECTORS.md` dejan abiertas dos preguntas que no son de alcance de MVP sino de arquitectura de fondo: la estrategia de aislamiento por tenant y la forma que toma el Collector. Ambas condicionan el modelo de datos, el despliegue y el piloto, y son costosas de cambiar después de construir. Este documento compara opciones conocidas de la industria para que una decisión futura (ADR) tenga evidencia de partida, sin cerrar el debate.

## Por qué estas dos preguntas van antes que la selección de conectores

- El modelo canónico (`CANONICAL-DATA-MODEL.md`) exige `tenant_id` obligatorio en toda entidad, pero no dice cómo se hace cumplir ese límite a nivel de almacenamiento, cómputo y agentes MCP.
- El Collector es el único componente que se ejecuta dentro de la red del cliente; su forma determina qué es operacionalmente viable en el piloto (RB-004 del backlog) antes de evaluar cualquier fabricante adicional.
- Cambiar la estrategia de aislamiento o la naturaleza del Collector después de escribir el primer conector implica rehacer, no extender.

## Parte 1 — Estrategias de aislamiento multi-tenant

| Estrategia | Descripción | Ventajas | Riesgos / costes |
| --- | --- | --- | --- |
| Base de datos compartida + `tenant_id` y controles lógicos (p. ej. Row-Level Security en Postgres) | Todos los tenants en las mismas tablas; cada fila lleva `tenant_id` y una política a nivel de motor de datos filtra el acceso. | Menor coste operativo, más fácil de escalar en número de tenants, un solo esquema que mantener. | El aislamiento depende de que cada consulta, migración y proceso batch respete la política; un error de código puede filtrar datos entre tenants. Requiere disciplina y pruebas automatizadas de aislamiento. |
| Esquema por tenant en una base compartida | Mismo motor de base de datos, un esquema (namespace) distinto por tenant. | Aislamiento más fuerte que RLS a nivel de motor; permite migraciones o restauraciones por tenant. | Escalar a cientos de tenants complica migraciones (aplicar el mismo cambio N veces) y el pooling de conexiones. |
| Base de datos dedicada por tenant | Cada tenant tiene su propia instancia o base de datos física. | Aislamiento más fuerte disponible; facilita cumplir residencia de datos y despliegues on-premise por cliente. | Mayor coste operativo y de infraestructura; versión y parches deben replicarse por tenant; complica consultas cross-tenant para soporte interno (si llegaran a necesitarse). |
| Modelo híbrido por sensibilidad | Datos de bajo riesgo en almacenamiento compartido; datos sensibles (credenciales, payloads de origen) en almacenamiento dedicado o cifrado por tenant. | Ajusta coste a riesgo real; compatible con clientes que exigen residencia estricta solo para ciertos datos. | Añade complejidad de diseño: dos rutas de datos, dos modelos de backup y recuperación. |

### Consideraciones transversales, no solo de base de datos

El aislamiento no se resuelve solo en la capa de datos. `MULTITENANCY.md` ya lista identidades, colas, cachés, observabilidad, exportaciones y credenciales de conectores como superficies que deben aislarse. Cualquier estrategia elegida debe demostrar cómo el contexto de tenant viaja de forma obligatoria y verificable a través de:

- autenticación y autorización de usuarios humanos,
- procesamiento asíncrono y colas de sincronización (`SyncRun`),
- cachés e índices de búsqueda,
- herramientas MCP invocadas por agentes,
- soporte operativo de Coresolutions (acceso de un ingeniero a datos de un cliente).

### Preguntas que una prueba técnica debería responder

1. ¿Cuántos tenants se esperan en el primer año, y con qué variabilidad de tamaño? Esto determina si una base por tenant es sostenible operativamente.
2. ¿Algún cliente exige residencia de datos o aislamiento físico que descarte por completo el modelo compartido?
3. ¿Qué motor de base de datos candidato soporta RLS u otro control equivalente de forma madura, y qué evidencia existe de que se puede auditar (pruebas automatizadas que intenten leer datos de otro tenant y deban fallar)?
4. ¿Cómo se propaga el `tenant_id` desde una consulta en lenguaje natural o una llamada MCP hasta la capa de datos, sin depender de que cada nueva funcionalidad lo recuerde manualmente?

## Parte 2 — Arquitectura del Collector

El Collector es el componente que corre dentro (o cerca) de la red del cliente para leer fuentes como vCenter o iLO. Es la pieza de software real más cercana a producción que el proyecto necesitará, y la documentación actual no compara alternativas.

| Opción | Descripción | Ventajas | Riesgos / costes |
| --- | --- | --- | --- |
| Agente propio, propósito específico | Software construido a medida que solo sabe leer las fuentes del modelo canónico y transmitir observaciones saneadas. | Control total sobre qué datos salen, formato, seguridad y footprint; más fácil de auditar frente al modelo de amenazas. | Hay que construir y mantener instalación, actualización, telemetría de salud y compatibilidad por versión de fuente desde cero. |
| Reutilizar un agente de recolección existente (p. ej. Telegraf, Fluent Bit u otro colector de métricas/logs de propósito general) como transporte, con lógica propia de normalización aguas arriba | Aprovecha un runtime maduro para conectividad, buffering, reintentos y salida cifrada; reduce trabajo de infraestructura del agente. | El agente genérico no entiende el modelo canónico (Asset/Observation/Relationship); requiere una capa de traducción; puede traer capacidades (escritura, ejecución de comandos) que exceden el principio de mínimo privilegio y deben desactivarse explícitamente. |
| Sin Collector local: llamadas directas desde la plataforma central hacia las fuentes del cliente | La plataforma multi-tenant se conecta salientemente o el cliente abre una entrada hacia sus APIs de gestión. | Elimina la necesidad de instalar y mantener software en el cliente. | Exige abrir una interfaz de administración hacia el exterior o credenciales alcanzables desde fuera de la red del cliente — contradice el principio de "no exponer una interfaz de administración al exterior" ya declarado en `TECHNICAL-FEASIBILITY-INITIAL.md`. Poco viable para la mayoría de clientes empresariales. |
| Modelo híbrido por tamaño de cliente | Collector local para clientes que lo exigen por política de seguridad; conexión directa autorizada y limitada para clientes pequeños que lo permitan. | Ajusta esfuerzo de despliegue a la exigencia real del cliente. | Duplica rutas de ingesta, pruebas y superficie de mantenimiento; complica el modelo de amenazas único. |

### Dimensiones operativas que cualquier opción debe resolver

- **Conectividad de salida:** ¿el Collector inicia conexión saliente hacia la plataforma (recomendado, evita abrir puertos entrantes) o al revés?
- **Proxies y certificados corporativos:** manejo de proxy HTTP/HTTPS y de certificados self-signed internos, mencionado como pregunta abierta en `ARCHITECTURE.md` (dominio de Ingesta) y en RB-004 del backlog.
- **Actualización y versión:** cómo se distribuyen nuevas versiones del Collector sin intervención manual constante del cliente.
- **Resiliencia offline:** comportamiento si pierde conectividad con la plataforma central (bufferizar, descartar, reintentar) y por cuánto tiempo.
- **Footprint y consumo de recursos:** aceptable para instalarse en infraestructura ya cargada del cliente.
- **Rotación y almacenamiento de credenciales locales:** dónde y cómo guarda las credenciales de solo lectura hacia vCenter/iLO mientras corre.

### Relación con el modelo de amenazas existente

`THREAT-MODEL-MVP.md` ya identifica al Collector como superficie de riesgo. Este documento no repite ese análisis; lo complementa señalando que **la elección de arquitectura del Collector** (construir vs. adaptar un agente existente vs. prescindir de él) es anterior y determina qué controles del modelo de amenazas son aplicables.

## Qué no decide este documento

- No selecciona motor de base de datos, proveedor cloud, lenguaje ni framework.
- No elige si el Collector es agente propio o adaptación de una herramienta existente.
- No compromete un cronograma ni asigna la investigación a una persona.
- No sustituye la necesidad de una prueba técnica autorizada (RB-004, RB-005) para validar cualquier opción contra un entorno real.

## Siguiente paso recomendado

Registrar estas dos preguntas como ítems explícitos de máxima prioridad en `research/RESEARCH-BACKLOG.md` (P0, antes o junto con RB-004/RB-005), porque bloquean tanto el piloto técnico como cualquier decisión posterior de MVP. Una vez exista evidencia de un entorno de piloto real, cada estrategia debe probarse, no solo documentarse, y cerrar con un ADR en `development/DECISIONS.md`.
