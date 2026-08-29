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
