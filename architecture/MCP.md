# MCP y acceso de agentes

> **Estado: HYPOTHESIS.** Se evalúa exponer capacidades mediante MCP para herramientas y agentes autorizados.

## Objetivo hipotético

Permitir que ChatGPT, Claude u otros agentes consulten información de infraestructura dentro de los permisos concedidos, con respuestas trazables y confinadas al tenant correspondiente.

## Límites iniciales propuestos

- **HYPOTHESIS:** Empezar con capacidades de solo lectura.
- **HYPOTHESIS:** Incluir tenant, identidad, autorización y auditoría en cada invocación.
- **HYPOTHESIS:** Atribuir las respuestas a fuentes y fecha de actualización.
- **OPEN QUESTION:** ¿Qué datos deben filtrarse, resumirse o prohibirse en las respuestas de agentes?
- **OPEN QUESTION:** ¿Cómo se previenen instrucciones maliciosas, sobreexposición y escalamiento de privilegios?

## Evolución a evaluar

Consulta → reporte → alerta proactiva → recomendación → acción controlada. Cada paso posterior requiere una decisión de seguridad, autorización, trazabilidad y reversibilidad.

## Hallazgo de investigación

**TO INVESTIGATE:** Las especificaciones de autorización de MCP cambian con el protocolo; una implementación futura deberá adoptar la versión vigente y verificar compatibilidad de clientes. La especificación de autorización publicada para 2025-11-25 exige metadatos de recurso protegido y detalla OAuth 2.1, descubrimiento de autorización y minimización de scopes. Esto no constituye una decisión de implementación.

Fuente consultada el 2026-08-29: [MCP Authorization specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization).
