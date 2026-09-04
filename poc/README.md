# PoC técnica — Collector de solo lectura

> **Estado: PoC autorizada por ADR-0002 en [development/DECISIONS.md](../development/DECISIONS.md).** No es código de producto. Ejecutar únicamente contra infraestructura propia del responsable del proyecto, nunca contra datos de un cliente real.

## Qué prueba esta PoC

Si el flujo completo **leer (solo lectura) → normalizar al modelo canónico → mostrar un resultado legible** tiene sentido operativo y de producto, antes de comprometer stack, nube o modelo de datos definitivo. No es un conector de producción ni una demostración lista para cliente.

## Qué no es

- No es el Collector de producto: no tiene instalador, actualización, resiliencia offline ni empaquetado.
- No implementa multi-tenancy real ni ninguna de las estrategias comparadas en [MULTITENANCY-COLLECTOR-OPTIONS.md](../research/MULTITENANCY-COLLECTOR-OPTIONS.md); usa un único tenant fijo por ejecución.
- No decide lenguaje, framework, base de datos ni proveedor cloud definitivos para el producto.
- No debe apuntarse a un cliente real bajo ninguna circunstancia sin una autorización separada.

## Contenido

- `collector/canonical_model.py` — estructuras mínimas (Tenant, Source, SyncRun, Asset, Observation, Relationship) siguiendo [CANONICAL-DATA-MODEL.md](../architecture/CANONICAL-DATA-MODEL.md).
- `collector/collector.py` — se conecta a vSphere y XClarity (mismas variables de entorno que [research/pilot-scripts](../research/pilot-scripts/README.md)), normaliza lo leído y escribe un bundle canónico local.
- `collector/.env.example` — plantilla de configuración; nunca completar `.env` con datos reales dentro del repositorio.

## Cómo correrlo

```bash
cd poc/collector
cp .env.example .env   # completar con la cuenta de solo lectura del laboratorio propio
pip install requests
set -a; source .env; set +a
python3 collector.py
```

Salida:

- Un resumen saneado (conteos por tipo de activo, calidad de observación, tipo de relación) impreso en consola.
- Un archivo JSON completo con el bundle canónico en `collector/output/<timestamp>.json`, ignorado por git. Revísalo localmente para juzgar si la normalización tiene sentido; no lo subas al repositorio ni lo pegues completo en una conversación.

## Límites de datos

- Todo identificador (host, VM, cluster, servidor físico) se reemplaza por un alias no reversible antes de guardarse.
- Solo se conservan campos no identificatorios en las observaciones (estado de conexión, estado de energía, salud). Todo lo demás se descarta.
- `uses_storage` (VM–datastore) no está implementado; es una limitación conocida, no un dato oculto.

## Qué sigue si la PoC muestra algo prometedor

No decide nada por sí sola. Un resultado prometedor debe registrarse como evidencia en [PILOT-READONLY-PLAN.md](../research/PILOT-READONLY-PLAN.md) y discutirse antes de ampliar el alcance (más tipos de activo, más fuentes, cualquier forma de reporte compartible con un cliente). Ampliar esta PoC hacia producto real requiere una nueva decisión de alcance, no una continuación implícita del código.
