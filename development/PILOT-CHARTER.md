# Carta de piloto — validación del MVP de solo lectura

> **Estado: HYPOTHESIS / TO INVESTIGATE.** Última actualización: 2026-08-30. Este documento prepara una validación; no autoriza desarrollo de producto ni conexión a un entorno sin aprobación explícita.

## Propósito

Organizar una prueba limitada que responda si Proyecto Loreto puede recopilar y presentar información de infraestructura útil, trazable y aislada por tenant, usando vSphere y una fuente de servidores disponible.

## Hipótesis a validar

| ID | Hipótesis | Evidencia mínima necesaria |
| --- | --- | --- |
| PH-01 | Una cuenta de solo lectura puede aportar inventario útil desde vCenter/vSphere. | Resultados de PT-01 y PT-02 del plan de piloto. |
| PH-02 | XClarity o iLO/Redfish aporta inventario y al menos una señal de salud útil en el entorno elegido. | Resultado de PT-04 y lista de campos disponibles/faltantes. |
| PH-03 | Es posible mostrar fuente, hora y calidad de cada dato sin ocultar limitaciones. | Mapeo de datos contra el modelo canónico. |
| PH-04 | El aislamiento de tenant se puede verificar de forma demostrable. | Resultado satisfactorio de PT-05. |
| PH-05 | El alcance puede mantenerse estrictamente en solo lectura y sin exposición administrativa innecesaria. | Revisión de permisos, red y cierre seguro. |

## Alcance del piloto

### Incluido

- Un tenant y un entorno de prueba autorizados.
- Una fuente vCenter/vSphere.
- Una única fuente de servidores: Lenovo XClarity Administrator **o** HPE iLO/Redfish.
- Lectura de los tipos y relaciones definidos en el [modelo canónico](../architecture/CANONICAL-DATA-MODEL.md), solo si las fuentes los exponen.
- Evidencia saneada de permisos, cobertura, calidad, aislamiento y cierre.

### Excluido

- Desarrollo de un producto, conector de producción o interfaz productiva.
- Escritura, cambios, remediación, reinicios o automatización.
- Descubrimiento de red generalizado, escaneo no autorizado o recolección masiva de logs.
- Integraciones adicionales, MCP, IA generativa, alertas o modalidad on-premise completa.
- Datos, secretos, endpoints, nombres de host o capturas sensibles en este repositorio.

## Roles necesarios

| Rol | Responsabilidad candidata | Debe aprobar / aportar |
| --- | --- | --- |
| Patrocinador de Coresolutions | Prioridad, alcance comercial y decisión posterior | Objetivo y continuidad del piloto |
| Responsable del cliente | Autoriza entorno, datos, ventana y requisitos | Aprobación explícita y límites de acceso |
| Administrador de infraestructura | Crea cuentas de mínimo privilegio y valida conectividad | vCenter y XClarity/iLO/Redfish disponibles |
| Seguridad | Revisa red, identidad, retención y modelo de amenazas | Puertas de seguridad antes de conectar |
| Responsable técnico de Loreto | Ejecuta la validación y documenta resultados | Evidencia saneada y riesgos |
| Revisor de producto | Evalúa si los datos sostienen la experiencia MVP | Interpretación de resultados y siguiente decisión |

Ningún rol o persona está asignado todavía.

## Criterios de entrada

Todos deben cumplirse antes de iniciar:

1. Aprobación escrita del entorno, fuentes y ventana de prueba.
2. Tenant de prueba identificado mediante alias no sensible.
3. Cuentas dedicadas de solo lectura, con propietario y procedimiento de revocación.
4. Red, proxy, certificados y ruta de comunicación revisados.
5. Lista de datos a recoger, retención y borrado aprobados.
6. Plan de piloto y modelo de amenazas revisados por las partes responsables.
7. Forma segura de conservar evidencia sin secretos ni detalles sensibles en el repositorio.

## Ejecución y evidencia

La ejecución sigue los casos `PT-01` a `PT-07` del [plan de prueba](../research/PILOT-READONLY-PLAN.md). Para cada caso, registrar únicamente:

- resultado (`PASS`, `PARTIAL`, `FAIL` o `BLOCKED`);
- fecha, responsable y fuente afectada;
- conteos o categorías no sensibles;
- campos/relaciones disponibles y ausentes;
- riesgo descubierto, impacto y acción recomendada;
- enlace a evidencia saneada, si se aprueba conservarla.

## Criterios de salida

### Resultado prometedor

Puede proponerse el siguiente paso si se cumplen los cinco criterios:

1. Las dos fuentes seleccionadas se consultan con permisos de solo lectura.
2. El inventario mínimo y al menos una relación vSphere son recuperables y trazables.
3. La fuente de servidores ofrece datos útiles o define claramente por qué no lo hace.
4. La prueba negativa de aislamiento de tenant es satisfactoria.
5. No existe hallazgo de seguridad o coste operativo que impida continuar sin una mitigación viable.

### Resultado parcial

Se ajustan el modelo canónico, alcance o fuente candidata y se registra la limitación. No se interpreta como aprobación de desarrollo.

### Resultado no viable

Se documenta la evidencia, se marca la hipótesis afectada como `REJECTED` o se redefine, y se evalúan alternativas sin borrar el historial.

## Decisión posterior al piloto

La revisión debe producir un ADR que indique una de estas opciones:

- `GO`: proponer alcance de MVP, integración inicial y plan de construcción, aún sujeto a aprobación.
- `ITERATE`: repetir una prueba acotada con alcance, fuente o controles corregidos.
- `NO-GO`: detener esa dirección por inviabilidad técnica, de seguridad, valor o coste.

No se ha elegido todavía ninguna opción.

## Documentos de ejecución

- [Especificación funcional del MVP](../product/MVP-SPECIFICATION.md)
- [Modelo canónico de datos](../architecture/CANONICAL-DATA-MODEL.md)
- [Modelo de amenazas](../architecture/THREAT-MODEL-MVP.md)
- [Plan de piloto de solo lectura](../research/PILOT-READONLY-PLAN.md)
- [Guia de preparacion del laboratorio interno (PDF)](../output/pdf/guia-laboratorio-interno-loreto.pdf)
- [Registro de decisiones](DECISIONS.md)
