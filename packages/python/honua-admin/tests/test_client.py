"""
Tests for HonuaAdminClient.
"""

import pytest
from unittest.mock import AsyncMock, patch
import httpx

from honua_admin import HonuaAdminClient, ServiceConfiguration, LayerConfiguration
from honua_admin.exceptions import AuthenticationError, ServiceNotFoundError


@pytest.mark.asyncio
async def test_client_initialization():
    """Test client initialization."""
    client = HonuaAdminClient(
        base_url='https://api.example.com',
        api_key='test-key',
        timeout=30.0,
        retry_attempts=3
    )

    assert client.base_url == 'https://api.example.com'
    assert client.api_key == 'test-key'
    assert client.timeout == 30.0
    assert client.retry_attempts == 3


@pytest.mark.asyncio
async def test_create_service_success():
    """Test successful service creation."""
    client = HonuaAdminClient('https://api.example.com', 'test-key')

    config = ServiceConfiguration(
        name='test-service',
        data_source='postgresql://localhost/test',
        layers=[
            LayerConfiguration(name='layer1', table='table1')
        ]
    )

    mock_response = AsyncMock()
    mock_response.json.return_value = {'id': 'service-123', 'url': 'https://api.example.com/services/service-123'}
    mock_response.raise_for_status.return_value = None

    with patch.object(client._client, 'post', return_value=mock_response) as mock_post:
        result = await client.create_service(config)

        assert result['id'] == 'service-123'
        assert result['url'] == 'https://api.example.com/services/service-123'
        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_create_service_auth_error():
    """Test service creation with authentication error."""
    client = HonuaAdminClient('https://api.example.com', 'invalid-key')

    config = ServiceConfiguration(
        name='test-service',
        data_source='postgresql://localhost/test',
        layers=[LayerConfiguration(name='layer1', table='table1')]
    )

    mock_response = AsyncMock()
    mock_response.status_code = 401
    mock_response.text = 'Unauthorized'

    mock_error = httpx.HTTPStatusError(
        message='Unauthorized',
        request=AsyncMock(),
        response=mock_response
    )

    with patch.object(client._client, 'post', side_effect=mock_error):
        with pytest.raises(AuthenticationError, match='Invalid API key'):
            await client.create_service(config)


@pytest.mark.asyncio
async def test_list_services():
    """Test listing services."""
    client = HonuaAdminClient('https://api.example.com', 'test-key')

    mock_response = AsyncMock()
    mock_response.json.return_value = [
        {'id': 'service-1', 'name': 'Service 1'},
        {'id': 'service-2', 'name': 'Service 2'}
    ]
    mock_response.raise_for_status.return_value = None

    with patch.object(client._client, 'get', return_value=mock_response) as mock_get:
        services = await client.list_services()

        assert len(services) == 2
        assert services[0]['id'] == 'service-1'
        assert services[1]['id'] == 'service-2'
        mock_get.assert_called_once_with('/admin/services')


@pytest.mark.asyncio
async def test_get_service_not_found():
    """Test getting a service that doesn't exist."""
    client = HonuaAdminClient('https://api.example.com', 'test-key')

    mock_response = AsyncMock()
    mock_response.status_code = 404
    mock_response.text = 'Service not found'

    mock_error = httpx.HTTPStatusError(
        message='Not Found',
        request=AsyncMock(),
        response=mock_response
    )

    with patch.object(client._client, 'get', side_effect=mock_error):
        with pytest.raises(ServiceNotFoundError, match='Service nonexistent not found'):
            await client.get_service('nonexistent')


@pytest.mark.asyncio
async def test_context_manager():
    """Test using client as async context manager."""
    async with HonuaAdminClient('https://api.example.com', 'test-key') as client:
        assert isinstance(client, HonuaAdminClient)
        # Client should be usable within context