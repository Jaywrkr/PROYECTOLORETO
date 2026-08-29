# Seguridad

> **Estado: TO INVESTIGATE.** Este documento reúne requisitos y amenazas a investigar; no prescribe todavía controles implementados.

## Requisitos confirmados

- **CONFIRMED:** Aislamiento estricto entre clientes.
- **CONFIRMED:** La plataforma puede tratar información sensible sobre infraestructura del cliente.

## Requisitos e hipótesis a validar

- **HYPOTHESIS:** Collector local con comunicación saliente segura hacia una plataforma central.
- **HYPOTHESIS:** Opción de despliegue completamente on-premise para requisitos regulatorios más exigentes.
- **TO INVESTIGATE:** Autenticación de usuarios, servicios y agentes; RBAC/ABAC; auditoría; gestión de secretos; cifrado; retención; residencia; respuesta a incidentes; soporte remoto; y requisitos regulatorios aplicables.

## Modelo de amenazas inicial

| Riesgo | Pregunta de control |
| --- | --- |
| Acceso cruzado de tenants | ¿Cómo se previene, detecta y prueba en todos los planos? |
| Compromiso de Collector | ¿Qué privilegios mínimos, identidad, actualización y revocación necesita? |
| Filtración de secretos | ¿Dónde se guardan y quién puede usarlos o rotarlos? |
| Datos sensibles en IA/MCP | ¿Qué se envía, a qué proveedor, bajo qué autorización y con qué registro? |
| Automatización peligrosa | ¿Qué aprobaciones, límites, reversibilidad y segregación se exigen? |

## Próximo trabajo

Crear requisitos de seguridad y privacidad basados en los clientes objetivo, el modelo de despliegue y una evaluación formal de amenazas.
