"""Honua Admin API client implementation."""

import json
from typing import Dict, List, Optional, Tuple, Union, Any
from urllib.parse import urljoin, urlencode
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import HonuaAdminError, HonuaAdminApiError, HonuaAdminOperationError
from . import models


class HonuaAdminClient:
    """
    Client for the Honua Admin REST API.

    Provides administrative functionality for managing Honua geospatial services,
    including service configuration, connection management, layer publishing, and bulk operations.

    Args:
        server_url: The base URL of the Honua server
        api_key: API key for authentication
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum number of retries for failed requests (default: 3)
        headers: Additional headers to include with all requests

    Example:
        >>> client = HonuaAdminClient(
        ...     server_url='https://api.honua.dev',
        ...     api_key='your-admin-api-key'
        ... )
        >>> services = client.list_services()
        >>> print(f"Found {len(services)} services")
    """

    def __init__(
        self,
        server_url: str,
        api_key: str,
        timeout: float = 30.0,
        max_retries: int = 3,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.server_url = server_url.rstrip('/')
        self.base_url = urljoin(self.server_url + '/', 'admin/v1/')
        self.timeout = timeout

        # Create session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'X-API-Key': api_key,
            'User-Agent': f'honua-admin-python/1.0.0a1',
        })

        if headers:
            self.session.headers.update(headers)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Make an HTTP request to the API."""
        url = urljoin(self.base_url, path.lstrip('/'))

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                files=files,
                timeout=self.timeout,
            )

            # Raise for HTTP errors
            if not response.ok:
                try:
                    error_data = response.json()
                    message = error_data.get('message', f'HTTP {response.status_code} error')
                except (ValueError, KeyError):
                    message = f'HTTP {response.status_code} error'

                raise HonuaAdminApiError(
                    message=message,
                    status_code=response.status_code,
                    response=error_data if 'error_data' in locals() else None,
                )

            return response

        except requests.exceptions.Timeout:
            raise HonuaAdminOperationError('Request timeout')
        except requests.exceptions.ConnectionError:
            raise HonuaAdminOperationError('Connection error')
        except requests.exceptions.RequestException as e:
            raise HonuaAdminOperationError(f'Request failed: {e}')

    def _get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request and return JSON response."""
        response = self._request('GET', path, params=params)
        return response.json()

    def _post_json(self, path: str, json_data: Dict[str, Any]) -> Any:
        """Make a POST request with JSON data and return JSON response."""
        response = self._request('POST', path, json_data=json_data)
        return response.json() if response.content else None

    def _patch_json(self, path: str, json_data: Dict[str, Any]) -> Any:
        """Make a PATCH request with JSON data and return JSON response."""
        response = self._request('PATCH', path, json_data=json_data)
        return response.json()

    def _put_json(self, path: str, json_data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Any:
        """Make a PUT request with JSON data and return JSON response."""
        if headers:
            # Temporarily update session headers
            original_headers = self.session.headers.copy()
            self.session.headers.update(headers)
            try:
                response = self._request('PUT', path, json_data=json_data)
                return response.json()
            finally:
                self.session.headers = original_headers
        else:
            response = self._request('PUT', path, json_data=json_data)
            return response.json()

    def _delete(self, path: str, headers: Optional[Dict[str, str]] = None) -> None:
        """Make a DELETE request."""
        if headers:
            original_headers = self.session.headers.copy()
            self.session.headers.update(headers)
            try:
                self._request('DELETE', path)
            finally:
                self.session.headers = original_headers
        else:
            self._request('DELETE', path)

    # Services

    def list_services(self) -> List[models.ServiceSummary]:
        """List all registered services."""
        data = self._get_json('/services')
        return [models.ServiceSummary(**service) for service in data]

    def get_service_settings(self, service_name: str) -> models.ServiceSettingsResponse:
        """Get the settings for a specific service."""
        data = self._get_json(f'/services/{service_name}')
        return models.ServiceSettingsResponse(**data)

    def update_protocols(self, service_name: str, protocols: List[str]) -> models.ServiceSettingsResponse:
        """Update the enabled protocols for a service."""
        data = self._patch_json(f'/services/{service_name}/protocols', {'protocols': protocols})
        return models.ServiceSettingsResponse(**data)

    # Connections

    def list_connections(self) -> List[models.SecureConnectionSummary]:
        """List all secure database connections."""
        data = self._get_json('/connections')
        return [models.SecureConnectionSummary(**conn) for conn in data]

    def get_connection(self, connection_id: str) -> models.SecureConnectionDetail:
        """Get detailed information about a secure database connection."""
        data = self._get_json(f'/connections/{connection_id}')
        return models.SecureConnectionDetail(**data)

    def create_connection(self, request: models.CreateSecureConnectionRequest) -> models.SecureConnectionSummary:
        """Create a new secure database connection."""
        data = self._post_json('/connections', request.model_dump())
        return models.SecureConnectionSummary(**data)

    def test_draft_connection(self, request: models.CreateSecureConnectionRequest) -> models.ConnectionTestResult:
        """Test a connection before saving."""
        data = self._post_json('/connections/test', request.model_dump())
        return models.ConnectionTestResult(**data)

    def update_connection(
        self,
        connection_id: str,
        request: models.UpdateSecureConnectionRequest
    ) -> models.SecureConnectionSummary:
        """Update an existing secure database connection."""
        data = self._patch_json(f'/connections/{connection_id}', request.model_dump(exclude_unset=True))
        return models.SecureConnectionSummary(**data)

    def test_connection(self, connection_id: str) -> models.ConnectionTestResult:
        """Test the health of an existing connection."""
        data = self._post_json(f'/connections/{connection_id}/test', {})
        return models.ConnectionTestResult(**data)

    def delete_connection(self, connection_id: str) -> None:
        """Delete a secure database connection."""
        self._delete(f'/connections/{connection_id}')

    # Layers

    def list_layers(
        self,
        connection_id: str,
        service_name: Optional[str] = None
    ) -> List[models.PublishedLayerSummary]:
        """List published layers for a connection."""
        params = {'serviceName': service_name} if service_name else None
        data = self._get_json(f'/connections/{connection_id}/layers', params=params)
        return [models.PublishedLayerSummary(**layer) for layer in data]

    def publish_layer(
        self,
        connection_id: str,
        request: models.PublishLayerRequest
    ) -> models.PublishedLayerSummary:
        """Publish a PostGIS table as a layer."""
        data = self._post_json(f'/connections/{connection_id}/layers', request.model_dump())
        return models.PublishedLayerSummary(**data)

    def set_layer_enabled(
        self,
        connection_id: str,
        layer_id: int,
        enabled: bool,
        service_name: Optional[str] = None
    ) -> models.PublishedLayerSummary:
        """Enable or disable a specific layer."""
        params = {'serviceName': service_name} if service_name else None
        data = self._patch_json(
            f'/connections/{connection_id}/layers/{layer_id}',
            {'enabled': enabled}
        )
        return models.PublishedLayerSummary(**data)

    def set_service_layers_enabled(
        self,
        connection_id: str,
        enabled: bool,
        service_name: Optional[str] = None
    ) -> List[models.PublishedLayerSummary]:
        """Enable or disable all layers for a service."""
        params = {'serviceName': service_name} if service_name else None
        data = self._patch_json(
            f'/connections/{connection_id}/layers',
            {'enabled': enabled}
        )
        return [models.PublishedLayerSummary(**layer) for layer in data]

    # Discovery

    def discover_tables(self, connection_id: str) -> models.TableDiscoveryResponse:
        """Discover PostGIS tables available on a connection."""
        data = self._get_json(f'/connections/{connection_id}/discover')
        return models.TableDiscoveryResponse(**data)

    # Metadata Resources

    def list_metadata_resources(
        self,
        kind: Optional[str] = None,
        ns: Optional[str] = None
    ) -> List[models.MetadataResource]:
        """List metadata resources, optionally filtered by kind and namespace."""
        params = {}
        if kind:
            params['kind'] = kind
        if ns:
            params['ns'] = ns

        data = self._get_json('/metadata', params=params if params else None)
        return [models.MetadataResource(**resource) for resource in data]

    def get_metadata_resource(
        self,
        kind: str,
        ns: str,
        name: str
    ) -> Tuple[models.MetadataResource, Optional[str]]:
        """Get a specific metadata resource by its identifier."""
        response = self._request('GET', f'/metadata/{kind}/{ns}/{name}')
        resource = models.MetadataResource(**response.json())
        etag = response.headers.get('ETag')
        return resource, etag

    def create_metadata_resource(self, resource: models.MetadataResource) -> models.MetadataResource:
        """Create a new metadata resource."""
        data = self._post_json('/metadata', resource.model_dump())
        return models.MetadataResource(**data)

    def update_metadata_resource(
        self,
        kind: str,
        ns: str,
        name: str,
        resource: models.MetadataResource,
        if_match: Optional[str] = None
    ) -> models.MetadataResource:
        """Update an existing metadata resource."""
        headers = {'If-Match': if_match} if if_match else None
        data = self._put_json(f'/metadata/{kind}/{ns}/{name}', resource.model_dump(), headers=headers)
        return models.MetadataResource(**data)

    def delete_metadata_resource(
        self,
        kind: str,
        ns: str,
        name: str,
        if_match: Optional[str] = None
    ) -> None:
        """Delete a metadata resource."""
        headers = {'If-Match': if_match} if if_match else None
        self._delete(f'/metadata/{kind}/{ns}/{name}', headers=headers)

    # Manifests

    def get_capabilities(self) -> models.AdminCapabilitiesResponse:
        """Get the admin API capabilities."""
        data = self._get_json('/capabilities')
        return models.AdminCapabilitiesResponse(**data)

    def get_manifest(self, ns: Optional[str] = None) -> models.MetadataManifest:
        """Export the metadata manifest."""
        params = {'ns': ns} if ns else None
        data = self._get_json('/manifest', params=params)
        return models.MetadataManifest(**data)

    def apply_manifest(self, request: models.ManifestApplyRequest) -> models.ManifestApplyResult:
        """Apply a metadata manifest."""
        data = self._post_json('/manifest', request.model_dump())
        return models.ManifestApplyResult(**data)

    # Bulk Operations for GeoPandas integration

    def bulk_import_geodataframe(
        self,
        connection_id: str,
        gdf: 'geopandas.GeoDataFrame',
        service_name: str,
        table_name: Optional[str] = None,
        srid: Optional[int] = None,
        overwrite: bool = False
    ) -> models.BulkOperationResult:
        """
        Import a GeoPandas GeoDataFrame as a layer.

        Args:
            connection_id: Database connection identifier
            gdf: GeoPandas GeoDataFrame to import
            service_name: Target service name
            table_name: Target table name (defaults to service name)
            srid: Target spatial reference ID
            overwrite: Whether to overwrite existing table

        Returns:
            Result of the bulk import operation

        Note:
            Requires geopandas to be installed: pip install honua-admin[geospatial]
        """
        try:
            import geopandas as gpd
            import tempfile
            import os
        except ImportError:
            raise HonuaAdminOperationError(
                "GeoPandas is required for this operation. Install with: pip install honua-admin[geospatial]"
            )

        # Create temporary GeoJSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.geojson', delete=False) as tmp_file:
            try:
                # Convert to target SRID if specified
                if srid and gdf.crs:
                    gdf = gdf.to_crs(f'EPSG:{srid}')

                # Export to GeoJSON
                gdf.to_file(tmp_file.name, driver='GeoJSON')

                # Upload via bulk import
                with open(tmp_file.name, 'rb') as f:
                    files = {'file': ('data.geojson', f, 'application/geo+json')}
                    form_data = {
                        'connectionId': connection_id,
                        'serviceName': service_name,
                        'options': json.dumps({
                            'format': 'geojson',
                            'tableName': table_name or service_name.replace('-', '_'),
                            'srid': srid,
                            'overwrite': overwrite,
                        })
                    }

                    # Remove JSON content type for multipart upload
                    original_content_type = self.session.headers.get('Content-Type')
                    if 'Content-Type' in self.session.headers:
                        del self.session.headers['Content-Type']

                    try:
                        response = self._request('POST', '/bulk/import', files=files, json_data=form_data)
                        data = response.json()
                        return models.BulkOperationResult(**data)
                    finally:
                        # Restore content type
                        if original_content_type:
                            self.session.headers['Content-Type'] = original_content_type

            finally:
                # Clean up temporary file
                os.unlink(tmp_file.name)

    def bulk_export_to_geodataframe(
        self,
        service_name: str,
        layer_ids: List[int],
        srid: Optional[int] = None
    ) -> 'geopandas.GeoDataFrame':
        """
        Export layers to a GeoPandas GeoDataFrame.

        Args:
            service_name: Source service name
            layer_ids: List of layer IDs to export
            srid: Target spatial reference ID for output

        Returns:
            GeoPandas GeoDataFrame with exported data

        Note:
            Requires geopandas to be installed: pip install honua-admin[geospatial]
        """
        try:
            import geopandas as gpd
            import tempfile
            import os
        except ImportError:
            raise HonuaAdminOperationError(
                "GeoPandas is required for this operation. Install with: pip install honua-admin[geospatial]"
            )

        # Request bulk export
        request = models.BulkExportRequest(
            service_name=service_name,
            layer_ids=layer_ids,
            format='geojson',
            options={'srid': srid} if srid else None
        )

        result = self.bulk_export(request)

        if not result.download_url:
            raise HonuaAdminOperationError("Export did not provide download URL")

        # Download and load as GeoDataFrame
        response = requests.get(result.download_url, timeout=self.timeout)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.geojson', delete=False) as tmp_file:
            try:
                tmp_file.write(response.content)
                tmp_file.flush()

                # Load as GeoDataFrame
                gdf = gpd.read_file(tmp_file.name)

                # Convert to target SRID if specified and different
                if srid and gdf.crs != f'EPSG:{srid}':
                    gdf = gdf.to_crs(f'EPSG:{srid}')

                return gdf

            finally:
                os.unlink(tmp_file.name)

    def bulk_export(self, request: models.BulkExportRequest) -> models.BulkOperationResult:
        """Perform a bulk export operation."""
        data = self._post_json('/bulk/export', request.model_dump())
        return models.BulkOperationResult(**data)