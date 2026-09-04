# Backlog de investigación

> **Estado: TO INVESTIGATE.** Última actualización: 2026-09-04. El orden refleja dependencias para validar el piloto; no es una decisión de roadmap comercial ni compromiso de construir cada integración.

## Cómo usar este backlog

- Cada ítem debe terminar con evidencia, fecha, fuentes y un cambio documentado de estado.
- Si un ítem cambia alcance, seguridad, arquitectura o inversión, registrar un ADR.
- `P0` desbloquea la prueba de factibilidad; `P1` prepara la siguiente decisión; `P2` amplía la evaluación tras el piloto.
- No iniciar desarrollo de conectores por completar un ítem de investigación.

## P0 — Preparar y ejecutar el piloto

| ID | Investigación | Resultado esperado | Dependencia |
| --- | --- | --- | --- |
| RB-001 | Seleccionar tenant, entorno y ventana autorizados | Alcance aprobado y responsable identificado | Patrocinador y cliente |
| RB-002 | Confirmar versiones y acceso de vCenter | Matriz de campos, permisos, relaciones y límites reales | RB-001 |
| RB-003 | Elegir XClarity o iLO/Redfish disponible | Fuente de servidores y versión confirmadas | RB-001 |
| RB-004 | Revisar red, proxy, certificados y salida de Collector | Patrón de conectividad autorizado o bloqueo documentado | RB-001 |
| RB-005 | Revisar privilegios y manejo de secretos | Cuentas solo lectura, propietario, revocación y saneamiento de evidencia | RB-002, RB-003 |
| RB-007 | Evaluar estrategia de aislamiento multi-tenant (base compartida con RLS, esquema por tenant, base por tenant o híbrida) contra el entorno de piloto | Estrategia candidata con evidencia de aislamiento verificable, o bloqueo documentado | RB-001 |
| RB-008 | Definir arquitectura candidata del Collector (agente propio, adaptación de un colector existente, o conexión directa) y su patrón de conectividad saliente | Decisión candidata de forma del Collector, validada contra red/proxy/certificados del piloto | RB-001, RB-004 |
| RB-006 | Ejecutar PT-01 a PT-07 | Evidencia de cobertura, calidad, aislamiento y cierre | RB-002 a RB-005, RB-007, RB-008 |

## P1 — Decidir alcance viable del MVP

| ID | Investigación | Resultado esperado | Documento afectado |
| --- | --- | --- | --- |
| RB-101 | Revisar resultados del piloto contra la especificación funcional | Campos y vistas que continúan, cambian o se excluyen | MVP-SPECIFICATION.md |
| RB-102 | Validar consolidación de activos entre vSphere y fuente de hardware | Regla de identidad o decisión de mantener activos separados | CANONICAL-DATA-MODEL.md |
| RB-103 | Estimar frecuencia de sincronización, volumen y fallos | Límites operativos candidatos, sin asumir tecnología | ARCHITECTURE.md |
| RB-104 | Revisar modelo de despliegue central, híbrido y on-premise | Restricciones de cliente, coste y riesgos comparables | SECURITY-DEPLOYMENT-INITIAL.md |
| RB-105 | Revisar riesgos abiertos con seguridad | Aceptación, mitigación o bloqueo de cada amenaza relevante | THREAT-MODEL-MVP.md |
| RB-106 | Registrar decisión `GO`, `ITERATE` o `NO-GO` | ADR posterior al piloto | DECISIONS.md |

## P2 — Ampliar la investigación de integraciones

| ID | Área | Preguntas de investigación |
| --- | --- | --- |
| RB-201 | Veeam | ¿Qué inventario, jobs, alertas, capacidad y estado pueden leerse de forma soportada? |
| RB-202 | Check Point | ¿Qué datos de estado, política y alertas se pueden consultar con privilegio mínimo? |
| RB-203 | IBM storage | ¿Qué APIs/herramientas exponen inventario, capacidad, firmware, eventos y relaciones? |
| RB-204 | Cisco / Aruba | ¿Qué cobertura práctica ofrecen APIs, SNMP y herramientas de gestión para red y relaciones? |
| RB-205 | Red Hat | ¿Qué componentes y fuentes se priorizan: sistema operativo, virtualización, automatización u otras? |
| RB-206 | Lifecycle | ¿Qué fuente, licencia, exactitud y derecho de uso existen para soporte y fin de vida? |

La prioridad entre estos ítems debe decidirse con evidencia de clientes, potencial comercial y esfuerzo técnico. No hay orden de implementación establecido.

## P2 — Viabilidad de producto y operación

| ID | Investigación | Preguntas de decisión |
| --- | --- | --- |
| RB-301 | Competencia y alternativa actual | ¿Qué problema permanece sin resolver frente a ITOM, CMDB y observabilidad existentes? |
| RB-302 | Coste de servicio | ¿Qué costes variables introducen Collector, integración, almacenamiento, IA, soporte y on-premise? |
| RB-303 | Modelo comercial | ¿Qué unidad de valor y empaquetamiento corresponde al resultado demostrado? |
| RB-304 | Equipo y soporte | ¿Qué capacidades se necesitan para mantener conectores y atender incidentes? |
| RB-305 | MCP | ¿Qué caso de uso, cliente, autorización y auditoría justifican exponer herramientas a agentes? |

## Definición de terminado para investigación

Un ítem queda `COMPLETED` solo cuando contiene: pregunta respondida o limitación explícita, evidencia con fecha y fuente, impacto sobre los documentos relevantes, riesgos remanentes y siguiente acción. Si la respuesta descarta una opción, usar `REJECTED` y conservar la razón.

## Enlaces

- [Carta de piloto](../development/PILOT-CHARTER.md)
- [Plan de piloto](PILOT-READONLY-PLAN.md)
- [Factibilidad técnica inicial](TECHNICAL-FEASIBILITY-INITIAL.md)
- [Opciones de multi-tenancy y Collector](MULTITENANCY-COLLECTOR-OPTIONS.md)
- [Decisiones](../development/DECISIONS.md)
