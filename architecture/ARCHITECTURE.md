# Arquitectura conceptual

> **Estado: HYPOTHESIS.** No existe una arquitectura implementada ni una selección tecnológica.

## Principios propuestos para validar

1. **Aislamiento por cliente:** el acceso debe mantenerse dentro del tenant autorizado.
2. **Complementariedad:** la plataforma no reemplaza las herramientas de administración de fabricantes.
3. **Trazabilidad:** toda información debe conservar fuente, momento de recopilación y nivel de confianza cuando sea posible.
4. **Mínimo privilegio:** conectores, usuarios y agentes reciben solo los permisos necesarios.
5. **Despliegue adaptable:** evaluar plataforma central multi-tenant y opciones on-premise sin asumir que ambas serán viables para el mismo alcance.
6. **Evolución controlada:** observación antes que recomendaciones; recomendaciones antes que acciones automatizadas.

## Componentes hipotéticos

```text
Fuentes del cliente ──> Conectores / Collector ──> Ingesta segura ──> Plataforma por tenant
 (APIs, SNMP, logs,         (posible agente         (por definir)       ├─ inventario y relaciones
  herramientas existentes)  local)                                      ├─ consultas y reportes
                                                                        └─ MCP autorizado
```

El diagrama es conceptual: no define protocolos, proveedores, datos, límites de red ni topología de despliegue.

## Dominios por definir

| Dominio | Preguntas principales |
| --- | --- |
| Ingesta | ¿Qué conectores, frecuencias, permisos y mecanismos de entrega son sostenibles? |
| Datos | ¿Cuál es el modelo mínimo de activos, relaciones, eventos, configuración y procedencia? |
| Acceso | ¿Cómo se autentican y autorizan usuarios, servicios y agentes? |
| Aislamiento | ¿Qué controles de tenant se aplican en identidad, datos, APIs, telemetría y operaciones? |
| Despliegue | ¿Qué límites y diferencias tendrá cloud central frente a on-premise? |
| IA/MCP | ¿Qué contexto, herramientas de lectura, auditoría y límites son seguros? |

El modelo conceptual que orienta el piloto está en [CANONICAL-DATA-MODEL.md](CANONICAL-DATA-MODEL.md).

Los riesgos y límites de confianza del piloto están en [THREAT-MODEL-MVP.md](THREAT-MODEL-MVP.md).

## Fuera de alcance actual

- Decisiones de lenguaje, framework, nube, base de datos o proveedor de IA.
- Ejecución de cambios sobre infraestructura.
- Compromisos de cobertura por fabricante.
