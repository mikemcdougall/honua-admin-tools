# @honua/cli

[![NPM Version](https://img.shields.io/npm/v/@honua/cli.svg)](https://www.npmjs.com/package/@honua/cli)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Command-line tool for Honua geospatial platform administration**

Part of the [honua-admin-tools](https://github.com/mikemcdougall/honua-admin-tools) ecosystem for multi-language admin operations.

## Installation

```bash
# Install globally for CLI usage
npm install -g @honua/cli

# Or install locally in your project
npm install @honua/cli
```

## Quick Start

```bash
# Initialize CLI configuration
honua config init --url https://api.honua.com --api-key your-key

# Deploy a service
honua service deploy ./service-config.yaml

# Import features
honua import features my-service 0 data.geojson --progress
```

## Configuration

Initialize your CLI configuration:

```bash
honua config init --url https://api.honua.com --api-key your-api-key
```

This creates a configuration file at `~/.honua/config.json`.

## Commands

### Service Management

```bash
# Deploy a service from configuration file
honua service deploy <config-file> [options]

# Options:
#   --environment <env>  Target environment (default: production)
#   --dry-run            Preview changes without deploying
```

Example service configuration (`service.yaml`):

```yaml
name: parcels-service
dataSource: postgresql://localhost:5432/gis
layers:
  - name: parcels
    table: public.parcels
    geometryColumn: geom
    spatialReference: 4326
  - name: buildings
    table: public.buildings
    geometryColumn: geom
    spatialReference: 4326
```

### Data Import

```bash
# Import features from file
honua import features <service-id> <layer-id> <file> [options]

# Options:
#   --progress           Show progress bar
#   --batch-size <size>  Number of features per batch (default: 1000)
#   --format <format>    Force file format (geojson, shapefile, csv)
```

Supported file formats:
- **GeoJSON** (`.geojson`, `.json`)
- **Shapefile** (`.shp` with associated files)
- **CSV** (`.csv` with lat/lon or WKT columns)

### Configuration

```bash
# Initialize configuration
honua config init --url <api-url> --api-key <key>

# View current configuration
honua config show

# Update configuration
honua config set --url <new-url>
honua config set --api-key <new-key>
```

## Examples

### Deploy Multiple Services

```bash
# Deploy to development environment
honua service deploy ./dev-config.yaml --environment development

# Deploy to production with dry-run first
honua service deploy ./prod-config.yaml --dry-run
honua service deploy ./prod-config.yaml
```

### Bulk Data Import

```bash
# Import parcel data with progress
honua import features parcels-service 0 ./data/parcels.geojson --progress

# Import building data in smaller batches
honua import features parcels-service 1 ./data/buildings.shp --batch-size 500 --progress
```

## Programmatic Usage

You can also use the CLI programmatically in Node.js applications:

```typescript
import { HonuaCLI } from '@honua/cli';

const cli = new HonuaCLI({
  baseUrl: 'https://api.honua.com',
  apiKey: 'your-api-key'
});

// Deploy service
await cli.deployService('./service-config.yaml', {
  environment: 'staging',
  dryRun: false
});

// Import features
await cli.importFeatures('my-service', 0, './data.geojson');
```

## Architecture

This CLI tool is part of the functionality-first architecture:

| Technology | Package | Purpose |
|------------|---------|---------|
| **CLI** | @honua/cli | Command-line operations |
| **JavaScript** | @honua/admin-tools | Web admin interfaces |
| **.NET** | Honua.Admin.Tools | Blazor components |
| **Python** | honua-admin | Scripting and automation |

## Documentation

See the [honua-admin-tools repository](https://github.com/mikemcdougall/honua-admin-tools) for complete documentation and examples.

## License

Licensed under the Apache License, Version 2.0.