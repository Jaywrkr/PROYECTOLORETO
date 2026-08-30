# Investigación de escritorio — expansión de conectores

> **Estado: TO INVESTIGATE.** Consultado el 2026-08-30. Esta investigación identifica superficies de integración documentadas; no valida permisos, licencias, versiones ni cobertura en entornos de clientes.

## Propósito

Preparar una evaluación posterior al piloto sin alterar el alcance actual. Ninguna familia descrita aquí se selecciona para el MVP de solo lectura.

## Hallazgos iniciales

| Familia | Superficie documentada | Valor potencial | Limitación o riesgo que debe validarse |
| --- | --- | --- | --- |
| Veeam Backup & Replication | REST API sobre HTTPS, documentada con OpenAPI; expone entidades y operaciones. | Inventario de backups, jobs, repositorios, sesiones y señales de protección podrían enriquecer la vista operativa. | La API también permite operaciones que cambian recursos; se requiere un rol y una lista de endpoints estrictamente de lectura. Validar versión, permisos y semántica de estado. |
| Check Point Management | API de gestión con referencias por versión, sesiones y comandos de consulta. | Objetos gestionados, estado y contexto de política podrían aportar información de seguridad/red. | La misma API permite cambios y publicación de sesiones. Validar cuenta de solo lectura, dominio/MDS, alcance, campos sensibles y prohibición de operaciones de cambio. |
| IBM Storage Virtualize / FlashSystem | REST sobre HTTPS, autenticación por token y comandos de listado; documentación indica límites de tasa. | Inventario de storage, capacidad, firmware, eventos y rendimiento podrían aportar relaciones de almacenamiento. | La interfaz usa `POST` incluso para comandos de lectura y acepta comandos de cambio. Requiere allowlist explícita de comandos `ls*`, manejo estricto de tokens y validación de límites. |
| Cisco Catalyst Center | API de inventario de dispositivos y campos de dispositivo/red. | Inventario y atributos de red; posible base para relaciones físicas/lógicas. | Confirmar producto y versión que tenga el cliente, API habilitada, permisos, topología disponible y datos sensibles. |
| HPE Aruba Networking Central | REST API y guía para listar dispositivos/inventario. | Inventario y estado de dispositivos administrados por Central. | Confirmar si el cliente usa Central, modelo de autorización, cobertura on-premise y relaciones de red disponibles. |
| Red Hat Ansible Automation Platform | API de controller y endpoints de hosts/facts; cambios de gateway/versiones documentados. | Puede aportar contexto de automatización e inventario conocido por AAP. | No se asume que AAP sea fuente autoritativa de infraestructura. Validar versión, inventarios gestionados, sensibilidad de facts y valor frente a otras fuentes. |

## Implicaciones transversales

1. **Solo lectura no equivale necesariamente a `GET`.** IBM Storage Virtualize documenta operaciones de lectura mediante `POST`; Veeam y Check Point tienen APIs que también incluyen acciones de cambio. La seguridad debe permitir por operación/rol, no inferirse del método HTTP.
2. **La versión determina la cobertura.** Todas las fuentes deben registrar producto, versión y revisión de API antes de prometer campos o relaciones.
3. **Las fuentes de gestión no son neutras.** Pueden contener secretos, políticas, configuraciones y objetos sensibles. El inventario de campos permitido debe definirse antes de ingerir datos.
4. **Una fuente adicional no debe ampliar el modelo sin evidencia.** Los tipos de activo y relación nuevos deben pasar por el modelo canónico y una decisión de alcance.

## Orden de evaluación propuesto

**HYPOTHESIS:** Después de validar vSphere + fuente de hardware, estudiar Veeam como siguiente candidato por su relación con preguntas operativas de protección y estado. Considerar IBM storage, Check Point, Cisco/Aruba y Red Hat según presencia en los entornos objetivo y evidencia de valor.

Este orden no es una selección de producto ni una prioridad comercial definitiva.

## Prueba de factibilidad mínima por familia

| Dimensión | Pregunta que debe responder cada prueba |
| --- | --- |
| Acceso | ¿Existe una cuenta dedicada con privilegio mínimo y revocación? |
| Lectura | ¿Qué endpoints/comandos exactos se permiten sin efectos secundarios? |
| Cobertura | ¿Qué activos, estados, versiones y relaciones se pueden recuperar? |
| Seguridad | ¿Qué secretos, políticas, logs o identificadores deben excluirse o sanearse? |
| Operación | ¿Qué límites de tasa, tiempo de sesión, red y mantenimiento aplican? |
| Modelo | ¿Qué entidad o relación nueva justifica incorporar y con qué procedencia? |

## Fuentes consultadas

- [Veeam Backup & Replication REST API v13](https://helpcenter.veeam.com/references/vbr/13/rest)
- [Veeam — Backups endpoint and roles](https://helpcenter.veeam.com/references/vbr/13/rest/1.3-rev2/tag/Backups/index.html)
- [Check Point Management API Reference](https://sc1.checkpoint.com/documents/latest/APIs/)
- [Check Point — Managing Security through API](https://sc1.checkpoint.com/documents/R82/WebAdminGuides/EN/CP_R82_CLI_ReferenceGuide/Content/Topics-CLIG/SPROVG/Managing-Security-through-API.htm)
- [IBM Storage Virtualize RESTful API](https://www.ibm.com/docs/en/flashsystem-9x00/9.1.3?topic=interface-storage-virtualize-restful-api)
- [Cisco Catalyst Center API quick start](https://developer.cisco.com/docs/dna-center/api-quick-start/)
- [HPE Aruba Networking Central — Making API calls](https://developer.arubanetworks.com/new-central/docs/making-api-calls)
- [Red Hat Ansible Automation Platform controller API](https://developers.redhat.com/api-catalog/api/ansible-automation-controller)

## Cambios necesarios antes de seleccionar una integración

Para cualquier familia, completar el ítem correspondiente del [backlog de investigación](RESEARCH-BACKLOG.md), actualizar [CONNECTORS.md](../architecture/CONNECTORS.md), revisar el [modelo de amenazas](../architecture/THREAT-MODEL-MVP.md) y proponer un ADR si cambia el alcance del MVP.
