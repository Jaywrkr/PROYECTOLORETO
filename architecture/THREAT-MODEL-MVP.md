# Modelo de amenazas — MVP de solo lectura

> **Estado: TO INVESTIGATE.** Última actualización: 2026-08-30. Este documento identifica riesgos y controles candidatos; no certifica seguridad ni define una arquitectura implementada.

## Alcance

Este modelo cubre el piloto candidato: lectura de vCenter/vSphere y de una única fuente de servidores (Lenovo XClarity Administrator o HPE iLO/Redfish), con posible Collector local y una vista por tenant.

Quedan fuera de alcance actual las acciones de escritura, automatización, alertas proactivas, IA generativa y MCP expuesto. Se mantienen como amenazas futuras para evitar que se incorporen sin revisión.

## Objetivos de protección

1. Evitar que un tenant vea, infiera o modifique datos de otro tenant.
2. Proteger credenciales de fuentes, tokens, certificados y secretos del Collector.
3. Garantizar que el piloto no ejecute cambios sobre infraestructura.
4. Conservar procedencia, hora y calidad de los datos para evitar conclusiones incorrectas.
5. Evitar exposición innecesaria de detalles sensibles de infraestructura.
6. Mantener evidencia auditable de accesos, sincronizaciones, fallos y exportaciones.

## Activos a proteger

| Activo | Sensibilidad / impacto si se compromete |
| --- | --- |
| Contexto de tenant e identidad de usuario | Puede provocar acceso cruzado o suplantación. |
| Credenciales de vCenter, XClarity o iLO/Redfish | Podrían revelar infraestructura o permitir cambios según sus permisos. |
| Certificados, tokens y configuración de Collector | Podrían permitir suplantar una conexión autorizada. |
| Inventario, relaciones y estados técnicos | Puede revelar topología, versiones, capacidad y riesgos operativos. |
| Historial de sincronización y errores | Puede exponer endpoints, nombres, secretos accidentales o patrones de operación. |
| Registros de auditoría | Son evidencia para investigar acceso, cambios de privilegios y fallos. |

## Límites de confianza candidatos

```text
Usuario / soporte autorizado
          │ identidad + autorización
          ▼
Vista o API por tenant ──> datos del tenant / auditoría
          ▲                         ▲
          │ conexión autorizada     │ ingesta validada
          │                         │
Collector local (posible) ──> vCenter / XClarity / iLO-Redfish
                 credenciales de solo lectura
```

Cada flecha representa un límite que exige identidad, autorización, validación de entrada, registro y manejo de fallos. La topología real sigue abierta.

## Escenarios de amenaza y controles candidatos

| ID | Escenario | Impacto | Controles candidatos | Evidencia / prueba requerida |
| --- | --- | --- | --- | --- |
| TM-01 | Una consulta manipula o pierde el contexto de tenant. | Exposición cruzada de datos. | `tenant_id` obligatorio en identidad, consulta, almacenamiento y auditoría; políticas de acceso verificables. | Prueba negativa: identidad A no puede enumerar ni leer activos, relaciones o errores de B. |
| TM-02 | Una cuenta de fuente tiene privilegios de escritura excesivos. | Cambio no autorizado en infraestructura. | Cuenta dedicada, mínimo privilegio, solo lectura, revisión independiente de permisos y revocación. | Inventario de permisos y prueba de que no se permite una operación de cambio. |
| TM-03 | Se filtra un secreto en configuración, log, error o exportación. | Acceso no autorizado a fuentes o plataforma. | Gestor de secretos por definir, saneamiento de logs, prohibición de secretos en repositorio, rotación y acceso mínimo. | Revisión de logs/errores de prueba y búsqueda de secretos antes de conservar evidencia. |
| TM-04 | Un Collector es suplantado, comprometido o usado fuera de su tenant. | Ingesta fraudulenta, filtración o pivot a red del cliente. | Identidad única del Collector, autenticación mutua a evaluar, actualización controlada, egreso restringido y revocación. | Registro de identidad, prueba de revocación y revisión de rutas de red autorizadas. |
| TM-05 | La fuente devuelve datos maliciosos, inesperados o excesivos. | Corrupción de vista, denegación de servicio o exposición de contenido peligroso. | Validación de esquema/tamaño, límites de tasa, saneamiento de campos y errores explícitos. | Casos de entrada incompleta, inválida y sobredimensionada manejados sin perder aislamiento. |
| TM-06 | Datos obsoletos o parciales se presentan como actuales o completos. | Decisiones operativas erróneas. | Procedencia, hora de lectura, estado de calidad y umbrales visibles. | Simular fallo de sincronización y comprobar que la vista marca `STALE`, `PARTIAL` o error. |
| TM-07 | Soporte de Coresolutions obtiene acceso mayor al autorizado. | Acceso indebido a información de cliente. | Delegación explícita, duración limitada a evaluar, auditoría y revisión de privilegios. | Evidencia de que un rol de soporte no accede sin asignación al tenant. |
| TM-08 | Backups, telemetría o logs mezclan tenants. | Filtración indirecta, difícil de detectar. | Aislamiento incluido en diseño de operaciones, exportación, cachés y recuperación. | Revisión de flujos operativos y prueba de exportación/restauración aislada cuando exista plataforma. |
| TM-09 | Una interfaz futura de MCP expone más datos o permisos que la vista humana. | Exfiltración o escalamiento por agentes. | Fuera del MVP; lectura inicial, scopes mínimos, autorización por recurso y auditoría por invocación. | Revisión de amenaza y autorización específica antes de habilitar MCP. |
| TM-10 | El modo on-premise recibe parches, auditoría o soporte insuficientes. | Riesgo operativo y de seguridad sostenido. | Definir ciclo de actualización, responsabilidades, telemetría permitida y soporte antes de ofrecerlo. | Plan de operación y recuperación evaluado para cada modalidad. |

## Controles mínimos para permitir el piloto

Los siguientes controles son **HYPOTHESIS** de puerta de seguridad. La prueba no debe empezar hasta que sean revisados y aceptados por el responsable del entorno:

1. Autorización explícita, tenant y fuentes de alcance definidos.
2. Cuentas de fuente dedicadas, solo lectura, con propietario y revocación disponible.
3. Inventario de datos que se recogerán, ubicación, período de retención y procedimiento de eliminación.
4. Ruta de red, certificados y proxy revisados; sin exposición administrativa entrante no aprobada.
5. Saneamiento de evidencias: no copiar secretos, IPs, nombres de host o payloads completos al repositorio.
6. Registro de accesos y sincronizaciones con contexto de tenant.
7. Prueba negativa de aislamiento incluida en el plan de ejecución.

## Supuestos a validar

- La fuente puede suministrar datos útiles con permisos estrictamente de lectura.
- Es posible distinguir y registrar datos observados de datos derivados.
- El cliente autoriza una ruta de conectividad compatible con su política de seguridad.
- El personal de Coresolutions tiene un modelo de acceso delegado aceptable para el cliente.
- No se requiere un modo on-premise completo para demostrar el primer caso de valor.

Si alguno falla, registrar el resultado en el plan de piloto y actualizar las hipótesis de arquitectura y MVP.

## Fuentes de referencia

Este modelo usa zero trust como principio orientador: la confianza no debe derivarse solo de ubicación de red y la identidad/autorización debe evaluarse para acceder a recursos. No adopta una implementación específica.

- [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST SP 800-207A — control de acceso para aplicaciones cloud-native](https://csrc.nist.gov/pubs/sp/800/207/a/final)

## Próxima revisión

Revisar este modelo después de elegir un entorno de piloto, conocer sus versiones y rutas de red, y antes de conceder cuentas o desplegar un Collector.
