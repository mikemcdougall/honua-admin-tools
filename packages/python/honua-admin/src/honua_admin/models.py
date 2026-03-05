"""
Data models for Honua admin operations.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LayerConfiguration(BaseModel):
    """Configuration for a geospatial layer."""

    name: str = Field(..., description="Layer name")
    table: str = Field(..., description="Database table name")
    geometry_column: str = Field(default="geom", description="Geometry column name")
    spatial_reference: int = Field(default=4326, description="SRID for spatial reference system")
    display_field: Optional[str] = Field(default=None, description="Field to use for display labels")


class ServiceConfiguration(BaseModel):
    """Configuration for a geospatial service."""

    name: str = Field(..., description="Service name")
    data_source: str = Field(..., description="Data source connection string")
    layers: List[LayerConfiguration] = Field(..., description="Layer configurations")
    description: Optional[str] = Field(default=None, description="Service description")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class BulkImportOptions(BaseModel):
    """Options for bulk import operations."""

    service_id: str = Field(..., description="Target service ID")
    layer_id: int = Field(..., description="Target layer ID")
    format: str = Field(default="geojson", description="Data format (geojson, shapefile, csv)")
    batch_size: Optional[int] = Field(default=1000, description="Number of features per batch")
    validation_mode: str = Field(default="strict", description="Validation mode (strict, lenient)")
    overwrite: bool = Field(default=False, description="Whether to overwrite existing data")


class ImportProgress(BaseModel):
    """Progress information for bulk imports."""

    processed_count: int = Field(..., description="Number of features processed")
    total_count: int = Field(..., description="Total number of features")
    percentage: float = Field(..., description="Completion percentage")
    message: str = Field(..., description="Current status message")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")


class UserCreateRequest(BaseModel):
    """Request model for creating a user."""

    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    password: Optional[str] = Field(default=None, description="Password (if not using SSO)")
    roles: List[str] = Field(default_factory=list, description="User roles")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User metadata")


class PermissionLevel(BaseModel):
    """Permission level for service access."""

    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


class ServiceHealth(BaseModel):
    """Health status of a service."""

    service_id: str = Field(..., description="Service ID")
    status: str = Field(..., description="Health status (healthy, degraded, unhealthy)")
    last_check: str = Field(..., description="Last health check timestamp")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Health check details")


class ServiceMetrics(BaseModel):
    """Performance metrics for a service."""

    service_id: str = Field(..., description="Service ID")
    request_count: int = Field(..., description="Number of requests")
    average_response_time: float = Field(..., description="Average response time in milliseconds")
    error_rate: float = Field(..., description="Error rate percentage")
    timestamp: str = Field(..., description="Metrics timestamp")