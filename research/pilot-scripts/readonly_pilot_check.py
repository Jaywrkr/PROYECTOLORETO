#!/usr/bin/env python3
"""Prueba de solo lectura para el piloto de Proyecto Loreto (PT-02, PT-03, PT-04, PT-06).

Ejecuta lecturas mínimas contra vSphere (REST API) y Lenovo XClarity Administrator
(REST API) usando cuentas dedicadas de solo lectura, y produce un resumen saneado
(sin nombres, IPs, seriales ni credenciales) que puede volcarse en la tabla de
"Registro de ejecución" de research/PILOT-READONLY-PLAN.md.

No crea, modifica ni elimina nada. No reintenta operaciones fallidas de forma
agresiva. No imprime ni guarda identificadores sensibles en texto plano.

Este script NO cubre:
  - PT-01 (verificación del rol/privilegios de la cuenta): confirmar manualmente
    en vCenter/XClarity antes de ejecutar este script.
  - PT-05 (prueba negativa de aislamiento con una identidad ajena al tenant):
    requiere una segunda cuenta fuera de alcance; ejecutar por separado.
  - PT-07 (revocar cuentas y eliminar datos de prueba): paso operativo posterior.

Uso:
    export VSPHERE_HOST=https://vcenter.ejemplo.local
    export VSPHERE_USER=usuario_solo_lectura
    export VSPHERE_PASSWORD=...
    export VSPHERE_VERIFY_SSL=true            # false solo en laboratorio con CA propia
    export XCLARITY_HOST=https://xclarity.ejemplo.local
    export XCLARITY_USER=usuario_solo_lectura
    export XCLARITY_PASSWORD=...
    export XCLARITY_VERIFY_SSL=true
    python3 readonly_pilot_check.py

Ninguna variable con secretos debe escribirse en un archivo dentro del repositorio.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import dataclass, field

import requests

TIMEOUT_SECONDS = 15


def env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() not in ("false", "0", "no")


def alias(value: str, prefix: str) -> str:
    """Reemplaza un identificador real por un alias no reversible."""
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}-{digest}"


@dataclass
class TestResult:
    test_id: str
    description: str
    status: str  # PASSED, FAILED, SKIPPED
    detail: dict = field(default_factory=dict)
    error: str | None = None


def vsphere_session(host: str, user: str, password: str, verify_ssl: bool) -> str | None:
    """PT-02 (parte 1): autentica y abre sesión de solo lectura."""
    url = f"{host.rstrip('/')}/api/session"
    try:
        resp = requests.post(url, auth=(user, password), verify=verify_ssl, timeout=TIMEOUT_SECONDS)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:
        print(f"[vSphere] No se pudo abrir sesión: {sanitize_exception(exc)}", file=sys.stderr)
        return None


def vsphere_get(host: str, path: str, session_token: str, verify_ssl: bool):
    url = f"{host.rstrip('/')}{path}"
    headers = {"vmware-api-session-id": session_token}
    resp = requests.get(url, headers=headers, verify=verify_ssl, timeout=TIMEOUT_SECONDS)
    resp.raise_for_status()
    return resp.json()


def run_vsphere_checks(results: list[TestResult]) -> None:
    host = os.environ.get("VSPHERE_HOST")
    user = os.environ.get("VSPHERE_USER")
    password = os.environ.get("VSPHERE_PASSWORD")
    verify_ssl = env_bool("VSPHERE_VERIFY_SSL", True)

    if not (host and user and password):
        results.append(TestResult("PT-02/03", "Inventario y relaciones de vSphere", "SKIPPED",
                                   error="Variables VSPHERE_HOST/USER/PASSWORD no configuradas"))
        return

    token = vsphere_session(host, user, password, verify_ssl)
    if token is None:
        results.append(TestResult("PT-02", "Conectar a vSphere y leer inventario mínimo", "FAILED",
                                   error="Fallo de autenticación o conectividad"))
        return

    try:
        datacenters = vsphere_get(host, "/api/vcenter/datacenter", token, verify_ssl)
        clusters = vsphere_get(host, "/api/vcenter/cluster", token, verify_ssl)
        hosts = vsphere_get(host, "/api/vcenter/host", token, verify_ssl)
        vms = vsphere_get(host, "/api/vcenter/vm", token, verify_ssl)
        datastores = vsphere_get(host, "/api/vcenter/datastore", token, verify_ssl)
    except requests.RequestException as exc:
        results.append(TestResult("PT-02", "Conectar a vSphere y leer inventario mínimo", "FAILED",
                                   error=sanitize_exception(exc)))
        return

    results.append(TestResult(
        "PT-02", "Conectar a vSphere y leer inventario mínimo", "PASSED",
        detail={
            "datacenters": len(datacenters),
            "clusters": len(clusters),
            "hosts": len(hosts),
            "vms": len(vms),
            "datastores": len(datastores),
        },
    ))

    # PT-03: relaciones observadas directamente disponibles en las listas anteriores.
    relationship_counts = {"contains_cluster_host": 0, "runs_on_host_vm": 0}
    try:
        for cluster in clusters:
            cluster_hosts = vsphere_get(
                host, f"/api/vcenter/host?filter.clusters={cluster['cluster']}", token, verify_ssl
            )
            relationship_counts["contains_cluster_host"] += len(cluster_hosts)
        for host_item in hosts:
            host_vms = vsphere_get(
                host, f"/api/vcenter/vm?filter.hosts={host_item['host']}", token, verify_ssl
            )
            relationship_counts["runs_on_host_vm"] += len(host_vms)
        results.append(TestResult(
            "PT-03", "Leer relaciones vSphere (contains, runs_on)", "PASSED",
            detail=relationship_counts | {
                "nota": "uses_storage (VM-datastore) no implementado en este PoC; requiere "
                        "leer discos por VM. Registrar como campo pendiente, no ocultar.",
            },
        ))
    except requests.RequestException as exc:
        results.append(TestResult("PT-03", "Leer relaciones vSphere", "FAILED",
                                   error=sanitize_exception(exc)))

    # Ejemplo de saneamiento: nunca se guarda el nombre real del host, solo un alias.
    sample_host_aliases = [alias(h.get("name", ""), "HOST") for h in hosts[:5]]
    results[-1].detail["muestra_alias_hosts"] = sample_host_aliases


def xclarity_session(host: str, user: str, password: str, verify_ssl: bool):
    url = f"{host.rstrip('/')}/login"
    payload = {"userName": user, "password": password}
    try:
        resp = requests.post(url, json=payload, verify=verify_ssl, timeout=TIMEOUT_SECONDS)
        resp.raise_for_status()
        return resp.cookies
    except requests.RequestException as exc:
        print(f"[XClarity] No se pudo abrir sesión: {sanitize_exception(exc)}", file=sys.stderr)
        return None


def run_xclarity_checks(results: list[TestResult]) -> None:
    host = os.environ.get("XCLARITY_HOST")
    user = os.environ.get("XCLARITY_USER")
    password = os.environ.get("XCLARITY_PASSWORD")
    verify_ssl = env_bool("XCLARITY_VERIFY_SSL", True)

    if not (host and user and password):
        results.append(TestResult("PT-04", "Conectar a XClarity y leer inventario/salud", "SKIPPED",
                                   error="Variables XCLARITY_HOST/USER/PASSWORD no configuradas"))
        return

    cookies = xclarity_session(host, user, password, verify_ssl)
    if cookies is None:
        results.append(TestResult("PT-04", "Conectar a XClarity y leer inventario/salud", "FAILED",
                                   error="Fallo de autenticación o conectividad"))
        return

    try:
        url = f"{host.rstrip('/')}/nodes"
        resp = requests.get(url, cookies=cookies, verify=verify_ssl, timeout=TIMEOUT_SECONDS)
        resp.raise_for_status()
        nodes = resp.json().get("nodeList", resp.json() if isinstance(resp.json(), list) else [])
    except requests.RequestException as exc:
        results.append(TestResult("PT-04", "Conectar a XClarity y leer inventario/salud", "FAILED",
                                   error=sanitize_exception(exc)))
        return

    health_states = {}
    missing_health = 0
    for node in nodes:
        health = node.get("health") or node.get("powerStatus")
        if health is None:
            missing_health += 1
        else:
            health_states[str(health)] = health_states.get(str(health), 0) + 1

    results.append(TestResult(
        "PT-04", "Conectar a XClarity y leer inventario/salud", "PASSED",
        detail={
            "servidores_gestionados": len(nodes),
            "distribucion_salud": health_states,
            "servidores_sin_campo_salud": missing_health,
        },
    ))


def sanitize_exception(exc: Exception) -> str:
    """Evita que un mensaje de error incluya URL completa, headers o payload con secretos."""
    return type(exc).__name__


def main() -> int:
    results: list[TestResult] = []
    run_vsphere_checks(results)
    run_xclarity_checks(results)

    summary = [
        {
            "id": r.test_id,
            "descripcion": r.description,
            "estado": r.status,
            "detalle": r.detail,
            "error": r.error,
        }
        for r in results
    ]

    print(json.dumps(summary, ensure_ascii=False, indent=2))

    print(
        "\nRecordatorio: PT-01, PT-05 y PT-07 no están cubiertos por este script y "
        "deben confirmarse manualmente (ver research/PILOT-READONLY-PLAN.md). "
        "Copia solo los valores saneados de este resumen a la tabla de registro; "
        "nunca pegues salida cruda con hostnames, IPs o seriales en el repositorio.",
        file=sys.stderr,
    )

    return 0 if all(r.status != "FAILED" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
