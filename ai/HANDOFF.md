# Handoff de Proyecto Loreto

> Actualizar al finalizar cada sesión significativa. Última actualización: 2026-08-29.

## Estado actual

**HYPOTHESIS / fase de descubrimiento.** La documentación inicial y una investigación de escritorio están creadas. No existe código de aplicación ni decisiones de stack, nube, modelo de datos, integraciones, modelo comercial o MVP.

## Último trabajo realizado

- Se creó la estructura de fuente de verdad para producto, arquitectura, proceso y continuidad entre agentes.
- Se registró el ADR-0001 sobre usar este repositorio como fuente de verdad.
- Se capturó la hipótesis de producto sin cerrar decisiones técnicas o comerciales.
- Se propuso, sin aprobar, un MVP de solo lectura con vSphere y una fuente de gestión de servidores; se añadieron límites, competencia y criterios de seguridad a investigar.
- Se preparó el plan ejecutable de prueba de factibilidad, incluido el registro de evidencia no sensible y cierre seguro.

## Decisiones recientes

- `ADR-0001` (ACCEPTED): este repositorio es la fuente de verdad de descubrimiento.

## Preguntas abiertas prioritarias

1. ¿Qué entorno de piloto puede proporcionar vSphere y Lenovo XClarity Administrator o HPE iLO/Redfish con permisos de solo lectura?
2. ¿Qué campos, versiones y relaciones son realmente accesibles en ese entorno?
3. ¿Qué requisitos de seguridad, residencia y despliegue aplican a dicho piloto?
4. ¿Qué evidencia confirma una diferenciación y modelo comercial viables?

## Pendientes

- Confirmar un entorno candidato y sus fuentes de gestión disponibles.
- Ejecutar una prueba técnica de solo lectura contra las fuentes seleccionadas.
- Revisar requisitos de seguridad, residencia y despliegue con el responsable del cliente.
- Completar análisis de competencia, costes y modelo comercial con evidencia de mercado.

## Próximo paso recomendado

Preparar una prueba de factibilidad de solo lectura, con un entorno vSphere y una fuente de servidores disponible. Definir datos mínimos, permisos, límites de red, criterios de éxito y una forma de borrar los datos de prueba.

## Archivos relevantes

- [Blueprint de producto](../product/PRODUCT-BLUEPRINT.md)
- [Casos de uso](../product/USE-CASES.md)
- [Arquitectura conceptual](../architecture/ARCHITECTURE.md)
- [Conectores](../architecture/CONNECTORS.md)
- [Seguridad](../architecture/SECURITY.md)
- [Registro de decisiones](../development/DECISIONS.md)
- [Roadmap](../development/ROADMAP.md)
- [Investigación técnica](../research/TECHNICAL-FEASIBILITY-INITIAL.md)
- [Plan de piloto de solo lectura](../research/PILOT-READONLY-PLAN.md)
- [Seguridad y despliegue](../research/SECURITY-DEPLOYMENT-INITIAL.md)
