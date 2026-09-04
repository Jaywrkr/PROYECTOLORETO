#!/usr/bin/env python3
"""PoC de Collector — autorizada por ADR-0002 (development/DECISIONS.md).

Lee vSphere y Lenovo XClarity Administrator en modo solo lectura y normaliza
lo obtenido al modelo canónico mínimo (Tenant/Source/SyncRun/Asset/
Observation/Relationship) descrito en architecture/CANONICAL-DATA-MODEL.md.

Alcance deliberado de esta PoC:
  - Un único tenant fijo por ejecución (alias, nunca el nombre real del cliente).
  - Solo los tipos de activo y relación ya listados como candidatos en el
    modelo canónico: datacenter, cluster, host, vm, datastore (vSphere) y
    servidor físico (XClarity), con relaciones contains/runs_on/managed_by.
  - `uses_storage` (VM-datastore) queda fuera, igual que en el script de
    verificación de piloto: requiere leer discos por VM.
  - Solo se conservan campos no identificatorios en las observaciones
    (estado de conexión, estado de energía, salud). Nunca nombre, IP,
    serial ni hostname en texto plano.

Esta PoC NO es el Collector de producto: es código desechable para validar
si el flujo completo (leer -> normalizar -> reportar) tiene sentido. No
debe apuntarse a datos de un cliente real, solo a infraestructura propia.

Uso: igual que research/pilot-scripts/readonly_pilot_check.py (mismas
variables de entorno VSPHERE_*/XCLARITY_*), más:
    export TENANT_ALIAS=lab-interno   # opcional, por defecto "poc-tenant"

Salida:
  - Resumen saneado (conteos) impreso en stdout.
  - Bundle canónico completo escrito en poc/collector/output/<timestamp>.json
    (carpeta ignorada por git; nunca commitear su contenido).
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))

from canonical_model import (  # noqa: E402
    Asset,
    CanonicalBundle,
    Observation,
    Relationship,
    Source,
    SyncRun,
    Tenant,
    now_iso,
    stable_alias,
)

TIMEOUT_SECONDS = 15

# Campos permitidos por observación: todo lo demás se descarta, no se guarda.
VSPHERE_HOST_FIELDS = {"connection_state", "power_state"}
VSPHERE_VM_FIELDS = {"power_state"}
XCLARITY_NODE_FIELDS = {"health", "powerStatus"}


def env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() not in ("false", "0", "no")


def sanitize_exception(exc: Exception) -> str:
    return type(exc).__name__


def collect_vsphere(bundle: CanonicalBundle) -> None:
    host = os.environ.get("VSPHERE_HOST")
    user = os.environ.get("VSPHERE_USER")
    password = os.environ.get("VSPHERE_PASSWORD")
    verify_ssl = env_bool("VSPHERE_VERIFY_SSL", True)
    if not (host and user and password):
        print("[vSphere] Variables no configuradas; se omite esta fuente.", file=sys.stderr)
        return

    source = Source(
        source_id=stable_alias(host, "SRC-VSPHERE"),
        tenant_id=bundle.tenant.tenant_id,
        family="vsphere",
        version=None,
        last_read=now_iso(),
    )
    bundle.sources.append(source)
    sync_run = SyncRun(
        sync_run_id=stable_alias(host + str(time.time()), "SYNC"),
        tenant_id=bundle.tenant.tenant_id,
        source_id=source.source_id,
        started_at=now_iso(),
    )
    bundle.sync_runs.append(sync_run)

    try:
        session_url = f"{host.rstrip('/')}/api/session"
        resp = requests.post(session_url, auth=(user, password), verify=verify_ssl, timeout=TIMEOUT_SECONDS)
        resp.raise_for_status()
        token = resp.json()
        headers = {"vmware-api-session-id": token}

        def get(path: str):
            r = requests.get(f"{host.rstrip('/')}{path}", headers=headers, verify=verify_ssl, timeout=TIMEOUT_SECONDS)
            r.raise_for_status()
            return r.json()

        clusters = get("/api/vcenter/cluster")
        hosts = get("/api/vcenter/host")
        vms = get("/api/vcenter/vm")
        datastores = get("/api/vcenter/datastore")

        cluster_asset_by_id = {}
        for c in clusters:
            asset = Asset(
                asset_id=stable_alias(c["cluster"], "ASSET-CLUSTER"),
                tenant_id=bundle.tenant.tenant_id,
                type="cluster",
                alias=stable_alias(c.get("name", c["cluster"]), "cluster"),
            )
            bundle.assets.append(asset)
            cluster_asset_by_id[c["cluster"]] = asset

        host_asset_by_id = {}
        for h in hosts:
            asset = Asset(
                asset_id=stable_alias(h["host"], "ASSET-HOST"),
                tenant_id=bundle.tenant.tenant_id,
                type="host",
                alias=stable_alias(h.get("name", h["host"]), "host"),
            )
            bundle.assets.append(asset)
            host_asset_by_id[h["host"]] = asset
            for f in VSPHERE_HOST_FIELDS:
                if f in h:
                    bundle.observations.append(Observation(
                        observation_id=stable_alias(h["host"] + f, "OBS"),
                        tenant_id=bundle.tenant.tenant_id,
                        asset_id=asset.asset_id,
                        source_id=source.source_id,
                        field=f,
                        value=str(h[f]),
                        observed_at=now_iso(),
                    ))

        for ds in datastores:
            asset = Asset(
                asset_id=stable_alias(ds["datastore"], "ASSET-DATASTORE"),
                tenant_id=bundle.tenant.tenant_id,
                type="datastore",
                alias=stable_alias(ds.get("name", ds["datastore"]), "datastore"),
            )
            bundle.assets.append(asset)

        for vm in vms:
            asset = Asset(
                asset_id=stable_alias(vm["vm"], "ASSET-VM"),
                tenant_id=bundle.tenant.tenant_id,
                type="vm",
                alias=stable_alias(vm.get("name", vm["vm"]), "vm"),
            )
            bundle.assets.append(asset)
            for f in VSPHERE_VM_FIELDS:
                if f in vm:
                    bundle.observations.append(Observation(
                        observation_id=stable_alias(vm["vm"] + f, "OBS"),
                        tenant_id=bundle.tenant.tenant_id,
                        asset_id=asset.asset_id,
                        source_id=source.source_id,
                        field=f,
                        value=str(vm[f]),
                        observed_at=now_iso(),
                    ))
            host_id = vm.get("host")
            if host_id and host_id in host_asset_by_id:
                bundle.relationships.append(Relationship(
                    relationship_id=stable_alias(vm["vm"] + host_id, "REL"),
                    tenant_id=bundle.tenant.tenant_id,
                    from_asset=asset.asset_id,
                    to_asset=host_asset_by_id[host_id].asset_id,
                    type="runs_on",
                    method="observed",
                    source_id=source.source_id,
                    observed_at=now_iso(),
                ))

        for h in hosts:
            cluster_id = h.get("cluster")
            if cluster_id and cluster_id in cluster_asset_by_id:
                bundle.relationships.append(Relationship(
                    relationship_id=stable_alias(cluster_id + h["host"], "REL"),
                    tenant_id=bundle.tenant.tenant_id,
                    from_asset=cluster_asset_by_id[cluster_id].asset_id,
                    to_asset=host_asset_by_id[h["host"]].asset_id,
                    type="contains",
                    method="observed",
                    source_id=source.source_id,
                    observed_at=now_iso(),
                ))

        sync_run.finished_at = now_iso()
        sync_run.result = "COMPLETE"
    except requests.RequestException as exc:
        sync_run.finished_at = now_iso()
        sync_run.result = "ERROR"
        print(f"[vSphere] Error durante la lectura: {sanitize_exception(exc)}", file=sys.stderr)


def collect_xclarity(bundle: CanonicalBundle) -> None:
    host = os.environ.get("XCLARITY_HOST")
    user = os.environ.get("XCLARITY_USER")
    password = os.environ.get("XCLARITY_PASSWORD")
    verify_ssl = env_bool("XCLARITY_VERIFY_SSL", True)
    if not (host and user and password):
        print("[XClarity] Variables no configuradas; se omite esta fuente.", file=sys.stderr)
        return

    source = Source(
        source_id=stable_alias(host, "SRC-XCLARITY"),
        tenant_id=bundle.tenant.tenant_id,
        family="xclarity",
        version=None,
        last_read=now_iso(),
    )
    bundle.sources.append(source)
    sync_run = SyncRun(
        sync_run_id=stable_alias(host + str(time.time()), "SYNC"),
        tenant_id=bundle.tenant.tenant_id,
        source_id=source.source_id,
        started_at=now_iso(),
    )
    bundle.sync_runs.append(sync_run)

    try:
        login_url = f"{host.rstrip('/')}/login"
        resp = requests.post(login_url, json={"userName": user, "password": password},
                              verify=verify_ssl, timeout=TIMEOUT_SECONDS)
        resp.raise_for_status()
        cookies = resp.cookies

        nodes_resp = requests.get(f"{host.rstrip('/')}/nodes", cookies=cookies,
                                   verify=verify_ssl, timeout=TIMEOUT_SECONDS)
        nodes_resp.raise_for_status()
        payload = nodes_resp.json()
        nodes = payload.get("nodeList", payload if isinstance(payload, list) else [])

        for node in nodes:
            raw_id = str(node.get("uuid") or node.get("uuid_2") or node.get("name") or id(node))
            asset = Asset(
                asset_id=stable_alias(raw_id, "ASSET-SERVER"),
                tenant_id=bundle.tenant.tenant_id,
                type="physical_server",
                alias=stable_alias(node.get("name", raw_id), "server"),
            )
            bundle.assets.append(asset)
            for f in XCLARITY_NODE_FIELDS:
                if f in node and node[f] is not None:
                    bundle.observations.append(Observation(
                        observation_id=stable_alias(raw_id + f, "OBS"),
                        tenant_id=bundle.tenant.tenant_id,
                        asset_id=asset.asset_id,
                        source_id=source.source_id,
                        field=f,
                        value=str(node[f]),
                        observed_at=now_iso(),
                    ))
            bundle.relationships.append(Relationship(
                relationship_id=stable_alias(raw_id + "managed", "REL"),
                tenant_id=bundle.tenant.tenant_id,
                from_asset=asset.asset_id,
                to_asset=source.source_id,
                type="managed_by",
                method="observed",
                source_id=source.source_id,
                observed_at=now_iso(),
            ))

        sync_run.finished_at = now_iso()
        sync_run.result = "COMPLETE"
    except requests.RequestException as exc:
        sync_run.finished_at = now_iso()
        sync_run.result = "ERROR"
        print(f"[XClarity] Error durante la lectura: {sanitize_exception(exc)}", file=sys.stderr)


def main() -> int:
    tenant_alias = os.environ.get("TENANT_ALIAS", "poc-tenant")
    tenant = Tenant(tenant_id=stable_alias(tenant_alias, "TENANT"), alias=tenant_alias)
    bundle = CanonicalBundle(tenant=tenant)

    collect_vsphere(bundle)
    collect_xclarity(bundle)

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{int(time.time())}.json"
    output_path.write_text(json.dumps(bundle.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    summary = bundle.summary()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\nBundle canónico completo (local, NO commitear): {output_path}", file=sys.stderr)

    had_error = any(run.result == "ERROR" for run in bundle.sync_runs)
    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main())
