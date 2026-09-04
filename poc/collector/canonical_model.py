"""Estructuras mínimas del modelo canónico para la PoC (ver architecture/CANONICAL-DATA-MODEL.md).

No es un esquema de base de datos ni una implementación de producto: son
dataclasses desechables para probar si el flujo Collector -> normalización
-> reporte tiene sentido. Nombres de campos y tipos siguen el documento
canónico, pero pueden cambiar sin previo aviso mientras la PoC esté activa.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import asdict, dataclass, field


def stable_alias(raw_value: str, prefix: str) -> str:
    """Alias no reversible para no conservar identificadores reales del cliente."""
    digest = hashlib.sha256(raw_value.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{digest}"


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


@dataclass
class Tenant:
    tenant_id: str
    alias: str


@dataclass
class Source:
    source_id: str
    tenant_id: str
    family: str  # "vsphere" | "xclarity"
    version: str | None
    last_read: str


@dataclass
class SyncRun:
    sync_run_id: str
    tenant_id: str
    source_id: str
    started_at: str
    finished_at: str | None = None
    result: str = "IN_PROGRESS"  # IN_PROGRESS | COMPLETE | PARTIAL | ERROR


@dataclass
class Asset:
    asset_id: str
    tenant_id: str
    type: str  # datacenter | cluster | host | vm | datastore | physical_server
    alias: str
    derived_state: str = "UNKNOWN"


@dataclass
class Observation:
    observation_id: str
    tenant_id: str
    asset_id: str
    source_id: str
    field: str
    value: str
    observed_at: str
    quality: str = "COMPLETE"  # COMPLETE | PARTIAL | STALE | UNAVAILABLE | ERROR


@dataclass
class Relationship:
    relationship_id: str
    tenant_id: str
    from_asset: str
    to_asset: str
    type: str  # contains | runs_on | uses_storage | managed_by
    method: str  # "observed"
    source_id: str
    observed_at: str


@dataclass
class CanonicalBundle:
    tenant: Tenant
    sources: list[Source] = field(default_factory=list)
    sync_runs: list[SyncRun] = field(default_factory=list)
    assets: list[Asset] = field(default_factory=list)
    observations: list[Observation] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "tenant": asdict(self.tenant),
            "sources": [asdict(s) for s in self.sources],
            "sync_runs": [asdict(s) for s in self.sync_runs],
            "assets": [asdict(a) for a in self.assets],
            "observations": [asdict(o) for o in self.observations],
            "relationships": [asdict(r) for r in self.relationships],
        }

    def summary(self) -> dict:
        """Resumen saneado: conteos y tipos de calidad, sin ningún alias ni valor crudo."""
        quality_counts: dict[str, int] = {}
        for obs in self.observations:
            quality_counts[obs.quality] = quality_counts.get(obs.quality, 0) + 1
        asset_type_counts: dict[str, int] = {}
        for asset in self.assets:
            asset_type_counts[asset.type] = asset_type_counts.get(asset.type, 0) + 1
        relationship_type_counts: dict[str, int] = {}
        for rel in self.relationships:
            relationship_type_counts[rel.type] = relationship_type_counts.get(rel.type, 0) + 1
        return {
            "tenant_alias": self.tenant.alias,
            "sources": len(self.sources),
            "sync_runs": len(self.sync_runs),
            "assets_total": len(self.assets),
            "assets_by_type": asset_type_counts,
            "observations_total": len(self.observations),
            "observations_by_quality": quality_counts,
            "relationships_total": len(self.relationships),
            "relationships_by_type": relationship_type_counts,
        }
