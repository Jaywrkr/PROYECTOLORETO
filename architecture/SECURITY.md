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

## Marco inicial a evaluar

**HYPOTHESIS:** Usar principios de zero trust como referencia: autenticar y autorizar de forma explícita identidades humanas, de servicio y de Collector; no confiar solo en la ubicación de red; y registrar accesos y cambios de privilegios. Esto no selecciona proveedor ni mecanismo concreto.

NIST describe zero trust como un enfoque que centra la protección en recursos y no concede confianza implícita por ubicación o propiedad de red. Fuente consultada el 2026-08-29: [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final).

Ver también [seguridad y despliegue inicial](../research/SECURITY-DEPLOYMENT-INITIAL.md).

El análisis de escenarios y puertas de seguridad para el piloto está en [THREAT-MODEL-MVP.md](THREAT-MODEL-MVP.md).
