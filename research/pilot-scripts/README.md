# Scripts del piloto de solo lectura

> **Estado: TO INVESTIGATE.** Herramientas de apoyo para ejecutar el [plan de piloto de solo lectura](../PILOT-READONLY-PLAN.md). No son conectores de producto ni código de aplicación: existen solo para producir evidencia de factibilidad.

## Contenido

- `readonly_pilot_check.py` — ejecuta PT-02, PT-03, PT-04 y el manejo de errores de PT-06 contra un vCenter y un XClarity Administrator reales, usando cuentas dedicadas de solo lectura. Configuración por variables de entorno; nunca por argumentos en texto plano ni archivos versionados.

## Reglas de ejecución

- Ejecutar únicamente contra el tenant/entorno de piloto autorizado, con cuentas de solo lectura dedicadas.
- Nunca commitear archivos `.env`, capturas de pantalla ni salidas crudas del script al repositorio.
- El script ya sanea identificadores (alias no reversibles) antes de imprimirlos, pero la responsabilidad de no pegar salida cruda en el repo o en el historial de esta conversación es de quien lo ejecuta.
- PT-01 (verificación de rol/privilegios), PT-05 (prueba negativa de aislamiento) y PT-07 (revocación y limpieza) son pasos manuales, no automatizados aquí.
- Los resultados saneados alimentan la tabla "Registro de ejecución" de `PILOT-READONLY-PLAN.md`.

## Por qué no se ejecuta desde esta sesión de IA

El plan de piloto prohíbe exponer interfaces administrativas hacia Internet. Una sesión de agente que corre fuera de la red del cliente no debe ser el punto que se conecte directamente al vCenter/XClarity del piloto salvo que el responsable del entorno confirme explícitamente una ruta de acceso ya autorizada y restringida. Por eso este script está pensado para ejecutarse dentro de la red donde vive el entorno de piloto.
