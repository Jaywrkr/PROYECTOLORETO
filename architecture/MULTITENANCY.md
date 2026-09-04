# Multi-tenancy y aislamiento

> **Estado: requisito confirmado; diseño de implementación abierto.**

## Invariante

**CONFIRMED:** Un cliente no puede acceder a información de otro cliente.

## Áreas que deben aislarse

- Identidades, sesiones, roles y permisos.
- Datos de inventario, relaciones, eventos, logs y documentos derivados.
- Solicitudes de API, consultas en lenguaje natural y herramientas MCP.
- Credenciales de conectores, secretos y configuraciones de despliegue.
- Procesamiento asíncrono, cachés, índices, observabilidad y soporte operacional.
- Exportaciones, reportes, respaldos y recuperación ante desastres.

## Decisiones pendientes

**OPEN QUESTION:** ¿Qué estrategia de aislamiento de datos corresponde a cada modalidad: base compartida con controles lógicos, esquema por tenant, base por tenant u otra?

**OPEN QUESTION:** ¿Cómo se representará el contexto de tenant de forma obligatoria y verificable de extremo a extremo?

**OPEN QUESTION:** ¿Qué modelo de delegación permite a Coresolutions apoyar a un cliente sin cruzar sus límites de acceso?

## Criterios de aceptación futuros

Antes de implementar, cada propuesta debe demostrar controles de prevención, pruebas de aislamiento, auditoría y tratamiento de fallos que impidan la mezcla de tenants.

## Investigación relacionada

Una comparación de estrategias candidatas (base compartida con controles lógicos, esquema por tenant, base por tenant, modelo híbrido) está en [MULTITENANCY-COLLECTOR-OPTIONS.md](../research/MULTITENANCY-COLLECTOR-OPTIONS.md). Es investigación de escritorio, no una decisión.
