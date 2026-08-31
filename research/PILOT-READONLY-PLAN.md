# Plan de prueba de factibilidad — solo lectura

> **Estado: TO INVESTIGATE.** Preparación documental completada el 2026-08-29. La ejecución exige un entorno autorizado y no habilita desarrollo de producto.

## Objetivo

Determinar si un primer piloto puede obtener datos técnicos útiles de forma segura, aislada y trazable desde:

1. un vCenter/vSphere autorizado; y
2. una fuente de gestión de servidores: Lenovo XClarity Administrator **o** HPE iLO/Redfish.

El resultado buscado es evidencia de factibilidad, no un conector de producción ni una promesa de MVP.

## Límites obligatorios

- Solo lectura: no crear, modificar, borrar, reiniciar ni reconfigurar recursos.
- Un único tenant de prueba; no mezclar datos con otros clientes ni datos de producción ajenos al alcance aprobado.
- No exponer interfaces administrativas hacia Internet.
- No incluir secretos, direcciones IP, series, nombres de hosts ni capturas sensibles en este repositorio.
- No activar MCP, IA generativa, alertas ni automatizaciones durante la prueba.

## Información que debe proporcionar el responsable del entorno

| Elemento | Requerido para | Registro permitido en el repositorio |
| --- | --- | --- |
| Aprobación escrita del alcance y ventana de prueba | Autorización | Fecha, responsable y referencia no sensible |
| Tenant y entorno de prueba identificados | Aislamiento | Alias no sensible |
| Versión de vCenter y fuente de servidores | Compatibilidad | Producto y versión, sin endpoint |
| Cuenta dedicada de solo lectura por fuente | Acceso | Confirmación de creación; nunca usuario, contraseña ni token |
| Ruta de red, proxy y certificados requeridos | Conectividad | Resultado y restricciones, sin detalles de red sensibles |
| Política de retención y eliminación | Manejo de datos | Período y responsable |

## Permisos y preparación

### vSphere

**TO INVESTIGATE:** El administrador debe asignar una cuenta dedicada con el rol mínimo de lectura aplicable al alcance de inventario. Antes de cualquier consulta, documentar el rol efectivo y confirmar que no incluye acciones de escritura.

La API REST de vSphere usa autenticación por sesión; la referencia del fabricante debe contrastarse con la versión real del entorno. Fuente: [vSphere Automation API](https://developer.broadcom.com/xapis/vsphere-automation-api/latest/).

### Fuente de servidores

Elegir una única ruta:

- **Lenovo:** cuenta de solo lectura en XClarity Administrator, con acceso únicamente a los dispositivos del piloto. Validar versión, autenticación HTTPS y recursos accesibles. Fuente: [XClarity REST APIs](https://pubs.lenovo.com/lxca_scripting/rest_apis).
- **HPE:** cuenta de solo lectura en iLO/Redfish de los servidores incluidos. Validar generación, firmware y recursos soportados; los equipos antiguos pueden no ofrecer la misma superficie. Fuente: [HPE iLO RESTful API](https://developer.hpe.com/platform/ilo-restful-api/home/).

## Datos mínimos a intentar leer

| Dominio | Campo / relación candidata | Resultado esperado |
| --- | --- | --- |
| Identidad de fuente | Tipo, versión y hora de consulta | Procedencia y compatibilidad registradas |
| vSphere | Datacenter, cluster, host, VM y datastore | Inventario de virtualización normalizable |
| vSphere | Host–VM, cluster–host y VM–datastore cuando la fuente los exponga | Relaciones observadas, no inferidas |
| Hardware | Fabricante, modelo, serial o identificador protegido, firmware y estado | Inventario y salud de servidores del alcance |
| Calidad | Campos ausentes, errores y antigüedad | Limitaciones visibles, no ocultas |

Los identificadores sensibles deben sustituirse por alias o hashes no reversibles en cualquier evidencia que llegue al repositorio.

## Casos de prueba y evidencia

| ID | Prueba | Éxito | Evidencia no sensible a registrar |
| --- | --- | --- | --- |
| PT-01 | Verificar autorización y límites de cuenta | La cuenta no puede ejecutar cambios | Rol/privilegio revisado y fecha |
| PT-02 | Conectar a vSphere y leer inventario mínimo | Datos recuperados sin escritura | Conteos, versión, hora y campos faltantes |
| PT-03 | Leer relaciones vSphere | Relaciones observadas recuperadas y distinguibles | Tipos de relación y conteos |
| PT-04 | Conectar a XClarity o iLO/Redfish | Inventario y salud disponibles para el alcance | Tipo de fuente, versión y campos obtenidos |
| PT-05 | Validar aislamiento | Una identidad fuera del tenant no puede enumerar ni leer datos del piloto | Resultado de prueba negativa, sin credenciales |
| PT-06 | Validar manejo de fallos | Errores de red, permiso o campo faltante no producen reintentos peligrosos ni ocultan el error | Escenario, respuesta y log saneado |
| PT-07 | Cerrar y eliminar datos de prueba | Cuentas revocadas si corresponde y datos eliminados según política | Confirmación, responsable y fecha |

## Registro de ejecución

Completar esta tabla durante el piloto, sin contenido sensible.

| Campo | Valor |
| --- | --- |
| Alias de tenant / entorno | PENDIENTE |
| Responsable que autorizó | PENDIENTE |
| Inicio / fin | PENDIENTE |
| Fuente de virtualización | PENDIENTE |
| Fuente de servidores elegida | PENDIENTE |
| PT-01 a PT-07 | PENDIENTE |
| Hallazgos | PENDIENTE |
| Riesgos / limitaciones | PENDIENTE |
| Decisión recomendada | PENDIENTE |

## Criterios de cierre

La prueba se considera técnicamente prometedora solo si se cumple todo lo siguiente:

1. Las fuentes entregan el inventario mínimo con cuentas de solo lectura.
2. La procedencia, hora de lectura y campos ausentes pueden conservarse junto al dato.
3. Las relaciones esenciales de vSphere se recuperan con claridad suficiente para el caso de uso.
4. El aislamiento del tenant supera una prueba negativa documentada.
5. La conectividad, permisos y retención son operables sin abrir un riesgo no aceptado.
6. Las limitaciones por versión, modelo o fuente quedan explícitas.

Un resultado fallido también es valioso: debe registrarse con evidencia y actualizar la hipótesis de MVP. Cualquier selección de integración o inicio de desarrollo posterior requiere un ADR y autorización explícita.

El análisis de amenazas y las puertas de seguridad que aplican a esta prueba están en [THREAT-MODEL-MVP.md](../architecture/THREAT-MODEL-MVP.md).
