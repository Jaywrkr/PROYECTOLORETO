# Factibilidad técnica inicial y MVP candidato

> **Estado: TO INVESTIGATE.** Investigación de escritorio realizada el 2026-08-29. No sustituye pruebas de compatibilidad, permisos, licencias o rendimiento en un cliente.

## Propósito

Reducir el alcance de investigación sin elegir definitivamente tecnologías ni iniciar desarrollo. La propuesta se enfoca en una fuente transversal de virtualización y una fuente de gestión de servidores.

## MVP candidato — no aprobado

**HYPOTHESIS:** Un piloto podría recopilar en modo solo lectura, por tenant, inventario y estado de:

- vCenter/vSphere: datacenters, clusters, hosts, VMs y datastores disponibles mediante la API autorizada.
- Una fuente de hardware: Lenovo XClarity Administrator **o** HPE iLO/Redfish, elegida por disponibilidad en el entorno de piloto.

La salida mínima sería una vista o reporte de inventario y salud con fuente, hora de actualización y advertencias sobre datos ausentes. La consulta natural, las alertas, el MCP y el grafo completo de dependencias quedan fuera del piloto inicial.

## Evidencia de APIs

| Fuente | Evidencia publicada | Oportunidad para el MVP | Limitación / prueba pendiente |
| --- | --- | --- | --- |
| vSphere Automation API | Broadcom publica referencia REST, autenticación por sesión y operaciones de vCenter, incluidos VMs y datastores. | Base para inventario de virtualización y relaciones visibles desde vCenter. | Confirmar versión de vCenter, privilegios mínimos de solo lectura, campos requeridos, rate limits y cobertura real de relaciones. |
| Lenovo XClarity Administrator | Lenovo documenta REST sobre HTTPS, autenticación y versiones; indica que la documentación actual aplica a 4.3+ y publica referencias para versiones anteriores. | Inventario y configuración de servidores administrados por XClarity. | Verificar si el cliente tiene XClarity, versión, dispositivos administrados y datos de salud/lifecycle que pueden leerse. |
| HPE iLO / Redfish | HPE documenta API REST compatible con Redfish para inventario y monitorización en iLO 5/6 y generaciones indicadas. | Alternativa para inventario y salud de servidores HPE administrables. | Los servidores antiguos pueden tener diferente cobertura; validar generación, firmware, permisos y disponibilidad de iLO. |

### Fuentes consultadas

- [Broadcom — vSphere Automation API](https://developer.broadcom.com/xapis/vsphere-automation-api/latest/)
- [Lenovo — XClarity Administrator REST APIs](https://pubs.lenovo.com/lxca_scripting/rest_apis)
- [HPE — iLO RESTful API](https://developer.hpe.com/platform/ilo-restful-api/home/)
- [HPE — guía de compatibilidad y navegación Redfish](https://developer.hpe.com/blog/getting-started-with-ilo-restful-api-redfish-api-conformance/)

## Prueba de factibilidad propuesta

**TO INVESTIGATE:** Antes de construir un conector, ejecutar una prueba autorizada de lectura con datos minimizados.

| Dimensión | Criterio de éxito candidato |
| --- | --- |
| Acceso | Cuenta dedicada de solo lectura; sin permisos de cambio ni credenciales compartidas. |
| Cobertura | Recuperar el conjunto mínimo de activos previsto y registrar campos no disponibles. |
| Procedencia | Conservar fuente, identificador origen y hora de lectura por registro. |
| Relaciones | Demostrar al menos relaciones vSphere visibles y distinguir relaciones observadas de inferidas. |
| Operación | Documentar red, proxy, certificados, frecuencia segura, consumo y manejo de fallos. |
| Seguridad | No exponer una interfaz de administración al exterior; revocar la cuenta y borrar datos de prueba al cerrar. |

## Exclusiones deliberadas

- Escritura, remediación o automatización de infraestructura.
- Descubrimiento de red amplio con credenciales privilegiadas.
- Garantía de soporte para todos los fabricantes, modelos o versiones.
- Compromiso de exponer MCP durante el piloto.

## Decisión que podría seguir

Solo después de una prueba satisfactoria se podrá proponer un ADR para seleccionar la primera integración y el alcance preciso de MVP.
