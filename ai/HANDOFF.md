# Handoff de Proyecto Loreto

> Actualizar al finalizar cada sesión significativa. Última actualización: 2026-09-04 (sesión 2).

## Estado actual

**HYPOTHESIS / fase de descubrimiento.** La documentación inicial y una investigación de escritorio están creadas. No existe código de aplicación ni decisiones de stack, nube, modelo de datos, integraciones, modelo comercial o MVP.

## Último trabajo realizado

- Se creó la estructura de fuente de verdad para producto, arquitectura, proceso y continuidad entre agentes.
- Se registró el ADR-0001 sobre usar este repositorio como fuente de verdad.
- Se capturó la hipótesis de producto sin cerrar decisiones técnicas o comerciales.
- Se propuso, sin aprobar, un MVP de solo lectura con vSphere y una fuente de gestión de servidores; se añadieron límites, competencia y criterios de seguridad a investigar.
- Se preparó el plan ejecutable de prueba de factibilidad, incluido el registro de evidencia no sensible y cierre seguro.
- Se definieron, como hipótesis, las vistas mínimas del MVP y el modelo canónico de tenant, fuentes, activos, observaciones y relaciones.
- Se documentó el modelo de amenazas del piloto con pruebas de aislamiento, privilegio mínimo, secretos, Collector y calidad de datos.
- Se consolidó el paquete de preparación en una carta de piloto con hipótesis, roles, puertas y criterios de decisión.
- Se ordenó la investigación pendiente por dependencias del piloto, validación de MVP y futuras integraciones.
- Se recopiló investigación de escritorio para Veeam, Check Point, IBM Storage, Cisco, Aruba y Red Hat; ninguna integración fue seleccionada.
- Se creó una guia PDF operativa para que infraestructura prepare el laboratorio interno de Loreto.
- Se identificaron dos decisiones estructurales pendientes que condicionan el resto del piloto (estrategia de aislamiento multi-tenant y arquitectura del Collector) y se documentó una comparación de opciones de escritorio para ambas, sin cerrar ninguna decisión. Se añadieron RB-007 y RB-008 al backlog de investigación como P0.
- Se creó `research/pilot-scripts/readonly_pilot_check.py`, un script de solo lectura para ejecutar PT-02/PT-03/PT-04/PT-06 del plan de piloto contra vSphere y XClarity, pensado para correr dentro de la red del responsable del entorno, no desde una sesión remota.
- El responsable del proyecto confirmó tener infraestructura propia (vSphere y XClarity/iLO) para pruebas y pidió avanzar hacia una PoC técnica de flujo completo para evaluar viabilidad de producto.
- Se registró `ADR-0002` (ACCEPTED): autoriza una PoC acotada (Collector + normalización mínima al modelo canónico + reporte simple) contra infraestructura propia del responsable del proyecto, sin comprometer stack, nube ni datos de cliente real.
- Se construyó la PoC en `poc/collector/`: normaliza lecturas de vSphere y XClarity al modelo canónico mínimo (Tenant/Source/SyncRun/Asset/Observation/Relationship), con alias no reversibles y lista blanca de campos permitidos. No se ejecutó todavía contra el laboratorio real; queda pendiente para el responsable del proyecto, que la corre localmente en su propia red.

## Decisiones recientes

- `ADR-0001` (ACCEPTED): este repositorio es la fuente de verdad de descubrimiento.
- `ADR-0002` (ACCEPTED): autoriza una PoC técnica acotada (Collector, normalización mínima, reporte simple) contra infraestructura propia, sin comprometer producto ni datos de cliente.

## Preguntas abiertas prioritarias

1. ¿Qué entorno de piloto puede proporcionar vSphere y Lenovo XClarity Administrator o HPE iLO/Redfish con permisos de solo lectura?
2. ¿Qué campos, versiones y relaciones son realmente accesibles en ese entorno?
3. ¿Qué requisitos de seguridad, residencia y despliegue aplican a dicho piloto?
4. ¿Qué evidencia confirma una diferenciación y modelo comercial viables?
5. ¿Qué estrategia de aislamiento multi-tenant (base compartida con controles lógicos, esquema por tenant, base por tenant o híbrida) es sostenible para el número y tipo de tenants esperados?
6. ¿El Collector debe ser un agente propio, una adaptación de un colector existente, o puede evitarse con conexión directa autorizada? ¿Qué patrón de conectividad saliente exige la red típica de un cliente?

## Pendientes

- Confirmar un entorno candidato y sus fuentes de gestión disponibles.
- Ejecutar una prueba técnica de solo lectura contra las fuentes seleccionadas.
- Revisar requisitos de seguridad, residencia y despliegue con el responsable del cliente.
- Completar análisis de competencia, costes y modelo comercial con evidencia de mercado.
- Validar contra un entorno real las opciones de aislamiento multi-tenant y de arquitectura del Collector (RB-007, RB-008) antes de comprometer el modelo canónico o iniciar cualquier desarrollo.

## Próximo paso recomendado

Ejecutar `poc/collector/collector.py` en la red del responsable del proyecto contra su vSphere/XClarity propios, revisar el bundle canónico local y el resumen saneado, y traer de vuelta ese resumen (nunca el JSON completo) para evaluar si la normalización y las relaciones observadas tienen sentido. En paralelo, decidir con evidencia las preguntas estructurales de RB-007 y RB-008 usando lo que la PoC muestre sobre conectividad y aislamiento.

## Archivos relevantes

- [Blueprint de producto](../product/PRODUCT-BLUEPRINT.md)
- [Casos de uso](../product/USE-CASES.md)
- [Especificación de MVP](../product/MVP-SPECIFICATION.md)
- [Arquitectura conceptual](../architecture/ARCHITECTURE.md)
- [Modelo canónico](../architecture/CANONICAL-DATA-MODEL.md)
- [Modelo de amenazas](../architecture/THREAT-MODEL-MVP.md)
- [Carta de piloto](../development/PILOT-CHARTER.md)
- [Guia de laboratorio (PDF)](../output/pdf/guia-laboratorio-interno-loreto.pdf)
- [Conectores](../architecture/CONNECTORS.md)
- [Seguridad](../architecture/SECURITY.md)
- [Registro de decisiones](../development/DECISIONS.md)
- [Roadmap](../development/ROADMAP.md)
- [Investigación técnica](../research/TECHNICAL-FEASIBILITY-INITIAL.md)
- [Plan de piloto de solo lectura](../research/PILOT-READONLY-PLAN.md)
- [Seguridad y despliegue](../research/SECURITY-DEPLOYMENT-INITIAL.md)
- [Backlog de investigación](../research/RESEARCH-BACKLOG.md)
- [Investigación de integraciones posteriores](../research/CONNECTOR-EXPANSION-DESK-RESEARCH.md)
- [Opciones de multi-tenancy y Collector](../research/MULTITENANCY-COLLECTOR-OPTIONS.md)
- [PoC del Collector](../poc/README.md)
