# Seguridad y despliegue inicial

> **Estado: TO INVESTIGATE.** Investigación inicial realizada el 2026-08-29. No es un diseño aprobado ni una certificación de cumplimiento.

## Objetivo de seguridad del piloto

Probar lectura de infraestructura sin permitir cruce de tenants, escritura sobre fuentes ni acceso administrativo entrante no justificado.

## Principios candidatos

- **HYPOTHESIS:** Identidad distinta para cada persona, servicio, Collector y tenant; sin confianza implícita basada únicamente en red.
- **HYPOTHESIS:** Credenciales de origen con privilegio mínimo y solo lectura durante el piloto.
- **HYPOTHESIS:** Comunicación iniciada desde el entorno del cliente hacia fuera, si el modelo central se valida; no se asume una apertura de entrada.
- **HYPOTHESIS:** Cada dato, consulta y exportación debe llevar contexto de tenant y quedar sujeto a autorización y auditoría.
- **HYPOTHESIS:** El MCP futuro empezará con herramientas de lectura, scopes mínimos y autorización por recurso.

NIST SP 800-207 describe un enfoque zero trust centrado en recursos, que no concede confianza implícita por ubicación de red. La referencia orienta la investigación; no prescribe la arquitectura final.

Fuentes consultadas el 2026-08-29:

- [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST SP 800-207A — control de acceso cloud-native/multi-cloud](https://csrc.nist.gov/pubs/sp/800/207/a/final)
- [MCP Authorization specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)

## Modalidades de despliegue a comparar

| Modalidad | Valor potencial | Riesgos / incógnitas |
| --- | --- | --- |
| Plataforma central multi-tenant con Collector local | Operación centralizada y evolución más rápida. | Residencia de datos, conectividad, confianza del cliente, modelo de aislamiento y soporte del Collector. |
| Instalación completamente on-premise | Puede atender requisitos de aislamiento o regulación más estrictos. | Operación, actualizaciones, soporte, coste, dependencias de IA y consistencia de funcionalidades. |
| Híbrida | Permite decidir qué datos permanecen locales y qué capacidades se centralizan. | Mayor complejidad de límites, sincronización, soporte y seguridad. |

No existe todavía una modalidad recomendada. La selección requiere requisitos reales de clientes, coste de operación y un modelo de amenazas.

## Criterios de aceptación de seguridad para una prueba

1. Contexto de tenant obligatorio y verificable en recopilación, almacenamiento y consulta.
2. Cuenta de fuente dedicada, limitada y revocable; nunca reutilizar credenciales personales.
3. Sin capacidad de escritura contra la infraestructura durante la prueba.
4. Inventario explícito de datos recogidos, ubicación, retención y procedimiento de eliminación.
5. Registro auditable de accesos, errores, cambios de configuración y exportaciones.
6. Prueba negativa de aislamiento: una identidad del tenant A no puede enumerar ni consultar datos del tenant B.
7. Revisión de red, certificados, proxy y salida autorizada antes de conectar un Collector.

## Preguntas de diseño abiertas

- ¿Qué datos técnicos se consideran sensibles para cada tipo de cliente?
- ¿Cuánto tiempo pueden retenerse inventario, logs y respuestas generadas?
- ¿Qué identidad administra Coresolutions y cuál controla el cliente?
- ¿Qué funciones permanecen disponibles en una instalación on-premise?
- ¿Qué versión de MCP y qué clientes serán soportados cuando se apruebe esa capacidad?
