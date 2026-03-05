"""Pydantic models for Honua Admin API."""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Literal
from pydantic import BaseModel, Field


# Base Models

class HonuaBaseModel(BaseModel):
    """Base model with common configuration."""

    class Config:
        extra = 'forbid'
        str_strip_whitespace = True


# Service Models

class ServiceSummary(HonuaBaseModel):
    """Summary information about a service."""
    name: str
    display_name: str
    enabled: bool
    protocols: List[str]
    last_modified: datetime


class MapServerSettings(HonuaBaseModel):
    """MapServer rendering settings."""
    enabled: bool
    max_image_width: Optional[int] = None
    max_image_height: Optional[int] = None
    max_record_count: Optional[int] = None


class AccessPolicy(HonuaBaseModel):
    """Service access policy settings."""
    public_read: bool
    admin_role: Optional[str] = None
    read_roles: Optional[List[str]] = None
    write_roles: Optional[List[str]] = None


class TimeInfo(HonuaBaseModel):
    """Temporal metadata settings."""
    enabled: bool
    time_field: Optional[str] = None
    time_extent: Optional[List[str]] = None


class ServiceSettings(HonuaBaseModel):
    """Complete service settings."""
    display_name: str
    enabled: bool
    protocols: List[str]
    map_server: Optional[MapServerSettings] = None
    access_policy: Optional[AccessPolicy] = None
    time_info: Optional[TimeInfo] = None


class ServiceSettingsResponse(HonuaBaseModel):
    """Response containing service settings."""
    service_name: str
    settings: ServiceSettings


# Connection Models

class SecureConnectionSummary(HonuaBaseModel):
    """Summary of a secure database connection."""
    id: str
    name: str
    description: Optional[str] = None
    connection_string: str
    enabled: bool
    last_tested: Optional[datetime] = None
    test_status: Optional[Literal['success', 'failure', 'pending']] = None


class SecureConnectionDetail(HonuaBaseModel):
    """Detailed information about a secure database connection."""
    id: str
    name: str
    description: Optional[str] = None
    connection_string: str
    enabled: bool
    last_tested: Optional[datetime] = None
    test_status: Optional[Literal['success', 'failure', 'pending']] = None
    metadata: Optional[Dict[str, Any]] = None


class CreateSecureConnectionRequest(HonuaBaseModel):
    """Request to create a new secure connection."""
    name: str
    description: Optional[str] = None
    connection_string: str
    enabled: bool = True
    metadata: Optional[Dict[str, Any]] = None


class UpdateSecureConnectionRequest(HonuaBaseModel):
    """Request to update an existing secure connection."""
    name: Optional[str] = None
    description: Optional[str] = None
    connection_string: Optional[str] = None
    enabled: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class ConnectionTestResult(HonuaBaseModel):
    """Result of a connection test."""
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None


# Layer Models

class PublishedLayerSummary(HonuaBaseModel):
    """Summary of a published layer."""
    layer_id: int
    service_name: str
    layer_name: str
    table_name: str
    enabled: bool
    geometry_type: str
    srid: int
    last_modified: datetime


class PublishLayerRequest(HonuaBaseModel):
    """Request to publish a new layer."""
    service_name: str
    layer_name: str
    table_name: str
    enabled: bool = True
    geometry_field: Optional[str] = None
    srid: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


# Discovery Models

class GeometryColumn(HonuaBaseModel):
    """Information about a geometry column."""
    column_name: str
    geometry_type: str
    srid: int
    dimensions: int


class DiscoveredTable(HonuaBaseModel):
    """Information about a discovered PostGIS table."""
    schema: str
    table_name: str
    geometry_columns: List[GeometryColumn]
    record_count: Optional[int] = None
    last_modified: Optional[datetime] = None


class TableDiscoveryResponse(HonuaBaseModel):
    """Response from table discovery operation."""
    connection_id: str
    tables: List[DiscoveredTable]
    timestamp: datetime


# Metadata Models

class ResourceMetadata(HonuaBaseModel):
    """Metadata for a Kubernetes-style resource."""
    name: str
    namespace: str
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, str]] = None


class MetadataResource(HonuaBaseModel):
    """Kubernetes-style metadata resource."""
    api_version: str
    kind: str
    metadata: ResourceMetadata
    spec: Dict[str, Any]
    status: Optional[Dict[str, Any]] = None


class AdminCapabilitiesResponse(HonuaBaseModel):
    """Admin API capabilities."""
    version: str
    features: List[str]
    limits: Dict[str, Optional[int]]


class MetadataManifest(HonuaBaseModel):
    """Collection of metadata resources."""
    api_version: str
    kind: str
    resources: List[MetadataResource]


class ManifestApplyRequest(HonuaBaseModel):
    """Request to apply a metadata manifest."""
    manifest: MetadataManifest
    dry_run: bool = False
    force: bool = False


class ManifestApplyResult(HonuaBaseModel):
    """Result of applying a metadata manifest."""
    applied: int
    skipped: int
    failed: int
    errors: Optional[List[str]] = None


# Bulk Operation Models

class BulkImportOptions(HonuaBaseModel):
    """Options for bulk import operations."""
    srid: Optional[int] = None
    encoding: Optional[str] = None
    delimiter: Optional[str] = None
    geometry_field: Optional[str] = None
    overwrite: bool = False


class BulkExportOptions(HonuaBaseModel):
    """Options for bulk export operations."""
    srid: Optional[int] = None
    encoding: Optional[str] = None
    include_metadata: bool = False


class BulkImportRequest(HonuaBaseModel):
    """Request for bulk import operation."""
    service_name: str
    format: Optional[Literal['shapefile', 'geojson', 'csv']] = None
    options: Optional[BulkImportOptions] = None


class BulkExportRequest(HonuaBaseModel):
    """Request for bulk export operation."""
    service_name: str
    layer_ids: List[int]
    format: Literal['shapefile', 'geojson', 'csv', 'geopackage']
    options: Optional[BulkExportOptions] = None


class BulkOperationResult(HonuaBaseModel):
    """Result of a bulk operation."""
    operation_id: str
    status: Literal['pending', 'running', 'completed', 'failed']
    records_processed: Optional[int] = None
    total_records: Optional[int] = None
    errors: Optional[List[str]] = None
    download_url: Optional[str] = None