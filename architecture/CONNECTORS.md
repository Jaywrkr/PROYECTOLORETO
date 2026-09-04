# Conectores y Collector

> **Estado: HYPOTHESIS.** No hay conectores ni mecanismos seleccionados.

## Hipótesis de adquisición

La información podría obtenerse mediante APIs de fabricante, SNMP, logs, herramientas existentes u otros mecanismos autorizados. Un Collector dentro del entorno del cliente podría consolidar o transmitir datos de manera segura hacia una plataforma central.

**TO INVESTIGATE:** La forma concreta del Collector (agente propio, adaptación de un colector existente o conexión directa sin agente local) no está decidida. Una comparación de opciones y sus riesgos operativos está en [MULTITENANCY-COLLECTOR-OPTIONS.md](../research/MULTITENANCY-COLLECTOR-OPTIONS.md).

## Matriz inicial de investigación

| Tecnología / familia | Fuente potencial | Datos a evaluar | Estado |
| --- | --- | --- | --- |
| IBM | API, herramientas existentes, logs | Inventario, storage, estado, lifecycle | TO INVESTIGATE |
| Lenovo | API, gestión de hardware, logs | Inventario, firmware, salud | TO INVESTIGATE |
| HPE / Aruba | API, SNMP, gestión existente | Servidores, red, firmware, alertas | TO INVESTIGATE |
| VMware | API, eventos, configuración | Compute, relaciones, capacidad, cambios | TO INVESTIGATE |
| Veeam | API, reportes, eventos | Backups, jobs, alertas, capacidad | TO INVESTIGATE |
| Check Point | API, logs, gestión existente | Estado, políticas, alertas | TO INVESTIGATE |
| Red Hat | API, gestión existente, logs | Sistemas, plataformas y estado | TO INVESTIGATE |
| Dell / Cisco / otros | API, SNMP, logs | Cobertura mínima y prioridad | TO INVESTIGATE |

## Criterios de evaluación

- Autenticación, permisos mínimos y rotación de credenciales.
- Versiones soportadas, estabilidad y límites de la interfaz.
- Campos disponibles, actualización, procedencia y calidad de datos.
- Red, firewall, proxy, consumo de recursos y resiliencia offline.
- Licencias, términos de uso, coste y derecho de redistribución de datos.
- Estrategia de mantenimiento y pruebas contra versiones de fabricante.

## Preguntas abiertas

1. ¿Qué conector ofrece el caso de uso de MVP más viable?
2. ¿Cuándo basta con conectarse a una herramienta de gestión existente y cuándo es necesario acceso directo?
3. ¿Qué datos nunca deben salir del entorno del cliente?

## Orden de investigación candidato

**HYPOTHESIS:** Priorizar vSphere como fuente transversal de virtualización y, como segunda fuente, Lenovo XClarity Administrator o HPE iLO/Redfish. Esta propuesta no selecciona un fabricante; busca limitar el primer piloto a una fuente de virtualización y una de hardware con API documentada.

La evidencia de escritorio, la matriz de pruebas y sus límites se mantienen en [TECHNICAL-FEASIBILITY-INITIAL.md](../research/TECHNICAL-FEASIBILITY-INITIAL.md).

La investigación de familias posteriores al piloto está en [CONNECTOR-EXPANSION-DESK-RESEARCH.md](../research/CONNECTOR-EXPANSION-DESK-RESEARCH.md).
