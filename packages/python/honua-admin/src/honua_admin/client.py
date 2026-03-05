"""
Honua Admin Client

Main client class for Honua geospatial platform administration.
"""

import asyncio
from typing import List, Optional, AsyncIterator, Dict, Any
import httpx
from pydantic import BaseModel

from .models import ServiceConfiguration, BulkImportOptions, ImportProgress
from .exceptions import HonuaAdminError, AuthenticationError, ServiceNotFoundError


class HonuaAdminClient:
    """Main admin client for Honua geospatial platform."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: Optional[float] = 30.0,
        retry_attempts: int = 3,
    ):
        """
        Initialize the admin client.

        Args:
            base_url: Base URL of the Honua API
            api_key: API key for authentication
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts for failed requests
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.retry_attempts = retry_attempts

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self._client.aclose()

    async def create_service(self, config: ServiceConfiguration) -> Dict[str, Any]:
        """
        Create a new geospatial service.

        Args:
            config: Service configuration

        Returns:
            Dictionary containing service ID and URL

        Raises:
            HonuaAdminError: If service creation fails
            AuthenticationError: If authentication fails
        """
        try:
            response = await self._client.post(
                "/admin/services",
                json=config.model_dump(),
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif e.response.status_code == 400:
                raise HonuaAdminError(f"Invalid service configuration: {e.response.text}")
            else:
                raise HonuaAdminError(f"Service creation failed: {e.response.text}")

    async def list_services(self) -> List[Dict[str, Any]]:
        """
        List all services.

        Returns:
            List of service dictionaries

        Raises:
            HonuaAdminError: If listing services fails
            AuthenticationError: If authentication fails
        """
        try:
            response = await self._client.get("/admin/services")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            else:
                raise HonuaAdminError(f"Failed to list services: {e.response.text}")

    async def get_service(self, service_id: str) -> Dict[str, Any]:
        """
        Get service details.

        Args:
            service_id: Service identifier

        Returns:
            Service details dictionary

        Raises:
            ServiceNotFoundError: If service doesn't exist
            AuthenticationError: If authentication fails
        """
        try:
            response = await self._client.get(f"/admin/services/{service_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif e.response.status_code == 404:
                raise ServiceNotFoundError(f"Service {service_id} not found")
            else:
                raise HonuaAdminError(f"Failed to get service: {e.response.text}")

    async def import_features(
        self,
        options: BulkImportOptions,
        file_path: str,
        on_progress: Optional[callable] = None,
    ) -> AsyncIterator[ImportProgress]:
        """
        Import features in bulk with progress tracking.

        Args:
            options: Import options
            file_path: Path to data file
            on_progress: Optional progress callback

        Yields:
            ImportProgress objects with current progress

        Raises:
            HonuaAdminError: If import fails
        """
        # Implementation would handle file upload and progress tracking
        # This is a placeholder implementation
        total_count = 1000  # Would be determined from file
        batch_size = options.batch_size or 100

        for i in range(0, total_count, batch_size):
            current_batch = min(batch_size, total_count - i)
            processed = i + current_batch
            percentage = (processed / total_count) * 100

            progress = ImportProgress(
                processed_count=processed,
                total_count=total_count,
                percentage=percentage,
                message=f"Imported batch {i//batch_size + 1}",
            )

            if on_progress:
                on_progress(progress)

            yield progress

            # Simulate processing time
            await asyncio.sleep(0.1)

    async def export_service_data(
        self,
        service_id: str,
        layer_id: int,
        format: str = "geojson",
    ) -> bytes:
        """
        Export service data.

        Args:
            service_id: Service identifier
            layer_id: Layer identifier
            format: Export format (geojson, shapefile, csv)

        Returns:
            Exported data as bytes

        Raises:
            HonuaAdminError: If export fails
        """
        try:
            response = await self._client.get(
                f"/admin/services/{service_id}/layers/{layer_id}/export",
                params={"format": format},
            )
            response.raise_for_status()
            return response.content
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif e.response.status_code == 404:
                raise ServiceNotFoundError(f"Service {service_id} or layer {layer_id} not found")
            else:
                raise HonuaAdminError(f"Export failed: {e.response.text}")

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()