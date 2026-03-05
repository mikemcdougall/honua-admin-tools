# honua-admin

[![PyPI Version](https://img.shields.io/pypi/v/honua-admin.svg)](https://pypi.org/project/honua-admin/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/pypi/pyversions/honua-admin.svg)](https://pypi.org/project/honua-admin/)

**Python admin tooling for Honua geospatial platform**

Part of the [honua-admin-tools](https://github.com/mikemcdougall/honua-admin-tools) ecosystem for multi-language admin operations.

## Installation

```bash
pip install honua-admin
```

## Quick Start

### Python API

```python
import asyncio
from honua_admin import HonuaAdminClient, ServiceConfiguration, LayerConfiguration

async def main():
    async with HonuaAdminClient('https://api.honua.com', 'your-api-key') as client:
        # Create a new service
        config = ServiceConfiguration(
            name='my-service',
            data_source='postgresql://localhost:5432/geodata',
            layers=[
                LayerConfiguration(
                    name='parcels',
                    table='public.parcels',
                    geometry_column='geom'
                )
            ]
        )

        service = await client.create_service(config)
        print(f"Created service: {service['id']}")

        # Import features with progress tracking
        from honua_admin import BulkImportOptions

        options = BulkImportOptions(
            service_id=service['id'],
            layer_id=0,
            format='geojson',
            batch_size=1000
        )

        async for progress in client.import_features(options, 'data.geojson'):
            print(f"Progress: {progress.percentage:.1f}% - {progress.message}")

# Run the example
asyncio.run(main())
```

### Command Line Interface

```bash
# Initialize configuration
honua-admin config init --base-url https://api.honua.com --api-key your-key

# Deploy a service from YAML configuration
honua-admin service deploy service-config.yaml

# Import features with progress
honua-admin import features my-service 0 data.geojson --show-progress

# List all services
honua-admin service list
```

## Configuration File

Create a service configuration file (`service.yaml`):

```yaml
name: parcels-service
description: Property parcel data service
data_source: postgresql://localhost:5432/gis

layers:
  - name: parcels
    table: public.parcels
    geometry_column: geom
    spatial_reference: 4326
    display_field: owner_name

  - name: buildings
    table: public.buildings
    geometry_column: geom
    spatial_reference: 4326
    display_field: address

metadata:
  contact: gis-admin@example.com
  update_frequency: daily
```

## Advanced Usage

### Bulk Operations with Progress Tracking

```python
import asyncio
from honua_admin import HonuaAdminClient, BulkImportOptions

async def bulk_import_with_progress():
    async with HonuaAdminClient('https://api.honua.com', 'your-api-key') as client:
        options = BulkImportOptions(
            service_id='my-service',
            layer_id=0,
            format='geojson',
            batch_size=500,
            validation_mode='strict'
        )

        def progress_callback(progress):
            print(f"Imported {progress.processed_count}/{progress.total_count} features")

        async for progress in client.import_features(
            options,
            'large-dataset.geojson',
            on_progress=progress_callback
        ):
            if progress.errors:
                print(f"Errors: {progress.errors}")

asyncio.run(bulk_import_with_progress())
```

### Service Health Monitoring

```python
async def monitor_service_health():
    async with HonuaAdminClient('https://api.honua.com', 'your-api-key') as client:
        # Check service health
        health = await client.get_service_health('my-service')
        print(f"Service status: {health.status}")

        # Get performance metrics
        metrics = await client.get_service_metrics('my-service', time_range='24h')
        print(f"Average response time: {metrics.average_response_time}ms")
```

### Error Handling

```python
from honua_admin import HonuaAdminError, AuthenticationError, ServiceNotFoundError

async def handle_errors():
    try:
        async with HonuaAdminClient('https://api.honua.com', 'invalid-key') as client:
            await client.list_services()
    except AuthenticationError:
        print("Invalid API key")
    except ServiceNotFoundError as e:
        print(f"Service not found: {e.message}")
    except HonuaAdminError as e:
        print(f"Admin operation failed: {e.message}")
```

## CLI Commands

### Service Management

```bash
# Deploy service with dry-run first
honua-admin service deploy config.yaml --dry-run
honua-admin service deploy config.yaml

# List all services
honua-admin service list

# Get service details
honua-admin service get my-service-id
```

### Data Import/Export

```bash
# Import GeoJSON data
honua-admin import features my-service 0 parcels.geojson --show-progress

# Import Shapefile with custom batch size
honua-admin import features my-service 0 buildings.shp --batch-size 500

# Export service data
honua-admin export features my-service 0 --format geojson > export.json
```

## Architecture

This Python package is part of the functionality-first architecture:

| Technology | Package | Purpose |
|------------|---------|---------|
| **Python** | honua-admin | Scripting and automation |
| **CLI** | @honua/cli | Command-line operations |
| **JavaScript** | @honua/admin-tools | Web admin interfaces |
| **.NET** | Honua.Admin.Tools | Blazor components |

## Development

```bash
# Clone repository
git clone https://github.com/mikemcdougall/honua-admin-tools.git
cd honua-admin-tools/packages/python/honua-admin

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black src/
isort src/
flake8 src/

# Run type checking
mypy src/honua_admin/
```

## Documentation

See the [honua-admin-tools repository](https://github.com/mikemcdougall/honua-admin-tools) for complete documentation and examples.

## License

Licensed under the Apache License, Version 2.0.