# Automation Guide

This guide covers how to use Honua Admin Tools for automation and DevOps workflows.

## Quick Start

### CLI Installation

```bash
# Install via npm (cross-platform)
npm install -g @honua/cli

# Configure
honua config init
```

### Python Installation

```bash
# Install Python package
pip install honua-admin[geospatial]

# For data science workflows
pip install honua-admin[geospatial] jupyter geopandas
```

### .NET Installation

```bash
# Add to your project
dotnet add package Honua.Admin.Tools
```

## Common Automation Patterns

### Infrastructure as Code

#### Terraform Example

```hcl
# Configure the Honua provider
terraform {
  required_providers {
    honua = {
      source = "mikemcdougall/honua"
      version = "~> 1.0"
    }
  }
}

provider "honua" {
  server_url = var.honua_server_url
  api_key    = var.honua_api_key
}

# Create a database connection
resource "honua_connection" "main_db" {
  name              = "production-postgis"
  connection_string = var.database_url
  enabled          = true

  metadata = {
    environment = "production"
    team        = "spatial-analytics"
  }
}

# Define a service
resource "honua_service" "analytics_service" {
  name         = "spatial-analytics"
  display_name = "Spatial Analytics Service"
  protocols    = ["rest", "grpc", "ogc"]

  access_policy {
    public_read = true
    admin_role  = "spatial-admin"
    read_roles  = ["analyst", "viewer"]
  }

  map_server {
    enabled           = true
    max_image_width   = 2048
    max_image_height  = 2048
    max_record_count  = 1000
  }
}

# Publish layers
resource "honua_layer" "population_data" {
  connection_id = honua_connection.main_db.id
  service_name  = honua_service.analytics_service.name

  table_name = "population_by_city"
  layer_name = "Population Data"
  enabled    = true

  metadata = {
    source      = "census-2020"
    update_freq = "yearly"
  }
}
```

### CI/CD Integration

#### GitHub Actions

```yaml
name: Deploy Geospatial Services

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  HONUA_SERVER_URL: ${{ secrets.HONUA_SERVER_URL }}
  HONUA_API_KEY: ${{ secrets.HONUA_API_KEY }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Honua CLI
        run: npm install -g @honua/cli

      - name: Validate configuration
        run: |
          honua services list --dry-run
          honua connections test --all

  deploy:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Honua CLI
        run: npm install -g @honua/cli

      - name: Deploy services
        run: |
          honua metadata apply -f deploy/services.yml
          honua layers publish-batch -f deploy/layers.yml

      - name: Health check
        run: honua services health-check --all
```

#### GitLab CI

```yaml
stages:
  - validate
  - deploy
  - verify

variables:
  HONUA_SERVER_URL: $HONUA_SERVER_URL
  HONUA_API_KEY: $HONUA_API_KEY

validate:
  stage: validate
  image: node:18
  before_script:
    - npm install -g @honua/cli
  script:
    - honua services list --dry-run
    - honua metadata validate -f deploy/
  only:
    - merge_requests
    - main

deploy:
  stage: deploy
  image: node:18
  before_script:
    - npm install -g @honua/cli
  script:
    - honua metadata apply -f deploy/services.yml
    - honua bulk import -f data/ --connection production-db
  only:
    - main

verify:
  stage: verify
  image: node:18
  before_script:
    - npm install -g @honua/cli
  script:
    - honua services health-check --all
    - honua layers verify --all
  only:
    - main
```

### Bulk Data Operations

#### Python Data Processing

```python
import geopandas as gpd
from honua_admin import HonuaAdminClient

# Initialize client
client = HonuaAdminClient(
    server_url='https://api.honua.dev',
    api_key='your-admin-api-key'
)

# Load data with GeoPandas
gdf = gpd.read_file('city_boundaries.geojson')

# Process the data
gdf['area_km2'] = gdf.geometry.area / 1_000_000
gdf['population_density'] = gdf['population'] / gdf['area_km2']

# Upload to Honua
result = client.bulk_import_geodataframe(
    connection_id='production-postgis',
    gdf=gdf,
    service_name='city-analytics',
    table_name='city_boundaries_processed',
    srid=4326,
    overwrite=True
)

print(f"Imported {result.records_processed} records")
```

#### CLI Batch Processing

```bash
#!/bin/bash

# Bulk import from multiple sources
honua bulk import \
  --connection production-db \
  --service spatial-analytics \
  --format shapefile \
  --parallel 4 \
  data/*.shp

# Batch layer publishing
find layers/ -name "*.yml" -exec honua layers publish -f {} \;

# Bulk styling updates
honua layers style-batch \
  --service spatial-analytics \
  --style-template choropleth \
  --field population \
  --color-ramp blues
```

### Monitoring and Alerting

#### Health Monitoring Script

```python
import asyncio
import logging
from honua_admin import HonuaAdminClient
from datadog import initialize, statsd

# Configure monitoring
initialize()
logger = logging.getLogger(__name__)

async def monitor_services():
    client = HonuaAdminClient(
        server_url=os.environ['HONUA_SERVER_URL'],
        api_key=os.environ['HONUA_API_KEY']
    )

    try:
        # Check service health
        services = client.list_services()
        healthy_count = sum(1 for s in services if s.enabled)

        statsd.gauge('honua.services.total', len(services))
        statsd.gauge('honua.services.healthy', healthy_count)

        # Check connection health
        connections = client.list_connections()
        for conn in connections:
            result = client.test_connection(conn.id)
            status = 1 if result.success else 0

            statsd.gauge(
                f'honua.connection.health',
                status,
                tags=[f'connection:{conn.name}']
            )

        # Check recent operations
        # TODO: Add bulk operation monitoring

        logger.info(f"Health check completed: {healthy_count}/{len(services)} services healthy")

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        statsd.increment('honua.health_check.errors')

if __name__ == '__main__':
    asyncio.run(monitor_services())
```

#### Alerting with CLI

```bash
#!/bin/bash

# Health check script for cron/systemd
UNHEALTHY_SERVICES=$(honua services list --format json | jq -r '.[] | select(.enabled == false) | .name')

if [ ! -z "$UNHEALTHY_SERVICES" ]; then
    echo "Unhealthy services detected: $UNHEALTHY_SERVICES"
    # Send to alerting system
    curl -X POST "$SLACK_WEBHOOK" \
      -H 'Content-Type: application/json' \
      -d "{\"text\": \"🚨 Honua services unhealthy: $UNHEALTHY_SERVICES\"}"
    exit 1
fi

echo "All services healthy"
```

### Database Migration Workflows

#### Schema Migration with CLI

```bash
#!/bin/bash

# Backup before migration
honua connections backup production-db --format sql

# Apply schema migrations
psql $DATABASE_URL -f migrations/001_add_temporal_columns.sql
psql $DATABASE_URL -f migrations/002_update_indexes.sql

# Refresh service metadata
honua services refresh production-service

# Verify layer integrity
honua layers verify --service production-service --connection production-db

echo "Migration completed successfully"
```

#### Python Migration Script

```python
from honua_admin import HonuaAdminClient
import sqlalchemy as sa
from alembic import command
from alembic.config import Config

def run_migration():
    # Run Alembic migrations
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    # Update Honua service metadata
    client = HonuaAdminClient(
        server_url=os.environ['HONUA_SERVER_URL'],
        api_key=os.environ['HONUA_API_KEY']
    )

    # Rediscover tables after schema changes
    result = client.discover_tables('production-db')
    print(f"Discovered {len(result.tables)} tables")

    # Republish affected layers
    for table in result.tables:
        if table.table_name in ['cities', 'boundaries', 'demographics']:
            client.publish_layer(
                connection_id='production-db',
                request={
                    'service_name': 'analytics',
                    'layer_name': table.table_name.title(),
                    'table_name': table.table_name,
                    'enabled': True
                }
            )

if __name__ == '__main__':
    run_migration()
```

## Best Practices

### Security

1. **API Key Management**
   - Use environment variables for API keys
   - Rotate keys regularly
   - Use different keys for different environments

2. **Network Security**
   - Use HTTPS endpoints
   - Implement IP allowlists where appropriate
   - Monitor API access logs

### Performance

1. **Batch Operations**
   - Use bulk import/export for large datasets
   - Process operations in parallel where possible
   - Monitor operation status for long-running jobs

2. **Connection Pooling**
   - Configure appropriate connection limits
   - Monitor database connection health
   - Use connection retries with exponential backoff

### Reliability

1. **Error Handling**
   - Implement comprehensive error handling
   - Use retries for transient failures
   - Log all operations for debugging

2. **Monitoring**
   - Set up health checks for all services
   - Monitor API response times
   - Alert on service degradation

### Documentation

1. **Configuration Management**
   - Document all configuration options
   - Use infrastructure as code
   - Version control all configurations

2. **Runbooks**
   - Create operational runbooks
   - Document disaster recovery procedures
   - Maintain deployment guides