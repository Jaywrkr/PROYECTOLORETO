# Product Blueprint — Proyecto Loreto

> **Madurez: borrador de descubrimiento.** Este documento captura la hipótesis inicial y debe evolucionar con evidencia.

## Resumen

**HYPOTHESIS:** Proyecto Loreto podría ser una capa inteligente sobre la infraestructura tecnológica heterogénea de cada cliente de Coresolutions. Debe complementar —no reemplazar— las consolas y herramientas de administración de fabricantes.

## Problema

**HYPOTHESIS:** Los clientes operan entornos con varios fabricantes y generaciones tecnológicas. Obtener una vista técnica coherente de inventario, estado, dependencias, lifecycle y cambios puede exigir múltiples herramientas y conocimiento especializado.

**TO INVESTIGATE:** Validar el problema con clientes y equipos de Coresolutions: frecuencia, coste, impacto operativo, procesos actuales y alternativas que ya usan.

## Cliente objetivo

**HYPOTHESIS:** Organizaciones con infraestructura empresarial híbrida y heterogénea, administrada por equipos internos, Coresolutions o ambos.

**OPEN QUESTION:** ¿Quién será el comprador, usuario principal y administrador técnico: cliente, mesa de servicios de Coresolutions, o ambos?

## Propuesta de valor

**HYPOTHESIS:** Una visión autorizada y consultable de la infraestructura podría reducir el tiempo para comprender el estado, identificar riesgos de soporte y responder preguntas operativas.

**TO INVESTIGATE:** Definir resultados medibles, diferenciación y disposición a pagar.

## Casos de uso

Ver [USE-CASES.md](USE-CASES.md). Ejemplos por validar: salud mensual de nodos, activos próximos a fin de soporte, problemas actuales, cambios semanales y dependencias de un componente.

## Arquitectura conceptual

**HYPOTHESIS:** Conectores podrían obtener información mediante APIs, SNMP, logs, herramientas existentes u otros mecanismos. Un Collector desplegado en la infraestructura del cliente podría comunicarse de forma segura con una plataforma central multi-tenant.

Ver [ARCHITECTURE.md](../architecture/ARCHITECTURE.md), [CONNECTORS.md](../architecture/CONNECTORS.md) y [MULTITENANCY.md](../architecture/MULTITENANCY.md).

## Integraciones

**CONFIRMED (contexto):** Coresolutions trabaja con tecnologías como IBM, Lenovo, HPE/Aruba, VMware, Veeam, Check Point y Red Hat; los entornos de clientes también pueden incluir otros fabricantes, como Dell y Cisco.

**TO INVESTIGATE:** Capacidades de acceso, límites de licencia, autenticación, versionado, cobertura y soporte por tecnología. No hay integración seleccionada.

## Seguridad

**CONFIRMED (requisito):** Cliente A nunca debe acceder a información del Cliente B.

**HYPOTHESIS:** Podrían requerirse instalaciones completamente on-premise para clientes con requisitos regulatorios elevados.

Ver [SECURITY.md](../architecture/SECURITY.md).

## Competencia

**TO INVESTIGATE:** Mapear herramientas de observabilidad, CMDB, ITOM, gestión de infraestructura, descubrimiento y asistentes de IA; comparar cobertura, deployment, seguridad, precios y vacíos.

## Diferenciación

**HYPOTHESIS:** La posible diferenciación podría surgir de combinar conocimiento de infraestructura multi-fabricante, contexto de dependencias, acceso seguro y consultas en lenguaje natural. Aún no está validada.

## Modelo comercial

**TO INVESTIGATE:** Elegir entre suscripción por activo/sitio/tenant, servicio gestionado, licencia on-premise, implementación y soporte. Ver [BUSINESS-MODEL.md](BUSINESS-MODEL.md).

## MVP

**HYPOTHESIS:** El MVP debería resolver un caso de alto valor con una cobertura de tecnologías limitada y controles de aislamiento desde el inicio.

**OPEN QUESTION:** ¿Cuál caso de uso, segmento de cliente y conjunto de integraciones ofrece la validación más rápida?

## Riesgos

- **TO INVESTIGATE:** Heterogeneidad, APIs incompletas, límites de licenciamiento y compatibilidad por versión.
- **TO INVESTIGATE:** Exposición de credenciales, datos sensibles y rutas de administración.
- **TO INVESTIGATE:** Exactitud, actualidad y trazabilidad de datos recopilados.
- **TO INVESTIGATE:** Coste de operar conectores, plataforma central y despliegues on-premise.
- **TO INVESTIGATE:** Diferenciación y disposición a pagar frente a herramientas existentes.

## Preguntas abiertas

1. ¿Qué problema prioritario se validará primero y con qué clientes?
2. ¿Qué datos mínimos hacen útil el inventario y qué fuente es confiable para cada dato?
3. ¿Qué modelos de despliegue y residencia de datos son exigidos por los clientes objetivo?
4. ¿Qué capacidades de MCP se pueden exponer de forma segura y con qué autorización?
5. ¿Qué límites separan observación, recomendación y ejecución automatizada?

## Criterios para determinar si vale la pena construir

La hipótesis solo avanzará si la investigación demuestra evidencia suficiente de:

- un problema recurrente, costoso y reconocido por el cliente objetivo;
- acceso técnico sostenible a datos de una primera combinación de tecnologías;
- aislamiento, seguridad y modelo de despliegue compatibles con los requisitos de clientes;
- una propuesta diferenciada y comercialmente viable;
- un MVP acotado que pueda medir valor antes de ampliar conectores o automatización.
